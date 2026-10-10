# FZ3B开发中的可复用调试经验

更新2026-10-09。来源为本项目实测和失败复盘；每项按所述内核/工具/接口范围使用，不扩展为所有平台规则。详见[错误台账](E:/AIProject/FPGAVibecoding/docs/analysis/2026-10-09-errors-and-solutions.md)。关键词：DMA、QUIESCE、self-pin、clock lease、PCAP、bank、PREG、FIFO、route、计时、备份。

## 接口、驱动与生命周期

- 检查真实BD接线和极性，官方reset辅助输入曾接错低有效。TKEEP/TSTRB只能比较同一接口同一拍；跨FIFO比较首拍会假报尾包错误。完整包、非整拍尾、强反压和计数平衡都要验证。
- 重绑驱动时硬件计数可能非零，以读回值建立基线；profile切换排空/复位合同与同profile快速路径分别验证。leaf/ILA前缀正确不证明整帧完整。
- Linux DMA API的coherent分配不表示HP0缓存一致；不虚标dma-coherent。NumPy/mmap虚拟地址不能当bus地址。用户源页固定、SG映射、统一deadline、同步完成后发布有效性、异常隔离及回收能力是同一合同。
- 本板4.14 memcpy provider缺device_synchronize时，cached DMA候选无法安全收尾，正式保持direct_wc；只在补齐provider/回收证明后重新评估，不能绕过或用CPU重放伪装DMA。
- 当前probe自引用ref1与terminal-quiesce后的ref0都是有意义状态。先排空正常QUIESCE再卸载；已终态ref0不重新打开退休端点。禁止强制rmmod或释放未知在途缓冲。
- `/proc/PID/fd/N`重新open设备不是dup旧FD，可能EBUSY。持时钟lease服务失败时按对应driver的quarantine/recovery/FINALIZE合同和真实寄存器恢复，不默认ptrace/注入/kill释放保护。
- core ABI、UAPI、参数manifest、descriptor arena和设备路径分别绑定；基类硬编码旧设备、漏P3参数相对路径和误称旧ABI都曾导致集成失败。发布完整闭包和兼容依赖，不只上传一个新Python。

## 时钟与PS加载

- `clk_set_rate`返回0和cpufreq sysfs不是实频证据。CPU1.2GHz实验通过PM父/divider、raw寄存器和guard FD核实，切到已有DPLL才生效；实验后恢复。未知PS PLL/MIO/DDR时钟不能猜值强写。
- AIB/PM权限或ACK不满足时停止该候选；本项目PL0失败后采用已验证空闲PL1并持续保持IOPLL引用。区分CRF/CRL不同PLL_STATUS地址。重启后旧PID/lease失效，需要fresh状态。
- 方法名“register_access”不保证只读，API可能写回多字payload。曾因只分配1个u32而实际写5个导致Oops；核源码/完整结构、缓冲大小和canary再调用。
- 本板FPGA Manager 4.14直接memcpy载荷，无字节序自动转换。Vivado native bin与Linux/PCAP文件逐32位字节序不同；A5用官方Bootgen从同bit导出，核大小/SHA及offset80同步字。该offset只适用于本冻结格式，不能推广所有文件。
- Linux开机service加载≠修改BOOT.BIN。顺序After不拉入依赖，需要对应Wants与挂载依赖；daemon终身flock、root socket、请求deadline、busy拒绝及目标幂等可避免多控制者切换。受控重启和实际断电验证分别记录。

## 数值、存储与流水

- 硬件逐码一致与整模型特征/排序质量是两道门。V4低精度结构正确但质量失败，后来改宽位数；suffix候选需在真实PL输出域测试。无损GELU表压缩保留全部舍入/饱和结果，不用提前截断省位数。
- normal PW2 signed40缩窄通过`abs(bias)+32768*sum(abs(weight))`逐输出通道证明，覆盖任意INT16输入及累加前缀；只对绑定权重有效。P3敏感48位不套用normal证明。
- 共享所有DW/PW乘法器曾极大降低资源却慢约22倍：PW算力缩减、权重复读、小写逐次等待、halo重复、流水填排叠加。衡量峰值算力、权重/激活流量和调度开销，再谈多核；不能把核数乘以单核FPS。
- DW7动态bank选择曾令每拍接入变为每3拍接入；固定物理bank访问再重排、共享唯一MAC调用点，可减少选择与重复综合。PW1相邻逻辑bank合并为真双口物理bank需同时证明访问冲突和输出时序。
- 用英文bank；解释II=1为“每拍可接入一组新计算，前组不必完成”，不等于一拍完成整组或整图。寄存器级数可改善时序，但leaf固定可见延迟改变会破坏上层合同。
- DDR级间ring不一定省LUT或提速：本项目q3/q7/expanded恢复片上FIFO并把客户端5真正缩回2后更划算；仅关mask仍保留仲裁不是结构精简。保留长残差DDR环/块间区，按BRAM预算和反压验证选深度。
- 先填完整32拍再发命令的写协议、可容纳完整响应的读协议，不能只把FIFO32改成8/16；可能在提交前死锁。PW2结果FIFO缩深度也需整核反压/收支排空证明。
- HLS逻辑bit压缩不保证实际BRAM下降；同阶段比较HLS/OOC/平台综合/route资源。DDR预留区总量不等实际使用，高地址可能需40位；不能凭“板上4GB”重划System RAM。

## 综合、实现与工具错误

- 正pre-route WNS、单leaf400MHz或OOC180MHz均不等完整平台签核；检查setup/hold/pulse、实际相关时钟、route状态、DRC及check_timing。用户要求低成功率候选先优化时，按拥塞/路径证据停止长route，不把主观估计写成确定概率。
- DSP融合需验证工具没有移除关键PREG。本项目定向保护stage3、opt/postphys核128/128；全层盲DONT_TOUCH或额外输出寄存器可能改延迟或恶化布线。
- Windows旧长路径可用项目内短构建路径，冻结source/rebuild映射；仿真每用例私有snapshot防共享文件竞争。调用官方受支持Tcl/工具入口，不猜不存在命令。
- xsim RC0不是TB PASS；检查向量数、watchdog、协议、错误标记与证据摘要，digest包括实际编译`.vh`等头。故障注入验证拒绝路径有价值，纯词句匹配测试没有。
- 已保存routed DCP后收尾解析失败，先只读重开并核fully-routed==routable、errors0，不重复route。完全布通报告可省略unrouted行。日志刚关闭的文件锁/SHA竞态保留原FAIL，待释放后派生回执，不能篡改原证据。
- 后台运行、日志记录和进程错误收集减少弹窗干扰。线程/内存按用户当次安排和工具实际允许值设置；不把短期“忽略阈值”固化为常规。Windows中文工具用`python -X utf8`，YAML分隔符必须原始`---`，不能转义成`\---`。

## 性能与清理交接

- 标明tensor→feature/采集/解码/显示、warmup/setup/fill/drain、独立输入数、线程/clock及结果交付。四profile执行不等四张图，唯一frame ID不等唯一样本。owner忙时、CPU利用率、单帧排队延迟与FPS分开。
- ARM四核各ORT session的spinning、预分配和线程数必须整流水实测；本项目front1/suffix3、spin/prealloc0胜出，不能泛化为所有模型最佳。共享mmap仍有输入/输出生命周期复制，不称全零复制。
- 相机四线程解码占3.6核，不能与推理3线程叠加期待两者最高FPS。最新帧队列/只解拟推理帧/较低分辨率是应用候选，保持官方预处理后实测。
- 清理前查真实依赖、分区容量、旧名软链和frozen manifest。`/root/workspace`独立小分区；先迁依赖和验证，不能只看目录日期。未知对象按用户要求确认，历史日志不作为当前程序必需依赖。
- 内核原始tar不含全部已配置环境；完整树备份含内容、权限、属主、时间及软链，双端验证后删除。当前已配置树在host，日常PS应用不需恢复；原厂系统/PL/KO与恢复说明保持。
- 项目长历史与删除后的路径留文档，新交接指current闭包和资格回执。旧manifest内容真实性与最新状态分开；追加证据，不原地改冻结payload。
