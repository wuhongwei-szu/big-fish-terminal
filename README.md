# Big Fish Terminal

蓝灰色 Windows Terminal 主题，金色光标、鲸鱼提示符，以及可替换的右侧背景。附带一张按文字新生成的动漫雨夜港湾背景：不需另找图片即可使用。

![默认雨夜港湾背景](assets/harbor-night.png)

## 安装

需要 Windows Terminal 和 Python 3.10 或更新版。保留此文件夹；配置会引用里面的背景与提示符。下面命令在 PowerShell 中运行。

```powershell
$settings = "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
python .\apply_wt_theme.py $settings
```

如果使用 Preview 或非商店版本，通过 Windows Terminal「设置 → 打开 JSON 文件」找到实际路径，替换 `$settings`。安装会添加 `Big Fish Blue`，更新 `profiles.defaults` 的主题字段，保留 profiles 列表与快捷键。单个 profile 显式设置的主题值会覆盖 defaults，请在终端设置中调整该 profile。JSONC 原文（包含注释和原有排版）会完整备份在旁边，当前配置重新写为 JSON。重复安装内容不变时不会重写文件或新增备份。

要启用当前 PowerShell 的鲸鱼提示符，追加 `--profile $PROFILE`。两个 PowerShell 版本的配置文件通常位于同一「文档」目录下，可同时传入：

```powershell
$documents = [Environment]::GetFolderPath('MyDocuments')
python .\apply_wt_theme.py $settings `
  --profile "$documents\PowerShell\Microsoft.PowerShell_profile.ps1" `
  --profile "$documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"
```

重开 PowerShell 标签页生效。已有配置中只替换 `bigfish terminal` 标记块，其他内容保留。支持 UTF-8 与 UTF-16 BOM 的已有 profile；保存为带 BOM 的 UTF-8，兼容 Windows PowerShell 5.1 的中文。没有 Starship 时使用内置的鲸鱼、当前目录和时间提示符。要显示 Git 分支与状态，请另行安装 [Starship](https://starship.rs/guide/)，加入 PATH；也可传 `--starship "C:\path\to\starship.exe"` 指向现有安装。项目不附带二进制、不自动下载软件或更改执行策略。受执行策略限制的机器请遵循自己的管理规则加载 profile。

## 换背景与人物

```powershell
python .\apply_wt_theme.py $settings --background "C:\art\my-background.png" --icon "C:\art\my-icon.png"
```

图片使用 `uniformToFill` 与 `bottomRight`：始终铺满内容区域，宽高比不同会裁剪左侧或上方，右下角保留。默认背景已包含新生成的角色；也可自行提供有权使用的透明角色 PNG，再复用原主题的渐暗与角色合成流程：

```powershell
python -m pip install -r .\requirements-compose.txt
python .\compose_background.py "C:\art\background.jpg" "C:\art\character.png" .\preview-output
python .\apply_wt_theme.py $settings --background "$PWD\preview-output\character-90.jpg"
```

合成输出 1920×1080，左侧压暗、角色靠右，提供 60/70/80/90% 四档透明度。可只用背景，不必使用合成器；安装脚本只依赖 Python 标准库。

默认背景使用内置 ImageGen 按文字生成，未输入原有街景图或角色图。颜色、来源与未随包提供的本机素材见 [SOURCES.md](SOURCES.md)。

## 还原

每次修改都在原文件旁创建 `*.bak-bigfish-时间戳`。关闭终端设置页，将所需备份复制回原路径。要仅停用鲸鱼提示符，从 PowerShell profile 删除 `# >>> bigfish terminal >>>` 到对应结束标记之间的整个块。完整卸载请先恢复 settings 与 profile，再删除本项目文件夹；备份含原有本机配置，请自行保留，不要提交仓库。

## 验证

```powershell
python -m unittest discover -s tests -v
```

测试使用临时配置，覆盖 JSONC、重复安装、原有 profile/快捷键保留、两种 PowerShell profile 写入和缺图时拒绝修改。实际加载仍需在自己的 Windows Terminal 中打开新标签页确认。
