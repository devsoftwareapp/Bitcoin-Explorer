"""Play Console graphics: 512x512 hi-res icon (PNG, no alpha) and 1024x500 feature graphic."""
import pathlib, base64
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "play-store" / "graphics"
OUT.mkdir(parents=True, exist_ok=True)
FG = ROOT / "android/app/src/main/res/mipmap-xxxhdpi/ic_launcher_foreground.png"

# 512x512 icon: black background + adaptive foreground (orange coin), flattened, no alpha
fg = Image.open(FG).convert("RGBA").resize((512, 512), Image.LANCZOS)
icon = Image.new("RGBA", (512, 512), (0, 0, 0, 255))
icon.alpha_composite(fg)
icon.convert("RGB").save(OUT / "app_icon_512.png", optimize=True)

# 1024x500 feature graphic rendered from HTML
coin_b64 = base64.b64encode(FG.read_bytes()).decode()
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;width:1024px;height:500px;overflow:hidden;background:#000;font-family:'Roboto','Helvetica Neue',Arial,sans-serif;color:#fff}}
.bg{{position:absolute;inset:0;background:radial-gradient(620px 360px at 88% 30%,rgba(247,147,26,.55),transparent 62%),radial-gradient(520px 300px at 0% 100%,rgba(247,147,26,.28),transparent 60%)}}
.t{{position:absolute;left:64px;top:110px;width:600px}}
.k{{color:#f7931a;font-weight:700;letter-spacing:.16em;font-size:22px;text-transform:uppercase}}
h1{{margin:14px 0 18px;font-size:76px;line-height:1.02;font-weight:800;letter-spacing:-.02em}}
p{{margin:0;font-size:28px;line-height:1.35;color:#e9e9e9;font-weight:500}}
.coin{{position:absolute;right:-40px;top:20px;width:520px;height:520px;opacity:.95}}
</style></head><body><div class="bg"></div>
<div class="t"><div class="k">Live Bitcoin data</div><h1>Bitcoin Explorer</h1>
<p>Fees, mempool, blocks, transactions<br>and wallet alerts in one place</p></div>
<img class="coin" src="data:image/png;base64,{coin_b64}"></body></html>"""
with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = br.new_page(viewport={"width": 1024, "height": 500}, device_scale_factor=1)
    pg.set_content(html, wait_until="load")
    pg.screenshot(path=str(OUT / "feature_graphic_1024x500.png"))
    br.close()
print("done")
