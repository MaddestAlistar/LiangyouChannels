# 良友频道库 · LiangyouChannels

由小红书：良哥看未来整理，更新时间：2026 年 10 月 4 日

点击网页里的主播头像，复制完整房间号或抖音账号标识，随后在汇流选择对应平台并手动粘贴添加。

- 抖音：50
- 斗鱼：32
- 虎牙：32
- B站：35
- YY：29

## 访问地址

播放器图标库订阅 JSON（在 App 的图标库入口添加）：

<https://raw.githubusercontent.com/MaddestAlistar/LiangyouChannels/main/liangyouchannels.json>

在线头像库：

<https://liangyou-channels.rf6mzd6g4q.chatgpt.site>

本仓库同时包含完整静态网页，可直接交给 GitHub Pages 或其他静态托管服务使用。GitHub Pages 的仓库设置选择 **Deploy from a branch / main / (root)** 即可。

## 头像和复制规则

178 张头像来自对应平台的公开主播或频道头像，制作成 256×256 PNG；每张图片左上角都包含平台文字角标。图标保存在 `icons/<平台>/<编号>.png`，头像原始来源保存在 JSON 的 `avatarSource` 和 `avatarSourcePage` 中。

**所有房间号均为字符串，点击时原样复制 `copyValue`。** 不去除句点，不转换为数字，不改变大小写：

- 陈泽：`9896719.`，末尾英文句点必须保留。
- 旭旭宝宝：`renyixu1989`。
- 小尾巴-ASMR：`Maren134689`。
- 盛宇：`DamnshinX`。
- 斗鱼靓号仍按确认名单复制，例如若若 `171717`、南波儿 `123455`；头像从当前直播间页面获取，避免旧接口把靓号识别成其他账号。

## 图标库格式

`liangyouchannels.json` 使用与良友媒体图标库相同的 `name / description / icons` 格式。每个图标含 `name` 和绝对 HTTPS 地址 `url`，可用于支持此格式的播放器图标库入口。

图标库订阅提供头像，不是直播播放列表。点击头像复制房间号的功能在在线头像库中使用。

## 频道数据字段

`channel-data.json` 保存在线头像库需要的完整频道数据；原有名称、平台、房间号、复制值和头像来源均在此文件中。

频道数据地址：

<https://raw.githubusercontent.com/MaddestAlistar/LiangyouChannels/main/channel-data.json>

JSON 顶层包含 `description`（整理者及更新时间）、`updatedAt`（`2026-10-04`）和 `channels`（频道数组）。每个频道的字段如下：

| 字段 | 用途 |
| --- | --- |
| `id` | 稳定频道标识 |
| `name` | 频道显示名称 |
| `platform` | `douyin`、`douyu`、`huya`、`bilibili` 或 `yy` |
| `platformLabel` | 中文平台名称 |
| `roomId` | 原样保存的房间号或账号标识，字符串 |
| `copyValue` | 点击头像时复制的字符串，与 `roomId` 一致 |
| `copyType` | `room_id` 或 `douyin_id` |
| `type` | `anchor`（主播）、`channel`（直播间）或 `event`（赛事） |
| `icon` | 仓库内的 PNG 路径，含平台角标 |
| `avatar` | PNG 的 GitHub Raw 直链，含平台角标 |
| `liveUrl` | 对应平台的直播入口 |
| `currentName` | 获取头像时的平台名称 |
| `avatarSource` | 原平台头像地址 |
| `avatarSourcePage` | 获取头像的页面或接口 |
| `avatarFetchedAt` | 头像获取日期 |
| `listConfirmedAt` | 名单确认日期 |

此页面使用浏览器原生复制功能，兼容回退复制及手动长按复制；支持键盘操作和手机浏览。网页读取同目录的 `channel-data.json`。以后增删频道时，应先更新此文件，再从 `channels` 按顺序重建 `liangyouchannels.json` 的 `icons`：`name` 取频道名称，新增的同名跨平台主播用平台后缀区分，`url` 取 `avatar`，同时同步两份文件的 `description`。房间号与 `copyValue` 必须保留原始大小写和全部符号。

本库由良哥看未来整理；主播、平台名称及头像属于各自对应的主体。


## 2026 年 10 月 4 日新增名单

本次五个平台各新增20位主播，原有78个频道保留，共178个。房间号和头像按对应平台的公开资料核对；名单不代表当前正在开播。

| 平台 | 主播 | 房间号 / 账号标识 |
| --- | --- | --- |
| 抖音 | [摩登兄弟刘宇宁](https://live.douyin.com/MD4528) | `MD4528` |
| 抖音 | [郭聪明](https://live.douyin.com/4045640) | `4045640` |
| 抖音 | [刘畊宏](https://live.douyin.com/895373343) | `895373343` |
| 抖音 | [吕德华](https://live.douyin.com/dehua66888) | `dehua66888` |
| 抖音 | [海来阿木](https://live.douyin.com/HLam0403) | `HLam0403` |
| 抖音 | [冯提莫](https://live.douyin.com/Fengtimo1219) | `Fengtimo1219` |
| 抖音 | [广东夫妇](https://live.douyin.com/AresCheng) | `AresCheng` |
| 抖音 | [一条小团团OvO](https://live.douyin.com/tuantuanxhchibb) | `tuantuanxhchibb` |
| 抖音 | [csgo茄子](https://live.douyin.com/Bigqiezi) | `Bigqiezi` |
| 抖音 | [唐艺](https://live.douyin.com/Baobao102) | `Baobao102` |
| 抖音 | [小阿七](https://live.douyin.com/xaq54886) | `xaq54886` |
| 抖音 | [高火火](https://live.douyin.com/HuoHuo6666) | `HuoHuo6666` |
| 抖音 | [兔子牙](https://live.douyin.com/tuziya55555) | `tuziya55555` |
| 抖音 | [多余和毛毛姐](https://live.douyin.com/duoyuduoyu) | `duoyuduoyu` |
| 抖音 | [骆王宇](https://live.douyin.com/luowangyu123) | `luowangyu123` |
| 抖音 | [董先生](https://live.douyin.com/dongxianshengzb) | `dongxianshengzb` |
| 抖音 | [刘媛媛·媛之有物](https://live.douyin.com/liuyuanyuan1991) | `liuyuanyuan1991` |
| 抖音 | [童锦程798。](https://live.douyin.com/tong798798) | `tong798798` |
| 抖音 | [骚男](https://live.douyin.com/196343414) | `196343414` |
| 抖音 | [郭有才](https://live.douyin.com/51192723700) | `51192723700` |
| 斗鱼 | [Big茄子](https://www.douyu.com/9418) | `9418` |
| 斗鱼 | [pigff](https://www.douyu.com/24422) | `24422` |
| 斗鱼 | [zard1991](https://www.douyu.com/60937) | `60937` |
| 斗鱼 | [玩机器丶Machine](https://www.douyu.com/6657) | `6657` |
| 斗鱼 | [智勋勋勋勋](https://www.douyu.com/312212) | `312212` |
| 斗鱼 | [冷少icon](https://www.douyu.com/96555) | `96555` |
| 斗鱼 | [椰汁糕冬瓜强](https://www.douyu.com/63136) | `63136` |
| 斗鱼 | [DL丶拖米](https://www.douyu.com/793400) | `793400` |
| 斗鱼 | [Zhou陈尧](https://www.douyu.com/88660) | `88660` |
| 斗鱼 | [白鲨AyoM](https://www.douyu.com/728) | `728` |
| 斗鱼 | [主播阿飞](https://www.douyu.com/84452) | `84452` |
| 斗鱼 | [仙某某](https://www.douyu.com/88080) | `88080` |
| 斗鱼 | [20岁天才歌手Running](https://www.douyu.com/2448877) | `2448877` |
| 斗鱼 | [雨神丶](https://www.douyu.com/6512) | `6512` |
| 斗鱼 | [叫我老陈就好了](https://www.douyu.com/74960) | `74960` |
| 斗鱼 | [大Mu金仙丶](https://www.douyu.com/1870001) | `1870001` |
| 斗鱼 | [甜心战士](https://www.douyu.com/242045) | `242045` |
| 斗鱼 | [贝拉小姐姐](https://www.douyu.com/3276456) | `3276456` |
| 斗鱼 | [QuQu非常规大师](https://www.douyu.com/5232) | `5232` |
| 斗鱼 | [陈死狗cnh](https://www.douyu.com/5524515) | `5524515` |
| 虎牙 | [董小飒](https://www.huya.com/13579) | `13579` |
| 虎牙 | [楚河](https://www.huya.com/998) | `998` |
| 虎牙 | [安德罗妮](https://www.huya.com/528300) | `528300` |
| 虎牙 | [TheShy](https://www.huya.com/991111) | `991111` |
| 虎牙 | [DANK1NG](https://www.huya.com/10188) | `10188` |
| 虎牙 | [RASH悲喜](https://www.huya.com/988) | `988` |
| 虎牙 | [鲨鱼哟](https://www.huya.com/400298) | `400298` |
| 虎牙 | [AG绝迹](https://www.huya.com/115959) | `115959` |
| 虎牙 | [陈子豪](https://www.huya.com/199300) | `199300` |
| 虎牙 | [Letme严君泽](https://www.huya.com/518518) | `518518` |
| 虎牙 | [托马斯CzH](https://www.huya.com/20641) | `20641` |
| 虎牙 | [小宇热游](https://www.huya.com/10098) | `10098` |
| 虎牙 | [CSBOY](https://www.huya.com/123321) | `123321` |
| 虎牙 | [杨齐家](https://www.huya.com/60066) | `60066` |
| 虎牙 | [芜湖神](https://www.huya.com/353322) | `353322` |
| 虎牙 | [北枫CC](https://www.huya.com/572329) | `572329` |
| 虎牙 | [狂魔哥解说](https://www.huya.com/919191) | `919191` |
| 虎牙 | [集梦阿布](https://www.huya.com/18) | `18` |
| 虎牙 | [集梦会长](https://www.huya.com/116) | `116` |
| 虎牙 | [节奏](https://www.huya.com/476644) | `476644` |
| B站 | [怕上火暴王老菊](https://live.bilibili.com/1030) | `1030` |
| B站 | [瓶子君152](https://live.bilibili.com/42062) | `42062` |
| B站 | [泛式](https://live.bilibili.com/33989) | `33989` |
| B站 | [渗透之C君](https://live.bilibili.com/1011) | `1011` |
| B站 | [神奇陆夫人](https://live.bilibili.com/115) | `115` |
| B站 | [魔法Zc目录](https://live.bilibili.com/721) | `721` |
| B站 | [hanser](https://live.bilibili.com/255) | `255` |
| B站 | [泠鸢yousa](https://live.bilibili.com/593) | `593` |
| B站 | [祖娅纳惜](https://live.bilibili.com/938957) | `938957` |
| B站 | [小缘](https://live.bilibili.com/196) | `196` |
| B站 | [兰音Reine](https://live.bilibili.com/22696653) | `22696653` |
| B站 | [永雏塔菲](https://live.bilibili.com/22603245) | `22603245` |
| B站 | [向晚大魔王](https://live.bilibili.com/22625025) | `22625025` |
| B站 | [乃琳Queen](https://live.bilibili.com/22625027) | `22625027` |
| B站 | [早稻叽](https://live.bilibili.com/631) | `631` |
| B站 | [東雪蓮Official](https://live.bilibili.com/22816111) | `22816111` |
| B站 | [雫るる_Official](https://live.bilibili.com/21013446) | `21013446` |
| B站 | [阿萨Aza](https://live.bilibili.com/52030) | `52030` |
| B站 | [冰糖IO](https://live.bilibili.com/876396) | `876396` |
| B站 | [扇宝](https://live.bilibili.com/22673512) | `22673512` |
| YY | [毕加索](https://www.yy.com/3594) | `3594` |
| YY | [大佛](https://www.yy.com/3851) | `3851` |
| YY | [兰梦莎](https://www.yy.com/4064) | `4064` |
| YY | [芮甜甜](https://www.yy.com/9759) | `9759` |
| YY | [浅蓝](https://www.yy.com/2648) | `2648` |
| YY | [大脸](https://www.yy.com/4164) | `4164` |
| YY | [晓夏](https://www.yy.com/2023) | `2023` |
| YY | [小天天](https://www.yy.com/3713) | `3713` |
| YY | [安安子](https://www.yy.com/2132) | `2132` |
| YY | [娅儿](https://www.yy.com/1251) | `1251` |
| YY | [小苹果](https://www.yy.com/939) | `939` |
| YY | [舞喵](https://www.yy.com/1659) | `1659` |
| YY | [AK](https://www.yy.com/5349) | `5349` |
| YY | [安迪](https://www.yy.com/2196) | `2196` |
| YY | [苏子](https://www.yy.com/2354) | `2354` |
| YY | [田子晴](https://www.yy.com/1551) | `1551` |
| YY | [戳小琪](https://www.yy.com/4172) | `4172` |
| YY | [李萝莉](https://www.yy.com/7940) | `7940` |
| YY | [李大鑫](https://www.yy.com/1418) | `1418` |
| YY | [小胖晚](https://www.yy.com/1860) | `1860` |
