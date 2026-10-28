# 采购清单：3D 打印耗材 / Robotiq 夹爪线材 / ZED 相机线材

**定稿：2026-10-28。** 以下面的「一页总览」为准；后面各章是选型过程和背景资料，里面早期的方案（CRX、外接 RS485 长线、PCIe 卡等）已被总览取代。纯文本版：[`purchase_list_zh.txt`](purchase_list_zh.txt)。下单前以官网页面为准。

## 一页总览（最终版：UR5e + ZED Box + H2D Pro + A250T）

### 要买的

| # | 用在哪 | 品名 | 型号 / 料号 | 数量 |
|---|---|---|---|---|
| 1 | H2D Pro | Bambu PAHT-CF（黑，1 kg，带料盘） | — | 1 |
| 2 | H2D Pro | Bambu Support for PA/PET（绿，0.5 kg） | S03-G1-1.75-500-SPL | 1 |
| 3 | H2D Pro + A250T | Bambu PLA-CF（1 kg，带料盘） | — | 2（两台各一卷） |
| 4 | H2D Pro | 胶棒（PAHT-CF 要涂胶） | Bambu 原装胶棒 | 1 |
| 5 | A250T | Snapmaker 双头打印模块 | SNM-23440 | 1 |
| 6 | A250T | 双头模块用 0.4 mm 硬化钢热端 | SNM-23445 | 1–2 |
| 7 | A250T | Bambu PETG-CF（1 kg，带料盘） | — | 1 |
| 8 | A250T | Bambu Support for PLA/PETG（0.5 kg） | S05-C0-1.75-500-SPL | 1 |
| 9 | ZED X Mini | GMSL2 Fakra 延长线 5 m（公-母，接原配短线） | CBL-310200 | 1 |
| 10 | ZED 2i | 螺丝锁 USB 3.0 Type-C 线 | 不用买（原配 4 m 够用；装得远再买 10 m CBL-221500） | 0 |
| 11 | 网络 | Cat6 网线（PC↔ZED Box、PC↔UR 控制柜） | 按距离，一般 5–10 m | 2 |
| 12 | 网络 | 5 口千兆交换机（PC 只有一个网口时） | 例：TP-Link TL-SG105 | 1 |
| 13 | 备用：ZED 2i 直连 PC 10 m | Stereolabs 10 m 双螺丝锁 USB 3.0 Type-C 线 | CBL-221500 | 1 |
| 14 | 备用：USB Hub | StarTech 工业级 4 口 USB 3.0 Hub（每口 ESD 防护，7–24 V 端子供电，附日本插头适配器） | ST4300USBM | 1 |

> 备用方案说明：ZED 2i 要直连 PC 且距离到 10 m 时，首选官方 10 m 线 CBL-221500，直插 PC 的 USB 3 口，图像和 IMU 都没问题。相机尽量不要走 Hub；Hub 留给键盘、鼠标、U 盘、调试设备用。如果一定要相机走 Hub，只接这一台相机，并且给 Hub 接上外部电源。
> 另一种省事的选择是 StarTech U01043（10 m 有源延长线，末端自带 4 口 Hub，有 ESD 防护，附 20 W 电源），一根线同时解决距离和备用口，但 Stereolabs 没有测试过它，到货后要先测 IMU 能不能读到。

### 不用买（已有或方案变了）

- Bambu AMS HT：H2D Pro 套装自带。
- Robotiq 转接口：现有的 M8 e-Series 转接口能直接插 UR5e 手腕。
- Robotiq 10 m 线、USB 转 RS485、24 V 电源、保险丝：夹爪走 UR5e 手腕内部供电和通信，不需要。
- PCIe USB 卡、USB Hub：相机都插 ZED Box，不插 PC。ZED Box Mini 只有 1 个 USB 口，调试时要插键盘鼠标的话，再买带外部电源的 Hub（StarTech ST4300USBM）。

---|---|---|---|---|---|
| 1 | H2D Pro | Bambu PAHT-CF（黑，1 kg，带料盘） | — | 1 | 必买 |
| 2 | H2D Pro | Bambu Support for PA/PET（绿，0.5 kg） | S03-G1-1.75-500-SPL | 1 | 必买 |
| 3 | H2D Pro | Bambu PLA-CF（1 kg，带料盘） | — | 1 | 必买 |
| 4 | H2D Pro | 胶棒（PAHT-CF 要涂胶） | Bambu 原装胶棒 | 1 | 必买 |
| 5 | A250T | 1.75 mm PLA，1 kg，带料盘 | 例：Bambu PLA Basic（スプール付き） | 1–2 | 必买 |
| 6 | A250T | 1.75 mm PETG，1 kg，带料盘 | 例：Bambu PETG HF（スプール付き） | 1 | 必买 |
| 7 | A250T | 双头打印模块 | Snapmaker SNM-23440 | 1 | 想打碳纤时才买 |
| 8 | A250T | 双头模块用 0.4 mm 硬化钢喷嘴 | Snapmaker SNM-23445 | 1–2 | 跟 7 一起买 |
| 9 | Robotiq | e-Series 转接口（M8） | 现有转接口 | — | 已确认能直接插 UR5e 手腕，不用买 |
| 10 | Robotiq | 10 m 高柔性线（M12 直头 → 散线） | CBL-COM-2065-10-HF | — | UR5e 手腕直连后不需要 |
| 11 | Robotiq | USB 转 RS485 | ACC-ADT-USB-RS485 | — | UR5e 手腕直连后不需要 |
| 12 | Robotiq | 24 V 导轨电源（2.5 A） | Mean Well HDR-60-24 | — | UR5e 手腕直连后不需要（手腕供电） |
| 13 | Robotiq | 2 A 保险丝（电源没有过流保护时） | Phoenix Contact 0916605 | — | 不需要 |
| 14 | ZED 2i | 5 m 螺丝锁 USB 3.0 Type-C 线（插 ZED Box） | CBL-221400（装得远就换 10 m CBL-221500） | 1 | 必买 |
| 15 | ZED | 4 口 PCIe USB 3.0 卡（4 个独立通道） | StarTech PEXUSB3S44V | — | 不需要（相机都接 ZED Box，不插 PC） |
| 16 | ZED | 工业级外部供电 USB 3.0 Hub | StarTech ST4300USBM 或 ST4300USBMS | — | 不需要；ZED Box 口不够接键盘鼠标时再买，相机不要走 Hub |
| 17 | ZED X Mini | GMSL2 Fakra 延长线 5 m（公-母，接原配短线） | CBL-310200 | 1 | 必买（原配线很短；总长 ≤ 15 m） |
| 18 | H2D Pro | Bambu AMS HT（单料位烘干送料，最高 85 °C） | SA008 | — | 已有，不用买 |

---

## 1. Bambu Lab H2D Pro：把三个空料仓填满（不改装）

**前提**：PLA 已经占 1 个料仓，TPU 95A HF 照旧从背面外挂进料。喷嘴不换，就用原装的 0.4 mm 碳化钨喷嘴。

### 先确认：原装热端是「标准流量」还是「高流量」

两种热端都是 0.4 mm 碳化钨嘴，但碳纤料的兼容性不一样：

| 料 | 标准流量 0.4 碳化钨（FAH040） | 高流量 0.4 碳化钨 |
|---|---|---|
| PLA-CF | ✅ | 不推荐 |
| PETG-CF | 不推荐 | 不推荐 |
| PAHT-CF | ✅ | 不推荐 |
| ABS-GF | ✅ | ✅ |
| Support for PA/PET / ABS / PLA/PETG | ✅ | ✅ |

在打印机屏幕或 Bambu Studio 的喷嘴信息里看一下是哪种，也可以看热端上的标签。是标准流量就用「推荐方案」，是高流量就用「备选方案」。

### 推荐方案（标准流量 0.4 碳化钨）

| 料仓 | 放什么 | 用来做什么 |
|---|---|---|
| 1 | PLA（已有） | 试装件、普通件 |
| 2 | **Bambu PAHT-CF** | 主力受力件：夹爪指尖、支架、治具。PA12 + 碳纤，吸水率比普通 PA-CF 低一半，受潮后强度只掉 12–18%，层间强度高 |
| 3 | **Bambu Support for PA/PET** | PAHT-CF 的专用支撑，只打支撑接触面 |
| 4 | **Bambu PLA-CF** | 要刚性、要尺寸准的治具和定位块，好打 |

为什么不选 PETG-CF：在原装 0.4 碳化钨嘴上，Bambu 官方表格标的是「不推荐」。

**打印要点**

- **PAHT-CF**：喷嘴 260–290 °C，热床 80–100 °C，腔温 45–60 °C，要涂胶。
- **烘干（不用改装打印机）**：PAHT-CF 和 PA/PET 支撑都要 80 °C 烘 8–12 小时。AMS 2 Pro 最多只能烘到 65 °C，不够，H2D Pro 套装里自带的 **AMS HT**（最高 85 °C）就能烘，不用另买。
  - PAHT-CF 常驻 AMS HT，边烘边送料。
  - PA/PET 支撑先在 AMS HT 里烘好，再放进 AMS 2 Pro。
  - 料仓分配（共 5 个位：AMS 2 Pro 4 个 + AMS HT 1 个）：AMS 2 Pro = PLA、TPU、PLA-CF、PA/PET 支撑；AMS HT = PAHT-CF。TPU 只有 Bambu「TPU for AMS」能放进 AMS，TPU 95A HF 要从背面外挂进料，那样 AMS 2 Pro 会多空一个位。
- **支撑**：PA/PET 支撑打完 2 小时内拆掉，放久了吸潮会粘死。
- **料仓接哪边**：AMS 接右侧固定热端。本体和支撑都从同一个喷嘴出，切片时支撑料只用在「支撑接触面」，可以少冲刷很多料。
- **PET-CF / PPA-CF 不进这三个料仓**：它们只能走左侧升降热端，而且不能进 AMS。

**日本购买**：Bambu Lab 官方日本商店（jp.store.bambulab.com），或者代理 sunstella。工程料在 sunstella 一般要等 10 个工作日左右。

### 备选方案（热端是高流量 0.4，或者不想烘尼龙）

| 料仓 | 放什么 |
|---|---|
| 2 | Bambu ABS-GF（玻纤 ABS，比普通 ABS 强、刚、耐热，可以进 AMS 2 Pro / AMS HT） |
| 3 | Bambu Support for ABS（S06-W0-1.75-500-SPL） |
| 4 | Bambu Support for PLA/PETG（S05-C0-1.75-500-SPL，给已有的 PLA 当支撑） |

---

## 2. Snapmaker A250T

### 原装状态

- 1.75 mm 线材，喷嘴最高 275 °C，热床最高 100 °C。
- 原装单头模块是 0.4 mm 黄铜嘴，官方支持 PLA、ABS、PETG、TPU。
- **原装头不要上碳纤料**，黄铜嘴很快会被磨坏。

### 耗材（原装头直接用）

- **PLA**：1.75 mm、1 kg、带料盘。买 Bambu 的话选「スプール付き」，refill 版没有料盘。
- **PETG**：同样选 1.75 mm 带料盘的。

### 可以自己动手加装的部分

| 改装件 | 料号 | 作用 | 安装 |
|---|---|---|---|
| **双头打印模块** | SNM-23440 | 喷嘴升到 300 °C，热端快拆；支持 PVA、易剥离支撑、尼龙、碳纤/玻纤尼龙 | 跟换激光头、CNC 头一样换整个工具头，装完要做一次校准（用户反馈约 45 分钟） |
| **0.4 mm 硬化钢喷嘴** | SNM-23445 | 双头模块专用，装上才能打碳纤 | 拧到热端上 |
| 快拆套件（A250T 版） | 24006 | 3D 打印 / 激光 / CNC 之间换头不用拧螺丝 | 只有经常换功能时才值得买 |

- 双头模块到货时附带一卷 500 g 易剥离支撑料。
- **风险**：有用户反馈早期批次温控不稳、会中途停止挤出，Snapmaker 后来给发了维修套件。买之前确认一下是不是新批次。
- 装了硬化钢嘴以后，可以打 **PETG-CF、PLA-CF**。这两种对热床和腔体要求低，A250T 打起来最稳。

**日本购买**：Snapmaker 在日本的代理是 VANLINKS 株式会社，在日本官方店、Amazon.co.jp、Yahoo!ショッピング 都有卖（2021 年起）。也可以从 Snapmaker 官网直邮。

---

## 3. Robotiq 2F-140 → PC（RS485，长线方案）

> **现状（更新）**：机械臂换成 **UR5e**。现有的 M8 e-Series 转接口原本就是给 UR e-Series 手腕设计的，夹爪直接插手腕，供电和 RS485 都走机械臂内部，**不用再拉外部线**。
> - 已确认：现有转接口能直接插上 UR5e 手腕，手腕代际匹配，不用换。
> - PC 控制夹爪：PC 用网线连 UR 控制柜。夹爪命令可以走 Robotiq URCap 在控制柜上开的 socket，也可以用 UR 的手腕 RS485 转发，把手腕串口转发成 PC 上的虚拟串口。
> - 下面的方案 A（10 m 线 + USB-RS485）只在夹爪要离开机械臂、在台面上单独用时才需要。

### 先看转接口（coupling）

| 转接口外观 | 型号 | 用哪套线 |
|---|---|---|
| 垂下一根约 1 m 的短线，末端是 M12 圆形插头 | GRP-CPL-062 | **方案 A（推荐）** |
| 边上直接一个 M8 小插头，原本插 UR e-Series 手腕 | GRP-ES-CPL-062 / -077 | 方案 B，或者换成 GRP-CPL-062 走方案 A |

### 方案 A：GRP-CPL-062 + 10 m 线（官方最长、正式支持）

线路：**夹爪短线 → CBL-COM-2065-10-HF（10 m）→ ACC-ADT-USB-RS485 → PC 的 USB 口**

| 料号 | 是什么 |
|---|---|
| CBL-COM-2065-10-HF | 10 m 高柔性线，一头 M12 直插头，一头散线。另有 5 m 版 CBL-COM-2065-05 |
| ACC-ADT-USB-RS485 | 1 m 长的 RS485 转 USB，一头 5 针 Combicon 端子，一头 USB-A |
| Mean Well HDR-60-24 | 24 V 2.5 A 导轨电源。夹爪要求 24 V ±10%、1 A，电源自带保护就不用另加保险丝 |
| Phoenix Contact 0916605 | 2 A 保险丝，用 AWG20 线。只有电源没有过流保护时才需要 |

单夹爪不用买 ACC-SPLIT-M12-2:1，那是双夹爪用的。

**接线（散线那头）**

| 线色 | 接到 |
|---|---|
| 红 | 电源 +24 V |
| 黑 | 电源 0 V |
| 白 | 转换器 1 号针 485+（A） |
| 绿 | 转换器 2 号针 485−（B） |
| 裸线 / 屏蔽 | 转换器 3 号针 485 GND |

- RS485 信号和 24 V 电源是隔离的，电源可以放在离 PC 远的地方。
- 通信参数按说明书默认值：Modbus RTU、115200 bps、8N1、从站 ID 9。
- 线沿着机械臂走时留够余量，让机械臂能转满行程。用螺旋护线套或者魔术贴扎带固定，别让线被关节夹住。

### 想比 10 m 还长

- Robotiq **不出更长的 e-Series 线**，官方建议换成 CB 系列转接口 + 10 m 线（也就是方案 A）。
- 10 m 还不够，就在 PC 那头用端子排自己接一段加长线。说明书要求：电源线至少 22 AWG，RS485 信号线至少 24 AWG。RS485 用屏蔽双绞线。
- 加长以后，在夹爪端量一下电压，**不能低于 21.6 V**（24 V −10%）。不够就把电源线换粗。

### 方案 B：e-Series 转接口（M8 插头）

- 买 ACC-TRBLS-KIT-M8：里面有 M8 8 针公头、母头转散线各一根，加一个 USB 转 RS485。不含 24 V 电源。
- Robotiq 明确说这套线**不能用在机器人运动中**，只适合台面调试、刷固件、改 ID。
- 要长期挂在机械臂上，就换 GRP-CPL-062，走方案 A。

---

## 4. ZED 相机：5 m 以上的线 + 不会烧相机的 USB 接法

### 先确认型号

- 现在有 **ZED 2i 和 ZED Mini 各一台**，都是 USB 3.0 Type-C，看第 4.1、4.2、4.4 节。
- ZED 2i 买 5 m（CBL-221400）或 10 m（CBL-221500）螺丝锁线；ZED Mini 买 4 m 线（CBL-211200）。Mini 再长要用带外部供电的有源延长线，而且要同时延长 USB 2.0，否则 IMU 读不到。
- 两台必须各占一个 USB 3.0 控制器，用 PEXUSB3S44V 正好。
- 第 4.3 节的 ZED X（GMSL2）留作参考，现在用不到。

### 4.1 ZED 2i / ZED Mini 官方线

| 相机 | 品名 | 长度 | 料号 |
|---|---|---|---|
| ZED 2i | USB 3.0 Type-C 双螺丝锁线 | 3 m | CBL-221300 |
| ZED 2i | USB 3.0 Type-C 双螺丝锁线 | **5 m** | **CBL-221400** |
| ZED 2i | USB 3.0 Type-C 双螺丝锁线 | **10 m** | **CBL-221500** |
| ZED 2i | 90° 弯头双螺丝锁线（只有 0.3 / 1.5 / 3 m） | 3 m | CBL-222300 |
| ZED Mini / ZED 2i | USB 3.0 Type-C 线（无螺丝锁） | 4 m | CBL-211200 |

- ZED 2i 用官方螺丝锁线，最远能到 10 m。
- ZED Mini 官方线最长 4 m，再长要用**有源、带外部供电**的延长线。
- Stereolabs 建议用官方线，社区里有用户反馈普通 USB-C 线接上不出图。

### 4.2 超过 10 m

| 方案 | 型号 | 距离 | 注意 |
|---|---|---|---|
| 有源铜缆 | Icron Spectra 3001 | 15 m | ZED Mini / 2 / 2i 会丢 IMU 数据（见下） |
| 光纤延长器 | Icron Spectra 3022 | 100 m | 同上，会丢 IMU 数据 |
| 光纤延长器 | Icron Raven 3124 | 200 m | 官方表里没有 IMU 警告 |
| 有源线 / 光纤中继 | Newnex FireNEX-uLINK 系列 | 最长 300 m | 厂家说 USB 3.0 和 2.0 同时延长，ZED 测过 |

- **IMU 的坑**：ZED Mini、ZED 2、ZED 2i 的图像走 USB 3.0，IMU 和气压计走 USB 2.0。只接了 USB 3.0 线芯的延长线，或者普通 USB-C 光纤线（AOC），**只能传图像，IMU 数据会读不到**。做 SLAM、视觉里程计要用 IMU 的话，选 Raven 3124 或 Newnex 这种同时延长 USB 2.0 的方案。

### 4.3 ZED X / ZED X Mini（GMSL2）

| 品名 | 长度 | 料号 |
|---|---|---|
| GMSL2 Fakra 延长线（公-母） | 5 m | CBL-310200 |
| GMSL2 Fakra 延长线（公-母） | 10 m | CBL-310300 |
| GMSL2 Fakra 延长线（公-母） | 15 m | CBL-310400 |

GMSL2 官方测过最长 15 m，超过 16–20 m 信号损失大，容易掉线。

### 4.4 USB 接法：保证不烧相机、不掉帧

1. **首选直插主机的 USB 3.0 口，不用 Hub。** Stereolabs 的排查文档第一条就是去掉 Hub 和延长线。
2. **一台 ZED 独占一个 USB 3.0 控制器。** 两台 ZED 不能接在同一个 Hub 上，带宽和供电都会不够。
3. **USB 口不够、要接多台**：加一块 **StarTech PEXUSB3S44V**。它是 4 口 PCIe USB 3.0 卡，每个口一个独立的 5 Gbps 通道。装的时候接上 SATA 或大 4pin 供电；也有用户反馈接了供电还是带不动相机，到手先接 ZED 测一下。
4. **一定要用 Hub 时**：只用**带外部电源**的 Hub（官方原话：有源线和带独立电源的 Hub）。推荐工业级：
   - **StarTech ST4300USBM**：金属外壳，每个口有 ESD 防护（空气 8 kV / 接触 4 kV），7–24 V DC 端子供电，附带含日本插头的电源适配器，总功率 20 W。
   - **StarTech ST4300USBMS**：每个口 350 W 浪涌保护，端子排供电，不带适配器，可以直接接 24 V 导轨电源。
5. 不要用来路不明、没有外部供电的便宜 Hub。

---

## 来源

**H2D Pro / Bambu 耗材**
- [Bambu H2D Pro 技术规格（AMS 支持的料）](https://bambulab.com/en-us/h2d-pro/tech-specs)
- [3D Universe – 标准流量碳化钨热端 0.4 mm（FAH040）兼容表](https://shop3duniverse.com/products/bambu-lab-hotend-with-tungsten-carbide-nozzle-0-4-mm-h2d-pro)
- [MatterHackers – H2D Pro 高流量碳化钨热端兼容表](https://www.matterhackers.com/store/l/bambu-lab-h2d-pro-high-flow-hotend-with-tungsten-carbide-nozzle/sk/MF3U93U7)
- [Bambu AMS 2 Pro（烘干上限 65 °C）](https://us.store.bambulab.com/en/products/ams-2-pro)
- [Bambu AMS HT（烘干上限 85 °C）](https://eu.store.bambulab.com/en/products/ams-ht)
- [sunstella – Bambu PAHT-CF](https://sunstella.co.jp/products/bambu-lab-paht-cf-spool)
- [Bambu PAHT-CF 技术数据表（打印参数、支撑材）](https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PAHT-CF_Technical_Data_Sheet.pdf)
- [Bambu Support for PA/PET](https://eu.store.bambulab.com/en-be/products/support-for-pa-pet)
- [Bambu Support for PLA/PETG（日本官方店）](https://jp.store.bambulab.com/en/products/support-for-pla-petg)
- [Bambu Support for ABS](https://eu.store.bambulab.com/es/products/support-for-abs)
- [Bambu ABS-GF](https://puzzlebox3d.com/?p=5075)

**Snapmaker A250T**
- [Snapmaker 3D 打印机规格](https://eu.snapmaker.com/pages/snapmaker-3d-printer)
- [Snapmaker – 双头模块 vs 单头模块](https://support.snapmaker.com/hc/en-us/articles/9162598063255-What-are-the-differences-between-Snapmaker-2-0-Dual-Extrusion-3D-Printing-Module-and-Single-Extrusion-3D-Printing-Module)
- [RobotShop – Snapmaker 双头模块规格](https://www.robotshop.com/products/snapmaker-3d-printer-dual-extrusion-module)
- [Botland – 双头模块 SNM-23440](https://botland.store/extruders/23440-dual-extrusion-module-for-snapmaker-20-3d-printer-6971573440590.html)
- [aio.lv – 双头模块硬化钢喷嘴 SNM-23445](https://aio.lv/en/product--snapmaker-snm-23445--11242844.md)
- [3DJake – Quick Swap Kit A250(T)](https://www.3djake.com/snapmaker/quick-swap-kit?sai=15368)
- [Snapmaker 博客 – 双头模块附带 500 g 易剥离支撑](https://www.snapmaker.com/blog/?p=4793)
- [desertcart – 双头模块用户评价](https://www.desertcart.co.za/products/539306651-snapmaker-2-0-dual-extrusion-3d-printing-module-for-dual)
- [PR TIMES – VANLINKS 日本销售](https://www.excite.co.jp/news/article/Prtimes_2021-07-16-36578-24/)

**Robotiq**
- [Robotiq – USB 直连 PC 的套件组成](https://blog.robotiq.com/knowledge/mounting-robotiq-2f-and-hand-e-grippers-on-franka-emika-robots)
- [Robotiq – 2F 说明书 Installation（电源、保险丝）](https://assets.robotiq.com/website-assets/support_documents/document/online/2F-85_2F-140_TM_InstructionManual_HTML5_20190503.zip/2F-85_2F-140_TM_InstructionManual_HTML5/Content/3.%20Installation.htm)
- [Robotiq – 更长的 e-Series 线](https://blog.robotiq.com/knowledge/longer-e-series-cable)
- [Robotiq – ACC-TRBLS-KIT-M8](https://blog.robotiq.com/knowledge/using-the-acc-trbls-kit-m8-troubleshooting-cable-kit-for-robotiq-grippers)
- [Robotiq – FANUC CRX 用 Robotiq 夹爪](https://blog.robotiq.com/knowledge/using-robotiq-adaptive-grippers-with-fanuc-crx-robots)
- [Robotiq 论坛 – CRX 手腕可用 GRP-ES-CPL-062](https://dof.robotiq.com/discussion/2218)
- [Robotiq – UR 转接口和对应线缆](https://blog.robotiq.com/knowledge/couplings-and-cables-ur-5-1736280767661)
- [READY Robotics – 接线针脚表](https://www.ready-robotics.com/639226a789d6f4bdf9243613/63c9612a40371553b9f89e4d_Setting_Up_a_Robotiq_Gripper_v5.1.0.pdf)
- [manualshive – 加长线规格（22 AWG / 24 AWG）](https://manualshive.com/ru/manual/robotiq/2-finger-140/1471358?page=6)
- [Automation Distribution – CBL-COM-2065-10-HF](https://automationdistribution.com/robotiq-cbl-com-2065-10-hf-cables-and-connectivity)
- [Altronics – Mean Well HDR-60-24](https://www.altronics.com.au/product/m8395-meanwell-60w-24vdc-din-rail-switchmode-power-supply-hdr-60-24)

**ZED / USB**
- [Stereolabs – 能不能用 USB 3 延长线（长距离方案、IMU 警告）](https://support.stereolabs.com/hc/en-us/articles/212542089)
- [Stereolabs – USB 3.0 带宽和连接问题排查](https://support.stereolabs.com/hc/en-us/articles/207635225-How-to-fix-common-USB-3-0-issues)
- [Stereolabs – ZED 2i 双螺丝锁线（料号）](https://www.stereolabs.com/store/products/usb-3-0-type-c-dual-screw-locking-cable)
- [Stereolabs – 90° 弯头螺丝锁线](https://www.stereolabs.com/en-be/store/products/right-angled-usb-3-0-type-c-dual-screw-locking-cable)
- [Stereolabs – USB 3.0 Type-C 线（ZED Mini）](https://www.stereolabs.com/en-tw/store/products/usb-type-c-cable)
- [Stereolabs – GMSL2 Fakra 延长线](https://www.stereolabs.com/en-au/store/products/gmsl2-cable-extender)
- [Stereolabs 社区 – GMSL2 最长 15 m](https://community.stereolabs.com/t/whether-it-can-be-supported-25m-or-not/11027)
- [Stereolabs 社区 – 两台 ZED 不要接同一个 Hub](https://community.stereolabs.com/t/multi-camera-says-camera-not-detected/2574)
- [Newnex – ZED 相机 USB 延长方案](https://newnex.com/zed-camera.php)
- [StarTech PEXUSB3S44V（RS Online）](https://za.rs-online.com/web/p/usb-cards/1383565)
- [StarTech ST4300USBM 规格](https://fleetnetwork.ca/startech-com-st4300usbm-4-port-industrial-usb-3-0-hub-5gbps-mountable-rugged-external/)
- [StarTech ST4300USBMS（浪涌保护版）](https://icecat.fr/us/p/vendorName/mpn/desc-20920404.html)
