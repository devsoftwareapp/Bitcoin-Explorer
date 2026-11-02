"""Render Play Store screenshots from the real web UI (www/index.html) with sample API data.
Run: python3 play-store/capture_screenshots.py  (from repo root)
"""
import hashlib, json, os, time, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
WWW = ROOT / "www"
OUT = ROOT / "play-store" / "screenshots"
NOW = int(time.time())
TIP = 948214

def H(s): return hashlib.sha256(s.encode()).hexdigest()
def addr(seed): return "bc1q" + H("a" + seed)[:38]
def bhash(h): return H(f"block{h}")

POOLS = ["Foundry USA", "AntPool", "ViaBTC", "MARA Pool", "F2Pool", "Binance Pool"]
BLOCKS = []
for i in range(16):
    h = TIP - i
    BLOCKS.append({
        "id": bhash(h), "height": h, "timestamp": NOW - 150 - i * 600,
        "tx_count": 2800 + (i * 37) % 900, "size": 1_450_000 + i * 11_000,
        "weight": 3_990_000 + i * 2000,
        "extras": {"medianFee": 6 + (i * 3) % 19, "totalFees": 21_000_000 + i * 310_000,
                   "pool": {"name": POOLS[i % len(POOLS)]}},
    })

MAIN_TX = H("tx-main")
TRACK_TX = H("tx-pending")
MAIN_ADDR = addr("main")
OTHER = [addr(f"o{i}") for i in range(20)]

def mk_tx(seed, conf_h, vin_addr=None, vout_addr=None, value=4_250_000):
    txid = H("tx-" + seed)
    confirmed = conf_h is not None
    vin = []
    for k in range(2):
        a = vin_addr if (vin_addr and k == 0) else OTHER[(hash(seed) + k) % 20]
        vin.append({"txid": H(seed + str(k)), "vout": 0, "is_coinbase": False,
                    "prevout": {"scriptpubkey_address": a, "value": value + k * 180_000}})
    vout = [
        {"scriptpubkey_address": vout_addr or OTHER[3], "value": value},
        {"scriptpubkey_address": OTHER[7], "value": 310_000 + (len(seed) * 1111)},
    ]
    bh = bhash(conf_h) if confirmed else None
    return {"txid": txid, "version": 2, "locktime": 0, "size": 221, "weight": 560, "fee": 3_120,
            "vin": vin, "vout": vout,
            "status": {"confirmed": confirmed, "block_height": conf_h, "block_hash": bh,
                       "block_time": NOW - 500 if confirmed else None}}

def chain_txs(addr_, n):
    out = []
    for i in range(n):
        out.append(mk_tx(f"{addr_}-{i}", TIP - 40 - i * 13,
                         vin_addr=addr_ if i % 3 == 0 else None,
                         vout_addr=addr_ if i % 3 != 0 else None,
                         value=(12_000_000 - i * 450_000) if i % 3 else 3_800_000 + i * 60_000))
    return out

MAIN = mk_tx("main", TIP - 3, vin_addr=MAIN_ADDR, vout_addr=OTHER[9], value=8_420_000)
MAIN["txid"] = MAIN_TX
PENDING = mk_tx("pending", None)
PENDING["txid"] = TRACK_TX
ADDR_TXS = chain_txs(MAIN_ADDR, 25)

def fees():
    return {"fastestFee": 14, "halfHourFee": 9, "hourFee": 5, "economyFee": 2, "minimumFee": 1}

def mempool_blocks():
    out = []
    for i in range(8):
        med = [28, 17, 11, 8, 6, 4, 3, 2][i]
        out.append({"medianFee": med, "feeRange": [max(1, med - 3), med - 1, med, med + 2, med + 6, med + 14],
                    "nTx": 2400 + i * 50, "totalFees": 19_000_000 - i * 1_200_000})
    return out

def hashrates():
    base = 1.05e21
    pts = [{"timestamp": NOW - (90 - i) * 86400, "avgHashrate": base * (0.82 + 0.18 * i / 89) * (1 + 0.02 * ((i * 7) % 5 - 2) / 5)} for i in range(90)]
    return {"currentHashrate": 1.11e21, "currentDifficulty": 1.1e14, "hashrates": pts, "difficulty": []}

def route_mempool(route):
    url = route.request.url
    p = url.split("/api", 1)[1].split("?")[0]
    body = None
    if p == "/v1/fees/recommended": body = fees()
    elif p == "/v1/blocks": body = BLOCKS
    elif p == "/mempool": body = {"count": 38214, "vsize": 58_410_000, "total_fee": 512_000_000}
    elif p == "/v1/difficulty-adjustment":
        body = {"progressPercent": 62.4, "difficultyChange": 3.21, "remainingBlocks": 812,
                "estimatedRetargetDate": (NOW + 812 * 600) * 1000}
    elif p == "/v1/prices": body = {"USD": 96410, "EUR": 89200}
    elif p == "/v1/fees/mempool-blocks": body = mempool_blocks()
    elif p == "/v1/mining/hashrate/3m": body = hashrates()
    elif p == "/blocks/tip/height": body = TIP
    elif p.startswith("/block-height/"): body = bhash(int(p.rsplit("/", 1)[1]))
    elif p.startswith("/block/"):
        parts = p.split("/")
        bh = parts[2]
        blk = next((b for b in BLOCKS if b["id"] == bh), BLOCKS[0])
        if len(parts) == 3: body = blk
        else:
            body = ([MAIN] + [mk_tx(f"b{i}", blk["height"]) for i in range(24)])
    elif p.startswith("/tx/"):
        tid = p.split("/")[2]
        if tid == TRACK_TX: body = PENDING
        elif tid == MAIN_TX: body = MAIN
        else: return route.fulfill(status=404, body="Transaction not found", headers={"Access-Control-Allow-Origin": "*"})
    elif p.startswith("/v1/tx/"): body = {}
    elif p.startswith("/address/"):
        parts = p.split("/")
        a = parts[2]
        if len(parts) == 3:
            body = {"address": a, "chain_stats": {"funded_txo_sum": 512_000_000, "spent_txo_sum": 383_570_000, "tx_count": 37},
                    "mempool_stats": {"funded_txo_sum": 0, "spent_txo_sum": 0, "tx_count": 0}}
        elif parts[3] == "txs" and len(parts) == 4: body = ADDR_TXS
        else: body = []
    else:
        return route.fulfill(status=404, body="not found", headers={"Access-Control-Allow-Origin": "*"})
    route.fulfill(status=200, body=json.dumps(body), headers={
        "Content-Type": "application/json", "Access-Control-Allow-Origin": "*"})

CURRENT_SHOT = {"html": ""}

def route_app(route):
    p = route.request.url.split("app.local", 1)[1].split("#")[0].split("?")[0]
    if p == "/shot.html":
        return route.fulfill(status=200, body=CURRENT_SHOT["html"], headers={"Content-Type": "text/html"})
    f = WWW / p.lstrip("/")
    if not f.exists(): return route.fulfill(status=404, body="nf")
    ct = "text/html" if f.suffix == ".html" else "application/javascript"
    route.fulfill(status=200, body=f.read_bytes(), headers={"Content-Type": ct})

SEED_JS = """
if (location.hostname === 'app.local' && !sessionStorage.getItem('seeded')) {
  sessionStorage.setItem('seeded', '1');
  localStorage.setItem('bx_cfg', JSON.stringify({unit:'btc', theme:'dark'}));
  localStorage.setItem('bx_fav', JSON.stringify([
    {t:'address', id:'%s'}, {t:'tx', id:'%s'}, {t:'block', id:'%s'}]));
  localStorage.setItem('bx_rec', JSON.stringify([
    {t:'tx', id:'%s'}, {t:'address', id:'%s'}, {t:'block', id:'%s'}]));
  localStorage.setItem('bx_trk', JSON.stringify([{id:'%s', st:0}]));
  localStorage.setItem('bx_wtrk', JSON.stringify([{id:'%s', n:37, b:128430000}]));
}
""" % (MAIN_ADDR, MAIN_TX, BLOCKS[0]["id"], MAIN_TX, MAIN_ADDR, BLOCKS[0]["id"], TRACK_TX, MAIN_ADDR)

# (filename, caption, app hash route, action)
SHOTS = [
    ("01_home", "Live Bitcoin fees and mempool at a glance", "", None),
    ("02_transaction", "Track any transaction, step by step", "tx/" + MAIN_TX, None),
    ("03_address", "Check balances and history for any address", "address/" + MAIN_ADDR, None),
    ("04_menu", "Favorites, tracking and wallet alerts", "", "menu"),
]
SIZES = {  # folder: (css_w, css_h, dsf, output px)
    "phone": (540, 960, 2),     # 1080x1920
    "tablet7": (600, 960, 2),   # 1200x1920
    "tablet10": (800, 1280, 2), # 1600x2560
}

def page_html(w, h, caption, src):
    hh = int(h * 0.22)
    fs = int(w * 0.068)
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{{margin:0;height:{h}px;width:{w}px;overflow:hidden;background:#000;font-family:'Roboto','Helvetica Neue',Arial,sans-serif}}
.bg{{position:absolute;inset:0;background:radial-gradient({int(w*0.9)}px {int(h*0.35)}px at 85% 0%,rgba(247,147,26,.45),transparent 60%),radial-gradient({int(w*0.8)}px {int(h*0.3)}px at 0% 100%,rgba(247,147,26,.25),transparent 60%),#000}}
.head{{position:absolute;top:0;left:0;right:0;height:{hh}px;display:flex;flex-direction:column;justify-content:center;padding:0 {int(w*0.07)}px;box-sizing:border-box}}
.kick{{color:#f7931a;font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:{int(fs*0.42)}px;margin-bottom:{int(h*0.008)}px}}
h1{{color:#fff;font-weight:800;line-height:1.12;margin:0;font-size:{fs}px;letter-spacing:-.01em}}
iframe{{position:absolute;left:{int(w*0.07)}px;top:{hh}px;width:{int(w*0.86)}px;height:{h-hh-int(h*0.04)}px;border:0;border-radius:{int(w*0.035)}px;box-shadow:0 0 0 2px #1c1c1c,0 30px 80px rgba(0,0,0,.6);background:#0d0f1a}}
</style></head><body><div class="bg"></div><div class="head"><div class="kick">Bitcoin Explorer</div><h1>{caption}</h1></div>
<iframe id="app" src="{src}"></iframe></body></html>"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=[
            "--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist", "--no-sandbox"])
        for folder, (w, h, dsf) in SIZES.items():
            d = OUT / folder
            d.mkdir(parents=True, exist_ok=True)
            ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=dsf)
            ctx.route("https://mempool.space/api/**", route_mempool)
            ctx.route("https://app.local/**", route_app)
            ctx.add_init_script(SEED_JS)
            pg = ctx.new_page()
            for fname, caption, route_hash, action in SHOTS:
                src = "https://app.local/index.html" + ("#/" + route_hash if route_hash else "")
                CURRENT_SHOT["html"] = page_html(w, h, caption, src)
                pg.goto("https://app.local/shot.html", wait_until="load")
                frame = pg.frame_locator("#app")
                # wait for the app inside the iframe
                app = pg.frames[1] if len(pg.frames) > 1 else None
                deadline = time.time() + 25
                while app is None and time.time() < deadline:
                    time.sleep(0.3); app = pg.frames[1] if len(pg.frames) > 1 else None
                ok = False
                while time.time() < deadline and not ok:
                    try:
                        ok = app.evaluate("!!document.querySelector('.card, .sct, .tx, .row')")
                    except Exception:
                        pass
                    time.sleep(0.4)
                time.sleep(1.8)
                if action == "menu":
                    app.evaluate("openDrawer()")
                    time.sleep(0.9)
                pg.screenshot(path=str(d / f"{fname}.png"))
                print(folder, fname, "ok" if ok else "NOT-READY")
                # close any open drawer before next shot
                try: app.evaluate("closeDrawer && closeDrawer()")
                except Exception: pass
            ctx.close()
        br.close()

if __name__ == "__main__":
    main()
