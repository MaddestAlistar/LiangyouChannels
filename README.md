# 良友频道库 · LiangyouChannels

根据共享聊天最后确认的 **54 个频道**整理。点击网页里的主播头像，复制完整房间号或抖音账号标识，随后在汇流选择对应平台并手动粘贴添加。

- 抖音：8
- 斗鱼：11
- 虎牙：11
- B站：14
- YY：10

## 访问地址

频道数据 JSON：

<https://raw.githubusercontent.com/MaddestAlistar/LiangyouChannels/main/liangyouchannels.json>

在线头像库：

<https://liangyou-channels.wintry-oasis-8264.chatgpt.site>

本仓库同时包含完整静态网页，可直接交给 GitHub Pages 或其他静态托管服务使用。GitHub Pages 的仓库设置选择 **Deploy from a branch / main / (root)** 即可。

## 头像和复制规则

54 张头像来自对应平台的公开主播或频道头像，制作成 256×256 PNG；每张图片左上角都包含平台文字角标。图标保存在 `icons/<平台>/<编号>.png`，头像原始来源保存在 JSON 的 `avatarSource` 和 `avatarSourcePage` 中。

**所有房间号均为字符串，点击时原样复制 `copyValue`。** 不去除句点，不转换为数字，不改变大小写：

- 陈泽：`9896719.`，末尾英文句点必须保留。
- 旭旭宝宝：`renyixu1989`。
- 小尾巴-ASMR：`Maren134689`。
- 斗鱼靓号仍按确认名单复制，例如若若 `171717`、南波儿 `123455`；头像从当前直播间页面获取，避免旧接口把靓号识别成其他账号。

微凉仍保留聊天确认的 YY `4098`。2026-10-03 该入口暂不可访问，JSON 标记 `roomStatus: needs_recheck`；头像使用 YY 官方搜索页中的睿廷微凉本人头像。此库保留确认名单，不将开播状态作为入库条件。

## JSON 字段

JSON 顶层为数组，每一项对应一个频道。

| 字段 | 用途 |
| --- | --- |
| `id` | 稳定频道标识 |
| `name` | 聊天最终确认的显示名称 |
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

此页面使用浏览器原生复制功能，兼容回退复制及手动长按复制；支持键盘操作和手机浏览。网页读取同目录的 JSON，更新名单时保留原始字符串。

本库由良哥看未来整理；主播、平台名称及头像属于各自对应的主体。
