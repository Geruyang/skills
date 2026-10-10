# 挑战者相机、USB 与调试证据

EBVC 的实物为挑战者 V1：CAM_RESET 由匹配原理图核实为 PG2；原生 USB 设备口是底板 J38，PB14/PB15。相机 CDC 与 fireDAP 虚拟串口是不同设备；历史 COM5/COM3 仅是该机器当时的枚举结果，重新按 PnP 身份确认。

USB 与以太网可能是两条必须保留的产品路径。默认关闭 Ethernet 不等于允许删掉 RMII、PHY、lwIP 与 HTTP；修改前检查用户保留要求和管脚/缓冲互斥条件。

fireDAP 应走 CMSIS-DAP/OpenOCD，不能当作 SEGGER J-Link 使用。独立 DC 供电且原装 DAP 未改装时，VREF 是参考输入；不要仅因线名 3V3 推断它在向板卡供电。USB Hub 的 overcurrent 状态码不是实际电流读数；已完成的拔线/重启检查不应无新证据反复要求。

SWD“读内存”工具的初始化脚本可能写 DBGMCU 或配置调试子系统，应核查 init/reset event，不能泛称完全只读。烧录旧未知程序前的备份单独保存；后续明确授权的同一烧录流程不重复索要授权。

RAM 解码绑定实际下载的 HEX、AXF、map 和由该 AXF 导出的 layout。即使修改仅限 UI，也可能移动全局符号。新镜像重新提取地址，不复用旧帧结构大小。Keil 构建、program、verify、reset、健康采样与真实手势验收分别记录。

有限采样报告窗口长度、新增完整记录数、CRC/拒收/丢弃增量与累计值。相机帧率、Vision 吞吐、preview_confirmed 和 LCD 提交分别解释；静态阅读器画面无提交增长不自动等于显示故障，也不能用提交增长代替视觉验收。

来源：EBVC Docs/usb-firedap-20260917.md、Docs/agent-team/round5-summary.md、Docs/reader-selection-20260922.md，及“上板开发2”用户纠正。不得把该项目的端口号、阈值或授权带到新设备。
