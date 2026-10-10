# FZ3B：已验证平台上的PS应用接续

本参考只描述本用户`E:/AIProject/FPGAVibecoding`，不是所有FZ3B镜像的默认配置。状态截至2026-10-09；新会话先查活状态。完整入口：

- [PS应用交接](E:/AIProject/FPGAVibecoding/docs/handoffs/2026-10-09-ps-application-development-handoff.md)
- [开发复盘](E:/AIProject/FPGAVibecoding/docs/analysis/2026-10-09-project-development-retrospective.md)及[错误台账](E:/AIProject/FPGAVibecoding/docs/analysis/2026-10-09-errors-and-solutions.md)
- [PS加载/重启验证](E:/AIProject/FPGAVibecoding/docs/handoffs/2026-10-09-ps-fpga-loader-autostart.md)

## 先定位当前版本

正式V10.5/A0005已完成完整RTL、实现、四profile实板、完整模型流水测试。core465A5641、ABI000A0005、capsFFF、UAPI10，设备`/dev/network10_v10_signed40`。CPU约1.0667GHz、PL1输入100MHz、job/PW200/400MHz。CPU1.2GHz曾A/B通过但已恢复；全宽200MHz停止；不要把旧候选当当前版本。

最近100对/200帧4.043501591FPS，历史同配置4.097891941FPS。两张固定tensor重复执行，包含流水填排与结果收集，排除setup、相机、JPEG、预处理和显示，不能称自然样本准确率或相机FPS。普通PS应用以当前bit不变为默认边界；硬件需求改变才另开设计工作。

| 内容 | 主机/板端入口 |
|---|---|
| 主机当前闭包 | `releases/current/hardware/`、`ps/`、`pl-loader-a0005-002/`、`model-source/`、`tools/` |
| 板端模型/runner/native/inputs | `/root/network10-v10.5-a0005-retained-current` |
| 板端runtime/validation | `/root/workspace/network10-v10.5-a0005-board-validation-001` |
| 板端加载器 | `/root/workspace/network10-v10.5-pl-loader/fz3b_pl_loader.py` |
| 原厂备份 | `/root/workspace/factory-backups/network10-factory-20261009-a0005-retained`及主机`releases/factory/` |
| SSH工具 | `releases/current/tools/fz3b-ssh-python.ps1`及自包含`python312-ssh-deps` |

板Ubuntu18.04/Python3.6.9/内核4.14/ORT1.16.3；主机PyTorch应用Python≥3.10，不能直接把host包安装板端。models manifest的ORT1.20.1是主机拆分环境。runtime-current和runtime-compat都需在搜索路径。旧名ORT实体/兼容链及lease KO仍被使用，日期旧不代表可删。内核编译树已离板备份；日常应用不需恢复。

## 加载器与会话生命周期

用既有SSH通道确认`loader status`、service active/enabled、manager operating、正确身份和无owner；不输出凭据。网口历史192.168.1.254，仍需核实际接口。不要因主机沙箱拒绝连接就判定板端断网。

`fz3b-pl-loader.service`在rc-local和workspace挂载后加载A5，daemon持续持有IOPLL lease FD。受控Linux重启及A5→factory→A5、busy拒绝已实测；新的实际断电复验仍未做。BOOT.BIN/image.ub未改。旧SIGSTOP-holder、PID与冻结README的manual-gate描述已被新资格回执覆盖。

```sh
python3 -B /root/workspace/network10-v10.5-pl-loader/fz3b_pl_loader.py status
# 前一会话已正常退出、设备空闲时，准备新的驱动生命周期：
python3 -B /root/workspace/network10-v10.5-pl-loader/fz3b_pl_loader.py prepare-a0005
```

同A5的prepare刷新驱动和身份，不重写位流；忙时不破坏当前作业。runtime用上下文或显式close，退出迭代也排空、QUIESCE/FREE/close。terminal-quiesce后下一会话需prepare，不重复打开退休端点。应用不直接rmmod、去overlay、kill持clock的daemon或强写时钟。

用户当前要求保留A5；只有明确恢复/切换任务才`switch-factory`。临时切factory不改下次启动默认A5；永久恢复需正常切换后再禁用自定义service。先前临时往返确认不等于以后每测完恢复的授权。

## 实际计算链与API

```text
RGB官方Resize/CenterCrop256 → FP32 NCHW[1,3,256,256]
→ PS stem[1,64,64,64]
→ INT16 HCW → PL P2/N0 → P3/N1 → P0/N2
→ FP32[1,128,32,32] → PS N3[1,256,16,16]
→ INT16 HCW → PL P1/N4 → FP32[1,256,16,16]
→ PS suffix11 → raw FP32[512] → L2归一化与语义/图库匹配
```

正式组装在`releases/current/ps/runtime-current/benchmark_cnn_pipeline_v10_live.py`：`build_v10_mixed_components()`、`LinuxIoctlV10Signed40CandidateTransport`及`V10Signed40ChainMixin + V10MixedBoundaryMixin + V10SplitPsLiveRuntime`。还没有单一正式应用工厂；抽现有组装，不重写驱动协议。

流式适配点`V10LiveRuntime.iter_results(items,max_in_flight=1..4,record_history=False)`：输入`(frame_id,tensor)`，非负严格递增ID、有限连续FP32指定形状；输出独立512维特征、frame_id、timing/completions。两lane一对、最多4对；PS_FRONT、PL、PS_SUFFIX各单owner，跨对重叠并按序交付。P2→P3→P0不可被其他批插入；奇数尾shadow不计真实FPS。

官方预处理RGB、短边256双线性/antialias、CenterCrop256、ToTensor[0,1]，没有通用CLIP mean/std。量化保持FP64除scale、ties-even、INT16饱和、CHW→HCW与小端；scale读当前manifest。native转换直接写WC DDR，正式`direct_wc`。cached DMA候选因板provider无安全同步回收未启用，不强开`allow_global_zynqmp_memcpy`。

signed40仅normal P0/P1/P2的PW2累加/FIFO，激活仍INT16，P3敏感宽度保留。suffix11是6Conv+5MatMul W8A8 QDQ，余部FP32，不是全图整数。ShmOrtPartitionClient用64B ORTSHM3头+mmap、继承FD和小pipe控制；输入和独立输出仍有复制，不称完整零复制。

## 应用缺口与优先级

1. 抽应用会话工厂，封装prepare/close/身份及增量结果；同批实现接收已有feature的matcher/缓存兼容合同，固定tensor与旧benchmark对照。host现CLI重新编码图片，不能直接当板端feature输入API。
2. 当前保留树没有已生成的text-cache/gallery NPZ，板包没有text encoder；在主机预计算文本，提供板Python3.6轻量reader，并绑定源模型/预处理与有效量化后端身份。512维相同不够；按文字prompt分类不是OCR。
3. 再接UVC采集→BGR转RGB/官方预处理→有界队列，只解拟推理帧。CM717旧2K四线程25FPS占约3.6核；旧本机相机/USB串口artifact已删除，板端旧目录未重查，先核并纳管源码，不存在则按历史协议重实现。
4. 再按用户应用目标实现unknown、去抖、显示/HTTP/网络结果与健康监控。自然物品/角度样本、长时间端到端、断电和热稳定性另验。

最新平均PS stem/N3/suffix调用146.383/43.223/238.836ms每张；PL P2/P3/P0/P1硬件41.270/7.789/99.914/172.072ms每对。suffix owner约478ms/对当前最忙，流水吞吐不能通过相加owner墙钟计算。多在途提高吞吐也加排队，比较1/2/4对的端到端时延。

修改前读新交接再查旧文档；冻结payload不原地改历史资格。详细SHA、目录和恢复方法以当前清单/资格回执为准。
