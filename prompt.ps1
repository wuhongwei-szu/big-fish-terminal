param([string]$StarshipPath)
$env:STARSHIP_CONFIG = Join-Path $PSScriptRoot 'starship.toml'
$starship = if ($StarshipPath -and (Test-Path -LiteralPath $StarshipPath)) { $StarshipPath } else { (Get-Command starship -ErrorAction SilentlyContinue).Source }
if ($starship) {
    Invoke-Expression (& $starship init powershell)
} else {
    function global:prompt {
        Write-Host ('🐋 主人 in ' + $PWD.Path + ' ' + (Get-Date -Format 'HH:mm')) -ForegroundColor Cyan
        return '❯ '
    }
}
