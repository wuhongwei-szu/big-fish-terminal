# 来源与分发边界

- `apply_wt_theme.py`、`starship.toml` 基于本机已安装的主题脚本整理；去除了本机用户名、磁盘路径、Git Bash 专用路径、下载和备份产物。`compose_background.py` 沿用原本的 NumPy/Pillow 合成算法，移除了私人预览页面，输入改为命令行参数，并修正角色透明度重复相乘的问题。
- `scheme.json` 保留实际使用的 20 个颜色值。配色设计从 [TCX123-a/MiAiCoding《大肥鱼视觉宪法》](https://github.com/TCX123-a/MiAiCoding/blob/c43646e53c486ca9e413129b59a1a76ce8d133c6/docs/10-%E5%A4%A7%E8%82%A5%E9%B1%BC%E8%A7%86%E8%A7%89%E5%AE%AA%E6%B3%95.md) 的视觉规范映射到暗色终端；本项目只提供颜色数值及本地映射，不复制上游文档或代码。上游该版本的 [LICENSE](https://github.com/TCX123-a/MiAiCoding/blob/c43646e53c486ca9e413129b59a1a76ce8d133c6/LICENSE) 标注 MIT、Copyright (c) 2026 miai，且 scope note 排除第三方图片和资产。与上游及 DeepSeek 无隶属关系。
- `assets/harbor-night.png` 使用内置 ImageGen 按文字描述新生成，内容为动漫雨夜港湾、鲸鱼灯和身穿黄色雨衣的守灯人。生成时未输入本机原有背景、角色图或其合成图片；本项目随代码一同提供此默认背景。
- 本机人物图曾引用 `EDMOK/blue-fish-archive`，未发现其允许再分发的许可证；人物、头像、图标均不随项目提供。
- 本机街景背景曾引用 [Pixabay 插画 8788959](https://pixabay.com/illustrations/anime-street-urban-nocturnal-8788959/)。该图与其衍生合成图片均不随项目提供；需要原图的使用者请在原站自行核对当前许可、下载和使用条件。
- [Starship](https://github.com/starship/starship) 为独立项目；本包不附带可执行文件。Pillow、NumPy 仅为可选合成器的运行依赖，不随包复制。

本项目的许可证仅覆盖随包提供、由项目维护者拥有相应权利的代码与随包默认背景，不向外部图片、品牌或第三方软件扩展授权。
