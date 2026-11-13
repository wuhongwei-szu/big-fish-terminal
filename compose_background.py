#!/usr/bin/env python3
"""把自备人物按不同透明度叠到选定的背景上，生成对比预览。"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter, ImageOps

import argparse
parser = argparse.ArgumentParser(description="Compose your own background and transparent character; 60/70/80/90 percent variants.")
parser.add_argument("background")
parser.add_argument("character")
parser.add_argument("output")
args = parser.parse_args()
bg_path, girl_path, outdir = args.background, args.character, args.output
os.makedirs(outdir, exist_ok=True)

W, H = 1920, 1080

bg = Image.open(bg_path).convert("RGB")
bg = ImageOps.fit(bg, (W, H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

# 左侧压暗，保证终端文字可读；右侧保留街景亮度
x = np.linspace(0, 1, W, dtype=np.float32)[None, :]
y = np.linspace(0, 1, H, dtype=np.float32)[:, None]
horiz = np.interp(x, [0.0, 0.35, 0.70, 1.0], [0.82, 0.58, 0.16, 0.06])
bottom = np.clip((y - 0.55) / 0.45, 0, 1) * 0.30
alpha = np.clip(horiz + bottom, 0, 0.92)
overlay = np.zeros((H, W, 4), dtype=np.uint8)
overlay[..., 0:3] = np.array([3, 7, 12], dtype=np.uint8)
overlay[..., 3] = (alpha * 255).astype(np.uint8)
bg = Image.alpha_composite(bg.convert("RGBA"), Image.fromarray(overlay, "RGBA")).convert("RGB")

girl = Image.open(girl_path).convert("RGBA")
target_h = 1000
new_w = int(girl.width * target_h / girl.height)
girl = girl.resize((new_w, target_h), Image.Resampling.LANCZOS)
gx = W - new_w - 36
gy = H - target_h

for pct in (60, 70, 80, 90):
    g = girl.copy()
    g.putalpha(g.getchannel("A").point(lambda p: int(p * pct / 100)))

    # 轻微蓝色光晕，让人物从街景里分离出来
    glow = Image.new("RGBA", g.size, (93, 173, 226, 0))
    glow.putalpha(g.getchannel("A").filter(ImageFilter.GaussianBlur(28)).point(lambda p: int(p * 0.28)))

    canvas = bg.copy().convert("RGBA")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(glow, (gx, gy))
    layer.alpha_composite(g, (gx, gy))
    canvas = Image.alpha_composite(canvas, layer).convert("RGB")

    out = os.path.join(outdir, f"character-{pct}.jpg")
    canvas.save(out, quality=92, subsampling=1)
    print(out)
