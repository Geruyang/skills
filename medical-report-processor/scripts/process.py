"""
体检报告处理器 - 核心处理脚本
=====================================

这个脚本负责：
1. 从PDF体检报告中提取文本内容
2. 识别医院名称和患者信息
3. 提取各项医学指标数据
4. 生成标准化的映射文件和数据文件

"""

import argparse
import csv
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ============================================================
# 第一步：加载标准模板
# ============================================================

def load_mappings_template() -> List[Dict[str, str]]:
    """
    加载指标映射模板（核心配置文件）

    这个模板定义了所有需要提取的标准指标，包括：
    - 指标的标准中文名称（canonical_name）
    - 指标的标准英文名称（official_feature_name）
    - 单位、参考范围、分组等信息

    返回：包含所有指标定义的列表
    """
    skill_dir = Path(__file__).parent.parent
    template_path = skill_dir / "assets" / "mappings_template.csv"

    with open(template_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader)


# ============================================================
# 第二步：收集和读取PDF文件
# ============================================================

def collect_pdf_files(paths: List[str]) -> List[Path]:
    """
    收集所有需要处理的PDF文件

    支持三种输入方式：
    1. 单个PDF文件路径
    2. 多个PDF文件路径
    3. 包含PDF的文件夹路径

    参数：
        paths: 文件路径列表

    返回：整理后的PDF文件路径列表
    """
    pdf_files = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            # 如果是文件夹，递归搜索所有PDF文件
            pdf_files.extend(sorted(path.rglob("*.pdf")))
        elif path.is_file() and path.suffix.lower() == ".pdf":
            # 如果是PDF文件，直接添加
            pdf_files.append(path)
        else:
            print(f"  [SKIP] Not a PDF: {p}")
    return pdf_files


def read_pdf_text(pdf_path: Path) -> str:
    """
    从PDF文件中提取文本内容

    这个函数会尝试多个PDF解析库（按优先级）：
    1. PyPDF2 - 纯Python实现，兼容性好
    2. pdfplumber - 表格提取能力强
    3. pymupdf (fitz) - 速度快，功能全

    参数：
        pdf_path: PDF文件路径

    返回：提取的文本内容
    """
    # 尝试PyPDF2（优先）
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(str(pdf_path))
        text = "\n".join(
            page.extract_text() or "" for page in reader.pages
        )
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # 尝试pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(str(pdf_path)) as pdf:
            text = "\n".join(
                page.extract_text() or "" for page in pdf.pages
            )
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # 尝试pymupdf (fitz)
    try:
        import fitz
        doc = fitz.open(str(pdf_path))
        text = "\n".join(
            page.get_text() for page in doc
        )
        doc.close()
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception:
        pass

    # 如果所有PDF库都失败，返回空字符串并提示用户
    print(f"  [WARN] Cannot read PDF text (no PDF library available): {pdf_path.name}")
    print(f"         Install one of: PyPDF2, pdfplumber, or pymupdf")
    return ""


# ============================================================
# 第三步：识别医院名称
# ============================================================

def detect_hospital_name(text: str) -> str:
    """
    从PDF文本中识别医院名称

    检测策略（按优先级）：
    1. 在报告标题中查找（如"XX医院体检报告"）
    2. 在表格字段中查找（如"医院名称：XX医院"）
    3. 在报告开头查找独立的医院名称

    参数：
        text: PDF文本内容

    返回：医院名称（如果识别失败，返回"Unknown_Hospital"）
    """
    patterns = [
        # 模式1: XX医院体检报告 / XX医院健康体检报告
        r'([\u4e00-\u9fa5]{2,20}(?:医院|体检中心|健康管理中心|卫生服务中心|医疗中心|卫生院))\s*(?:体检|健康体检|健康检查)',
        # 模式2: 体检机构/医院名称 header
        r'(?:体检机构|医院名称|体检单位|医疗机构)[：:\s]*([\u4e00-\u9fa5]{2,20}(?:医院|体检中心|健康管理中心|卫生服务中心|医疗中心|卫生院))',
        # 模式3: 报告顶部的独立医院名称
        r'^([\u4e00-\u9fa5]{2,20}(?:医院|体检中心|健康管理中心|医疗中心))\s*$',
    ]

    # 只检查前30行（医院名称通常在报告开头）
    lines = text.split("\n")
    first_30_lines = "\n".join(lines[:30])

    for pattern in patterns:
        match = re.search(pattern, first_30_lines, re.MULTILINE)
        if match:
            name = match.group(1).strip()
            if len(name) >= 4:
                return name

    # 后备方案：查找任何类似医院的名称
    fallback = re.search(
        r'([\u4e00-\u9fa5]{2,20}(?:医院|体检中心|健康管理中心|医疗中心))',
        first_30_lines
    )
    if fallback:
        return fallback.group(1).strip()

    return "Unknown_Hospital"


# ============================================================
# 第四步：提取患者基本信息
# ============================================================

def extract_patient_info(text: str) -> Dict[str, str]:
    """
    从PDF文本中提取患者基本信息

    提取的信息包括：
    - 姓名（姓名、受检者、被检人）
    - 性别（统一为"男"或"女"）
    - 年龄
    - 体检年份（从体检日期中提取）
    - ID（档案号、登记号、身份证号）

    参数：
        text: PDF文本内容

    返回：包含患者信息的字典
    """
    info = {}

    # 姓名
    name_patterns = [
        r'姓\s*名[：:]\s*([^\s\n\d]{2,4})',
        r'受检者[：:]\s*([^\s\n\d]{2,4})',
        r'被检人[：:]\s*([^\s\n\d]{2,4})',
        r'客户姓名[：:]\s*([^\s\n\d]{2,4})',
    ]
    for pat in name_patterns:
        m = re.search(pat, text)
        if m:
            name = m.group(1).strip()
            # 过滤非姓名文本
            name = re.sub(r'[^\u4e00-\u9fa5]', '', name)
            if 2 <= len(name) <= 4:
                info['sample_name'] = name
                break
    if 'sample_name' not in info:
        info['sample_name'] = 'Unknown'

    # 性别
    gender_pat = re.search(r'性\s*别[：:]\s*(男|女)', text)
    if gender_pat:
        info['sex'] = gender_pat.group(1)
    else:
        # 后备方案：在年龄附近查找独立的"男"或"女"
        gender_fallback = re.search(r'[男女]\s*[·•]?\s*\d{1,3}', text)
        if gender_fallback:
            info['sex'] = gender_fallback.group(0)[0]

    # 年龄
    age_pat = re.search(r'年\s*龄[：:]\s*(\d{1,3})', text)
    if age_pat:
        info['age'] = age_pat.group(1)
    else:
        age_fallback = re.search(r'[男女]\s*[·•]?\s*(\d{1,3})\s*岁', text)
        if age_fallback:
            info['age'] = age_fallback.group(1)

    # 体检年份（从体检日期中提取）
    year_patterns = [
        r'体检日期[：:]\s*(\d{4})',
        r'检查日期[：:]\s*(\d{4})',
        r'报告日期[：:]\s*(\d{4})',
        r'(\d{4})[-/年]\d{1,2}[-/月]\d{1,2}',  # 日期格式
    ]
    for pat in year_patterns:
        m = re.search(pat, text)
        if m:
            info['exam_year'] = m.group(1)
            break

    # ID（档案号/登记号/身份证号）
    id_patterns = [
        r'档案号[：:]\s*(\d{10,20})',
        r'登记号[：:]\s*(\d{10,20})',
        r'编号[：:]\s*(\d{10,20})',
        r'身份证号[：:]\s*(\d{15,18})',
        r'(\d{15,18})',  # 后备方案
    ]
    for pat in id_patterns:
        m = re.search(pat, text)
        if m:
            info['ID'] = m.group(1)
            break

    return info


# ============================================================
# 指标提取
# ============================================================

# 常见医学单位（按长度降序排列，用于贪婪匹配）
MEDICAL_UNITS = sorted([
    '10^9/L', '10^12/L', 'mmol/L', 'μmol/L', 'umol/L',
    'ml/min/1.73m^2', 'ml/min', 'mIU/L', 'ng/ml',
    'KU/L', 'U/L', 'g/L', 'mg/L', '次/分钟', '次/分',
    '/μL', 'mmHg', 'kg/m^2',
    'Kg', 'kg', 'Cm', 'cm', 'fL', 'fl', 'pg', '%',
    'mmol', 'BPM',
], key=len, reverse=True)


def _join_split_names(text: str) -> str:
    """预处理：拼接跨PDF行的指标名称

    模式：以中文结尾的名称行 + 数字行 + 中文尾部
    示例：
      丙氨酸氨基转移
      12.80 7-40 U/L
      酶
    变为：
      丙氨酸氨基转移酶 12.80 7-40 U/L

    也处理：名称 + 数字行，尾部字符在同一行：
      平均红细胞血红
      333.00 316-354 g/L
      蛋白浓度
    变为：
      平均红细胞血红蛋白浓度 333.00 316-354 g/L
    """
    lines = text.split('\n')
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # 只在以下情况拼接：行以中文结尾且不包含
        # a complete value+unit or value+ref pattern
        has_value = bool(re.search(r'\d+\.?\d*\s+(?:[a-zA-Z/%μ^²³]+|次/|[Uu]/[Ll]|mm[oO]l|kg|cm|mmHg)', line))
        has_ref_range = bool(re.search(r'(?<!\d{4})\d{1,3}\.?\d*\s*[－—\-~至到]+\s*\d+', line))

        if (re.search(r'[\u4e00-\u9fa5]$', line) and
            not re.search(r'\d+\s*$', line) and
            not has_value and
            not has_ref_range and
            i + 1 < len(lines)):

            next_line = lines[i + 1]
            # 下一行以数字开头（可能是数值）
            if re.match(r'^\s*\d+\.?\d*', next_line):
                # 检查第+2行是否存在且是短中文（指标名尾部）
                name_tail = ''
                if i + 2 < len(lines):
                    third = lines[i + 2].strip()
                    if (re.match(r'^[\u4e00-\u9fa5()（）\w]{1,10}$', third) and
                        not re.match(r'^\d', third)):
                        name_tail = third
                        i += 1  # consume the tail line

                # 拼接：名称行 + 名称尾部 + 空格 + 值行
                joined = line.rstrip() + name_tail + ' ' + next_line.strip()
                result.append(joined)
                i += 2  # consumed 3 lines (name, value, tail) or 2 (name, value)
                continue

        result.append(line)
        i += 1

    return '\n'.join(result)


def _second_pass_scan(text: str, template_canonical: set,
                      existing: Dict[str, Dict]) -> Dict[str, Dict]:
    """第二遍扫描：宽松扫描以捕获第一遍遗漏的指标

    当第一遍提取遗漏项目时使用。使用更宽松的模式：
    - 段落中的冒号格式：名称：值
    - 小结格式：小结：.*名称: 值
    - 行内名称-值：名称 值 单位（任何上下文）
    """
    new_results = {}

    # --- 模式A: 段落中的冒号格式（带单位）---
    # 匹配：丙氨酸氨基转移酶：76.10U/L, 低密度脂蛋白胆固醇：4.11mmol/L
    colon_with_unit = re.compile(
        r'([\u4e00-\u9fa5a-zA-Z()（）]{2,30})[：:]\s*(\d+\.?\d*)\s*([a-zA-Z/%μ^²³]+(?:/[a-zA-Z]+)?)'
    )
    for m in colon_with_unit.finditer(text):
        name = m.group(1).strip()
        value = m.group(2)
        unit = m.group(3)
        if name not in existing and name not in new_results:
            new_results[name] = {
                'value': value, 'unit': unit, 'original_name': name
            }

    # --- 模式B: 小结/列表格式 ---
    # 匹配：小结：红细胞分布宽度(SD): 48.40 fL
    #      1、锌: 7.80 μmol/L
    #      2、高密度脂蛋白胆固醇: 2.38 mmol/L
    summary_pat = re.compile(
        r'(?:\d+[、.]?\s*|、\s*|小结[：:]?\s*)'
        r'([\u4e00-\u9fa5a-zA-Z()（）（）]{2,30})[：:]\s*'
        r'(\d+\.?\d*)\s*([a-zA-Z/%μ^²³]+(?:/[a-zA-Z]+)?)?'
    )
    for m in summary_pat.finditer(text):
        name = m.group(1).strip()
        value = m.group(2)
        unit = m.group(3) or ''
        # 过滤非指标文本
        skip = ['过氧化氢', 'PH值', '白细胞酯酶', '阴道', '白带', '清洁度']
        if any(s in name for s in skip):
            continue
        if name not in existing and name not in new_results:
            new_results[name] = {
                'value': value, 'unit': unit, 'original_name': name
            }

    # --- 模式C: 名称-值-单位在同一行（值在参考范围后）---
    # 匹配：丙氨酸氨基转移酶 7-40 U/L 12.80
    broad_table = re.compile(
        r'([\u4e00-\u9fa5a-zA-Z()（）]{2,30})\s+'
        r'(?:[≤≥<>\d][\d.\-—~至到\s]*?)\s+'
        r'(' + '|'.join(re.escape(u) for u in MEDICAL_UNITS if len(u) >= 2) + r')\s+'
        r'(\d+\.?\d*)'
    )
    for m in broad_table.finditer(text):
        name = m.group(1).strip()
        unit = m.group(2)
        value = m.group(3)
        if name not in existing and name not in new_results:
            new_results[name] = {
                'value': value, 'unit': unit, 'original_name': name
            }

    # --- 模式C2: 名称 值 参考范围 单位（值在参考范围前）---
    # 匹配：丙氨酸氨基转移酶 12.80 7-40 U/L
    #      天门冬氨酸氨基转移酶 20.80 15-35 U/L
    #      低密度脂蛋白胆固醇 2.35 <3.37 mmol/L
    name_val_ref_unit = re.compile(
        r'([\u4e00-\u9fa5a-zA-Z()（）]{2,30})\s+'
        r'(\d+\.?\d*)\s+'
        r'(?:[≤≥<>\d][\d.\-—~至到\s]*?)\s+'
        r'(' + '|'.join(re.escape(u) for u in MEDICAL_UNITS if len(u) >= 2) + r')'
    )
    for m in name_val_ref_unit.finditer(text):
        name = m.group(1).strip()
        value = m.group(2)
        unit = m.group(3)
        if name not in existing and name not in new_results:
            new_results[name] = {
                'value': value, 'unit': unit, 'original_name': name
            }

    return new_results


def extract_indicators_from_text(text: str,
                                  template: List[Dict[str, str]] = None,
                                  synonym_map: Dict[str, str] = None) -> Dict[str, Dict]:
    """
    从PDF文本中提取所有可量化的医学指标（核心功能）

    这是整个脚本最核心的函数！使用多策略提取方法：

    策略0: 特殊处理血压（需要拆分为收缩压和舒张压）
    策略1: 括号格式 【指标名】值
    策略2: 表格格式（逐行解析）
    策略3: 冒号格式 名称：值
    第二遍: 宽松扫描（捕获遗漏项）
    第三遍: 断行拼接（处理PDF换行问题）

    参数：
        text: PDF文本内容
        template: 指标模板（用于匹配标准名称）
        synonym_map: 同义词映射（用于名称转换）

    返回：包含所有提取指标的字典 {指标名: {value, unit, original_name}}
    """
    results = {}

    # --- 策略0: 血压特殊处理 ---
    # 血压需要拆分为收缩压和舒张压两个指标
    bp_pat = re.compile(r'血压\s*[:：]?\s*(\d{2,3})/(\d{2,3})\s*(mmHg)?')
    for m in bp_pat.finditer(text):
        results['血压'] = {
            'value': f"{m.group(1)}/{m.group(2)}",
            'unit': 'mmHg',
            'original_name': '血压'
        }

    # --- 策略0b: 行内格式（名称 数值 单位）---
    # 匹配如: 白细胞计数 5.2 10^9/L
    inline_pat = re.compile(
        r'([^\s\n\d]{2,15})\s+(\d+\.?\d*)\s+(' + '|'.join(
            re.escape(u) for u in MEDICAL_UNITS if len(u) >= 2
        ) + r')'
    )
    for m in inline_pat.finditer(text):
        name = m.group(1).strip()
        value = m.group(2)
        unit = m.group(3)
        if name not in results:
            results[name] = {'value': value, 'unit': unit, 'original_name': name}

    # --- 策略1: 括号格式 【指标名】值...单位 ---
    # 匹配如: 【甘油三酯】1.74 mmol/L
    bracket_pat = re.compile(
        r'【\*?([^】\n]+)】\s*(\d+\.?\d*(?:/\d+\.?\d*)?)',
    )
    for m in bracket_pat.finditer(text):
        name = m.group(1).strip()
        value = m.group(2)
        rest = text[m.end():m.end() + 30]
        unit = _extract_unit(rest)
        results[name] = {'value': value, 'unit': unit, 'original_name': name}

    # --- 策略2: 表格格式（逐行解析）---
    # 这是最常用的格式，处理表格形式的数据
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if not line or len(line) < 5:
            continue

        skip_patterns = [
            r'^(项目|序号|检验项|检查项|报告|总结|建议|备注|注意|提示)',
            r'(项目名称|参考范围|参考值|单位|结果)$',
            r'^\d{4}[-/]\d{1,2}[-/]\d{1,2}',
        ]
        if any(re.search(p, line) for p in skip_patterns):
            continue

        unit_result = _find_unit(line)
        if unit_result:
            unit_name, unit_pos = unit_result
            before_unit = line[:unit_pos].strip()
            after_unit = line[unit_pos + len(unit_name):].strip()

            # 去除after_unit中的括号参考范围
            clean_after = re.sub(r'[（(][^）)]*[）)]', '', after_unit).strip()
            value = _extract_numeric_value(clean_after)
            # 如果clean_after为空或仅含参考范围，尝试before_unit（名称 值 参考格式）
            if not value and ' ' in before_unit:
                last_parts = before_unit.rsplit(' ', 2)
                if len(last_parts) >= 2:
                    value = _extract_numeric_value(last_parts[-1])
            if not value:
                continue

            name = _extract_name(before_unit)
            if name and len(name) >= 2 and name not in results:
                results[name] = {
                    'value': value, 'unit': unit_name, 'original_name': name
                }
        else:
            ref_match = re.search(
                r'(?<!\d{4})\d{1,3}\.?\d*\s*[－—\-~至到]{1,2}\s*\d+\.?\d*', line
            )
            if not ref_match:
                ref_match = re.search(
                    r'[≤≥<>\u2264\u2265=]+\s*\d+\.?\d*', line
                )
            if ref_match:
                before_ref = line[:ref_match.start()].strip()
                after_ref = line[ref_match.end():].strip()
                value = _extract_numeric_value(after_ref)
                name = _extract_name(before_ref)
                if name and value and len(name) >= 2 and name not in results:
                    results[name] = {
                        'value': value, 'unit': '', 'original_name': name
                    }

    # --- 策略3: 冒号格式 名称：值 ---
    colon_pat = re.compile(r'([^\s\n：:]{2,12})[：:]\s*(\d+\.?\d*)')
    exclude_kw = ['日期', '时间', '科室', '医生', '电话', '单位', '部门', '工号',
                  '结论', '次数', '页码', '编号', '登记号', '档案号']
    for m in colon_pat.finditer(text):
        name = m.group(1).strip()
        if any(kw in name for kw in exclude_kw):
            continue
        value = m.group(2)
        if name not in results:
            results[name] = {
                'value': value, 'unit': '', 'original_name': name
            }

    # --- 第二遍扫描：宽松扫描以捕获遗漏项 ---
    if template:
        template_canonical = {row['canonical_name'] for row in template}
    else:
        template_canonical = set()

    second_results = _second_pass_scan(text, template_canonical, results)
    # 只添加不在第一遍结果中的第二遍扫描项
    for k, v in second_results.items():
        if k not in results:
            results[k] = v

    # --- 第三遍扫描：拼接断行名称并重新扫描仍然缺失的项目 ---
    joined_text = _join_split_names(text)
    if joined_text != text:
        third_results = _second_pass_scan(joined_text, template_canonical, results)
        for k, v in third_results.items():
            if k not in results:
                results[k] = v

    return results


def _find_unit(line: str) -> Optional[Tuple[str, int]]:
    """
    在行中查找医学单位

    参数：
        line: 要搜索的文本行

    返回：(单位, 位置) 或 None
    """
    for unit in MEDICAL_UNITS:
        pos = line.find(unit)
        if pos >= 0:
            return (unit, pos)
    return None


def _extract_unit(text: str) -> str:
    """
    从值后的文本中提取单位

    参数：
        text: 值后面的文本

    返回：单位字符串
    """
    for unit in MEDICAL_UNITS:
        if unit in text[:20]:
            return unit
    return ''


def _extract_numeric_value(text: str) -> Optional[str]:
    """
    从文本中提取数值，处理各种格式

    参数：
        text: 要提取数值的文本

    返回：数值字符串或None
    """
    text = text.strip()

    # 血压：101/59 或 101/59mmHg
    bp_match = re.search(r'(\d+)/(\d+)\s*(?:mmHg)?', text)
    if bp_match:
        return f"{bp_match.group(1)}/{bp_match.group(2)}"

    # 常规数字（可能带标记符）
    num_match = re.search(r'(\d+\.?\d*)\s*[↑↓*]?\s*$', text)
    if num_match:
        return num_match.group(1)

    # 任意数字
    num_match = re.search(r'(\d+\.?\d*)', text)
    if num_match:
        return num_match.group(1)

    return None


def _extract_name(before_ref: str) -> Optional[str]:
    """
    提取项目名称，去除参考范围

    参数：
        before_ref: 参考范围前的文本

    返回：项目名称或None
    """
    cleaned = re.sub(r'^[【】\*\s]+|[【】\*\s:：]+$', '', before_ref.strip())

    # 在参考范围开始处分割
    split_pat = re.search(
        r'\s*(?:[：:]\s*\S+|[≤≥<>\u2264\u2265=]+\s*\d+|\d+\.?\d*\s*[－—\-~至到]+|[－—\-]+\s*$)',
        cleaned
    )
    if split_pat:
        name = cleaned[:split_pat.start()].strip()
    else:
        name = cleaned

    name = re.sub(r'[【】\*\s]+', '', name)
    return name if len(name) >= 1 and len(name) <= 20 else None


# ============================================================
# 名称映射（医院名称 → 标准名称）
# ============================================================

def load_synonym_map() -> Dict[str, str]:
    """
    从参考资料加载医学同义词映射

    返回：同义词映射字典
    """
    skill_dir = Path(__file__).parent.parent
    syn_path = skill_dir / "references" / "medical_synonyms.md"

    synonym_map = {}
    if not syn_path.exists():
        return synonym_map

    with open(syn_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析行格式："医院1, 医院2 → 标准名称"
    for line in content.split('\n'):
        line = line.strip()
        if not line.startswith('-') or '→' not in line:
            continue
        line = line.lstrip('- ').strip()
        parts = line.split('→')
        if len(parts) != 2:
            continue
        variants = [v.strip() for v in parts[0].split(',')]
        canonical = parts[1].strip()
        for v in variants:
            synonym_map[v] = canonical

    return synonym_map


def normalize_indicators(
    raw_indicators: Dict[str, Dict],
    template: List[Dict[str, str]],
    synonym_map: Dict[str, str],
) -> Tuple[Dict[str, Dict], Dict[str, str]]:
    """使用模板和同义词将原始PDF指标映射到标准名称

    返回：
        (标准化字典, 医院名称到标准名称的映射)
        normalized_dict: {canonical_name: {value, unit, original_name}}
        hospital_to_canonical_map: {hospital_name: canonical_name}
    """
    template_canonical_set = {row['canonical_name'] for row in template}
    official_feature_set = {row['official_feature_name'] for row in template}
    # 反向映射：official_feature_name → canonical_name
    feature_to_canonical = {row['official_feature_name']: row['canonical_name'] for row in template}
    normalized = {}
    hospital_to_canonical = {}

    # 标准化同义词映射：值可能是canonical_name或official_feature_name
    # 将所有同义词值转换为canonical_name
    normalized_synonyms = {}
    for variant, value in synonym_map.items():
        if value in template_canonical_set:
            normalized_synonyms[variant] = value
        elif value in official_feature_set:
            normalized_synonyms[variant] = feature_to_canonical[value]
    synonym_map = normalized_synonyms

    # 构建反向同义词映射：标准名 → [变体列表]
    canonical_to_variants: Dict[str, List[str]] = {}
    for variant, canonical in synonym_map.items():
        if canonical not in canonical_to_variants:
            canonical_to_variants[canonical] = []
        canonical_to_variants[canonical].append(variant)

    # 从模板构建标准名→英文名的查找表
    canonical_to_feature = {
        row['canonical_name']: row['official_feature_name']
        for row in template
    }

    # 特殊处理血压：拆分收缩压和舒张压
    bp_data = None
    for name, data in list(raw_indicators.items()):
        if '血压' in name and '/' in str(data.get('value', '')):
            bp_value = str(data['value'])
            parts = bp_value.split('/')
            if len(parts) == 2:
                try:
                    v1, v2 = float(parts[0]), float(parts[1])
                    systolic, diastolic = (v1, v2) if v1 > v2 else (v2, v1)
                    bp_data = {
                        'systolic_bp': {'value': str(int(systolic)), 'unit': 'mmHg', 'original_name': name},
                        'diastolic_bp': {'value': str(int(diastolic)), 'unit': 'mmHg', 'original_name': name},
                    }
                    # 收缩压和舒张压分别记录映射关系
                    hospital_to_canonical[name + '（收缩压）'] = 'SBP'
                    hospital_to_canonical[name + '（舒张压）'] = 'DBP'
                    del raw_indicators[name]
                except ValueError:
                    pass
                break

    # 映射每个原始指标（按official_feature_name存储，以兼容数据文件）
    for name, data in raw_indicators.items():
        canonical = None

        # 与canonical_name精确匹配
        if name in template_canonical_set:
            canonical = name
        # 通过同义词匹配
        elif name in synonym_map and synonym_map[name] in template_canonical_set:
            canonical = synonym_map[name]
        # 模糊匹配：名称包含标准名称
        else:
            for cn in sorted(template_canonical_set, key=len, reverse=True):
                if cn in name and len(cn) >= 3:
                    canonical = cn
                    break

        if canonical:
            feat_name = canonical_to_feature.get(canonical, canonical)
            if feat_name not in normalized:
                normalized[feat_name] = data
                if name != canonical:
                    hospital_to_canonical[name] = canonical

    # Add blood pressure data
    if bp_data:
        for feat_name, bp_info in bp_data.items():
            if feat_name not in normalized:
                normalized[feat_name] = bp_info

    return normalized, hospital_to_canonical


# ============================================================
# Output Generation
# ============================================================

def resolve_filename(output_dir: Path, base_name: str) -> Path:
    """
    解决文件名冲突：基础名 → 基础名2 → 基础名3 → ...

    参数：
        output_dir: 输出目录
        base_name: 基础文件名

    返回：可用的文件路径
    """
    name, ext = os.path.splitext(base_name)
    candidate = output_dir / base_name
    if not candidate.exists():
        return candidate

    counter = 2
    while True:
        candidate = output_dir / f"{name}{counter}{ext}"
        if not candidate.exists():
            return candidate
        counter += 1


def generate_mapping_file(
    hospital_name: str,
    mappings: Dict[str, str],  # hospital_name → canonical_name
    template: List[Dict[str, str]],
    output_dir: Path,
) -> Path:
    """
    生成医院的映射文件

    映射文件记录了医院实际使用的指标名称与标准名称的对应关系。
    例如：医院使用"丙氨酸氨基转移酶"，标准名称是"谷丙转氨酶"

    文件格式：
    hospital_name | canonical_name | official_feature_name | unit | reference | group
    丙氨酸氨基转移酶 | 谷丙转氨酶 | alanine_aminotransferase | U/L | 9--50 | 肝胆功能

    参数：
        hospital_name: 医院名称
        mappings: 医院名称→标准名称的映射字典
        template: 指标模板（包含所有标准指标定义）
        output_dir: 输出目录

    返回：生成的映射文件路径
    """
    filename = f"{hospital_name}mappings.csv"
    filepath = resolve_filename(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow([
            'hospital_name', 'canonical_name', 'official_feature_name',
            'official_unit', 'official_reference', 'official_group_zh'
        ])

        # 反向映射: 标准名称 → 医院名称
        canonical_to_hospital = {v: k for k, v in mappings.items()}

        # 按模板顺序写入每一行（确保顺序一致）
        for row in template:
            cn = row['canonical_name']
            if cn in canonical_to_hospital:
                hn = canonical_to_hospital[cn]
            else:
                hn = ''

            writer.writerow([
                hn,
                cn,
                row['official_feature_name'],
                row['official_unit'],
                row['official_reference'],
                row['official_group_zh'],
            ])

    return filepath


def generate_data_file(
    patients_data: List[Dict[str, Dict]],
    template: List[Dict[str, str]],
    output_dir: Path,
    batch_size: int,
) -> Path:
    """
    生成数据文件（包含所有患者的指标数据）

    数据文件格式：
    第1行：表头（按模板顺序排列的标准英文名称）
    第2行：患者1的数据
    第3行：患者2的数据
    ...

    文件名示例：26,07,22 14:30[3].csv（2026年7月22日14:30处理了3份报告）

    参数：
        patients_data: 所有患者的数据列表
        template: 指标模板（用于确定列顺序）
        output_dir: 输出目录
        batch_size: 本批处理的PDF数量

    返回：生成的数据文件路径
    """
    now = datetime.now()
    base_name = f"{str(now.year)[-2:]},{now.month:02d},{now.day:02d} {now.hour:02d}：{now.minute:02d}[{batch_size}].csv"
    filepath = resolve_filename(output_dir, base_name)

    # 从模板获取指标顺序（确保列顺序一致）
    feature_order = [row['official_feature_name'] for row in template]

    with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        # 写入表头
        writer.writerow(feature_order)

        # 写入每个患者的数据
        for patient in patients_data:
            row_data = []
            for feat in feature_order:
                if feat in patient:
                    val = patient[feat].get('value', '')
                    row_data.append(str(val))
                else:
                    row_data.append('')  # 缺失值用空字符串表示
            writer.writerow(row_data)

    return filepath


# ============================================================
# 主处理流程
# ============================================================

def main():
    """
    主函数：协调整个处理流程

    处理步骤：
    1. 解析命令行参数
    2. 收集PDF文件
    3. 加载模板和同义词
    4. 逐个处理PDF：
       a. 读取PDF文本
       b. 识别医院名称
       c. 提取患者信息
       d. 提取医学指标
    5. 生成输出文件：
       a. 映射文件（每家医院一份）
       b. 数据文件（所有患者一份）
    """
    parser = argparse.ArgumentParser(
        description='Medical Report Processor — Process PDF exam reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python process.py report.pdf --both
  python process.py report1.pdf report2.pdf --mapping
  python process.py ./reports/ --data
        """
    )
    parser.add_argument('paths', nargs='+', help='PDF file paths or directory paths')
    parser.add_argument('--mapping', action='store_true', help='Output mapping file(s) only')
    parser.add_argument('--data', action='store_true', help='Output data file only')
    parser.add_argument('--both', action='store_true', help='Output both mapping and data files')

    args = parser.parse_args()

    # Determine output mode
    if args.both or (args.mapping and args.data):
        output_mode = 'both'
    elif args.mapping:
        output_mode = 'mapping'
    elif args.data:
        output_mode = 'data'
    else:
        output_mode = 'both'

    # Collect PDFs
    pdf_files = collect_pdf_files(args.paths)
    if not pdf_files:
        print("ERROR: No PDF files found.")
        sys.exit(1)

    print(f"Found {len(pdf_files)} PDF file(s)")
    print(f"Output mode: {output_mode}")
    print(f"{'='*50}")

    # Load template
    template = load_mappings_template()
    synonym_map = load_synonym_map()

    # Output directory = first PDF's folder
    output_dir = pdf_files[0].parent

    # Process each PDF
    hospital_data: Dict[str, List[Tuple[str, Dict[str, Dict]]]] = {}
    all_patients_normalized = []

    for i, pdf_path in enumerate(pdf_files):
        print(f"\n[{i+1}/{len(pdf_files)}] Processing: {pdf_path.name}")

        # Read PDF
        text = read_pdf_text(pdf_path)
        if not text or len(text.strip()) < 50:
            print(f"  [SKIP] Insufficient text content")
            continue

        # Detect hospital
        hospital = detect_hospital_name(text)
        print(f"  Hospital: {hospital}")

        # Extract patient info
        patient_info = extract_patient_info(text)
        print(f"  Patient: {patient_info.get('sample_name', '?')} | "
              f"{patient_info.get('sex', '?')} | "
              f"{patient_info.get('age', '?')}y")

        # Extract indicators
        raw_indicators = extract_indicators_from_text(text, template, synonym_map)
        print(f"  Raw indicators extracted: {len(raw_indicators)}")

        normalized, h2c = normalize_indicators(raw_indicators, template, synonym_map)

        # Merge patient info into normalized
        for key, value in patient_info.items():
            if key in {row['canonical_name'] for row in template}:
                normalized[key] = {
                    'value': value,
                    'unit': '',
                    'original_name': key
                }

        print(f"  Mapped indicators: {len(normalized)}")

        # Store by hospital
        if hospital not in hospital_data:
            hospital_data[hospital] = []
        hospital_data[hospital].append((pdf_path.name, normalized))

        all_patients_normalized.append(normalized)

    if not all_patients_normalized:
        print("\nERROR: No reports successfully processed.")
        sys.exit(1)

    # --- Generate outputs ---
    print(f"\n{'='*50}")
    print(f"Output directory: {output_dir}")

    # Mapping files
    mapping_paths = []
    if output_mode in ('mapping', 'both'):
        print("\n--- Mapping Files ---")
        for hospital, patients_list in hospital_data.items():
            # Build combined mapping for this hospital (union of all patients)
            combined_h2c = {}
            for _, normalized in patients_list:
                for feat_name, data in normalized.items():
                    original = data.get('original_name', feat_name)
                    if original != feat_name:
                        combined_h2c[original] = feat_name

            path = generate_mapping_file(hospital, combined_h2c, template, output_dir)
            mapping_paths.append(path)
            print(f"  ✓ {path.name}")

    # Data file
    data_path = None
    if output_mode in ('data', 'both'):
        print("\n--- Data File ---")
        data_path = generate_data_file(
            all_patients_normalized, template, output_dir, len(pdf_files)
        )
        print(f"  ✓ {data_path.name}")

    print(f"\n{'='*50}")
    print(f"COMPLETE: {len(all_patients_normalized)} patient(s) processed")

    # Return paths for caller
    return {
        'mapping_paths': mapping_paths,
        'data_path': data_path,
        'output_dir': str(output_dir),
    }


if __name__ == "__main__":
    main()
