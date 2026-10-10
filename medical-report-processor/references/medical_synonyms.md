# Medical Synonyms Reference

Extensible knowledge base for mapping hospital examination item names to standard canonical names.
Add new synonym entries as new hospital report patterns are discovered.

**Format**: `hospital_variant_1, hospital_variant_2 → canonical_name`

**Important**: This is a supplementary reference. The AI should use medical reasoning as the primary matching strategy, falling back to this list when needed. Never treat this list as exhaustive or authoritative.

---

## 基础信息 (Basic Info)

- 姓名, 受检者, 被检人, 体检人, 客户姓名 → sample_name
- 性别, 本人性别 → sex
- 年龄, 周岁, 实足年龄 → age
- 体检编号, 档案号, 登记号, 编号, 条码号, 身份证号 → ID
- 体检日期, 检查日期, 报告日期, 采样日期 → exam_year

---

## 脂肪/肥胖 (Obesity)

- 体重指数, 体质指数, BMI, 身体质量指数 → bmi
- 腰围, 腹围 → waist_circumference

---

## 血流动力学 (Hemodynamics)

- 收缩压, 高压, SBP → systolic_bp
- 舒张压, 低压, DBP → diastolic_bp
- 脉搏, 脉率, 脉搏数, 心率 → pulse

---

## 免疫/炎症 (Immunology/Inflammation)

- 白细胞计数, 白细胞, 白细胞数, WBC → white_blood_cell_count
- 中性粒细胞百分比, 中性粒细胞百分率, 中性粒细胞百分数, 中性粒细胞%, NEUT% → neutrophil_percentage
- 中性粒细胞计数, 中性粒细胞绝对值, 中性粒细胞#, NEUT# → neutrophil_count
- 单核细胞百分比, 单核细胞百分率, 单核细胞百分数, 单核细胞%, MONO% → monocyte_percentage
- 单核细胞计数, 单核细胞绝对值, 单核细胞#, MONO# → monocyte_count
- 嗜酸性粒细胞百分比, 嗜酸性粒细胞百分率, 嗜酸性粒细胞百分数, 嗜酸性粒细胞%, EO% → eosinophil_percentage
- 嗜酸性粒细胞计数, 嗜酸性粒细胞绝对值, 嗜酸性粒细胞#, EO# → eosinophil_count
- 嗜碱性粒细胞百分比, 嗜碱性粒细胞百分率, 嗜碱细胞百分比, 嗜碱性粒细胞百分数, 嗜碱性粒细胞%, BASO% → basophil_percentage
- 嗜碱性粒细胞计数, 嗜碱性粒细胞绝对值, 嗜碱细胞绝对值, 嗜碱性粒细胞#, BASO# → basophil_count
- 淋巴细胞百分比, 淋巴细胞百分率, 淋巴细胞百分数, 淋巴细胞%, LYMPH% → lymphocyte_percentage
- 淋巴细胞计数, 淋巴细胞绝对值, 淋巴细胞#, LYMPH# → lymphocyte_count

---

## 红细胞指标 (Red Blood Cell)

- 血红蛋白, 血红蛋白浓度, 血色素, Hb, HGB → hemoglobin
- 红细胞平均体积, 平均红细胞体积, MCV → mean_corpuscular_volume
- 红细胞计数, 红细胞[血], 红细胞数, RBC → red_blood_cell_count
- 平均红细胞血红蛋白含量, 平均血红蛋白含量, 平均血红蛋白量, MCH → mean_corpuscular_hemoglobin
- 平均红细胞血红蛋白浓度, 平均血红蛋白浓度, MCHC → mean_corpuscular_hemoglobin_concentration
- 红细胞压积, 血细胞比容, 红细胞比积, HCT, Ht → hematocrit
- 红细胞体积分布宽度, 红细胞分布宽度, 红细胞分布宽度(SD), 红细胞分布宽度SD, RDW, RDW-CV, RDW-SD → red_cell_distribution_width

---

## 止血/凝血 (Hemostasis)

- 血小板计数, 血小板, 血小板数, PLT → platelet_count

---

## 尿沉渣 (Urine Sediment)

- 白细胞[尿], 尿白细胞, 尿液白细胞, 尿WBC → urine_white_blood_cells
- 上皮细胞[尿], 尿上皮细胞, 尿液上皮细胞 → urine_epithelial_cells
- 细菌, 尿细菌, 尿液细菌 → urine_bacteria
- 红细胞[尿], 尿红细胞, 尿液红细胞, 尿RBC → urine_red_blood_cells

---

## 尿液化学 (Urine Chemistry)

- 尿酸碱度, 尿液pH, 尿pH值, pH → urine_ph

---

## 肝胆功能 (Hepatobiliary)

- 谷丙转氨酶, 丙氨酸氨基转移酶, ALT, GPT → alanine_aminotransferase
- 谷草转氨酶, 天门冬氨酸氨基转移酶, AST, GOT → aspartate_aminotransferase
- 总胆红素, TBIL, TB → total_bilirubin
- 直接胆红素, 结合胆红素, DBIL, DB → direct_bilirubin
- γ-谷氨酰转移酶, γ-谷氨酰基转移酶, γ-GT, GGT → gamma_glutamyl_transferase
- 碱性磷酸酶, ALP, AKP → alkaline_phosphatase

---

## 肝合成功能 (Liver Synthesis)

- 总蛋白, TP → total_protein
- 白蛋白, 清蛋白, ALB → albumin
- 球蛋白, GLB, GLO → globulin

---

## 肾功能 (Renal Function)

- 尿素, 尿素氮, BUN, UREA → urea
- 肌酐, 血肌酐, Cr, CREA → creatinine

---

## 脂质代谢 (Lipid Metabolism)

- 总胆固醇, 胆固醇, TC, CHOL → total_cholesterol
- 甘油三酯, TG, TRIG → triglycerides
- L-胆固醇, 低密度脂蛋白胆固醇, LDL-C, LDL → ldl_cholesterol
- H-胆固醇, 高密度脂蛋白胆固醇, HDL-C, HDL → hdl_cholesterol

---

## 糖代谢 (Glucose Metabolism)

- 葡萄糖, 血糖, GLU, BS, 空腹血糖 → glucose
- 糖化血红蛋白, 糖基化血红蛋白, HbA1c, HbA1C, GHb → glycated_hemoglobin

---

## 嘌呤代谢 (Purine Metabolism)

- 尿酸, UA, URIC → uric_acid
