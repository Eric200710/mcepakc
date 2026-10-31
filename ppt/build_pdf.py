# -*- coding: utf-8 -*-
"""
ebrewing × AI Agent — 課堂報告 PDF 生成腳本
Swiss Style · IKB 克萊因藍 · 16:9 (1024×576pt)
"""
import sys, io, os, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate
from reportlab.graphics.shapes import *
from reportlab.pdfgen import canvas as rl_canvas
from PIL import Image
import tempfile

# ── 尺寸 16:9 ──────────────────────────────────────────────────
W, H = 960, 540   # points (px at 72dpi)

# ── 顏色 ───────────────────────────────────────────────────────
INK     = colors.HexColor('#0a0a0a')
PAPER   = colors.HexColor('#fafaf8')
GREY1   = colors.HexColor('#f0f0ee')
GREY2   = colors.HexColor('#d4d4d2')
GREY3   = colors.HexColor('#737373')
ACCENT  = colors.HexColor('#002FA7')   # IKB Klein Blue
WHITE   = colors.white
DARK_BG = colors.HexColor('#0f0f0f')

# ── 字型 ───────────────────────────────────────────────────────
FONT_DIR = r'C:\Windows\Fonts'
try:
    pdfmetrics.registerFont(TTFont('NotoSansSC', os.path.join(FONT_DIR, 'NotoSansSC-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('NotoSansSC-Bold', os.path.join(FONT_DIR, 'NotoSansSC-Bold.ttf')))
    ZH = 'NotoSansSC'; ZH_B = 'NotoSansSC-Bold'
except:
    ZH = 'Helvetica'; ZH_B = 'Helvetica-Bold'

MONO = 'Courier'
SANS = 'Helvetica'
SANS_B = 'Helvetica-Bold'

# ── 魚皮膚 base64 ─────────────────────────────────────────────
SKIN_B64 = {
    '黃鱸':     'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAEr0lEQVR4AexWPWwbZRh+7nw+O2ljY9ehsUKtJpGgKCRNRVQ6BFSJkYEBlbKgbkggKOLHSEwIBANq2dj4U2cWOnRnyIAYGOiABCogFgbShKRRHNvn+/iez1x6dzrncuGiE6fv5Mff+/O8333vj+9sIuZ697Uzon11Xrzefly88s4T4uX2eSkvi08/Pic+u3ZOXP/gjMLq9Zbww7PHbJ/I/db7K4JIFBRDji3AbnkcO+Xj2HUL6PVc9PsCnYGJn/+20XcNtf2F8R18tzMeAG3KmeLXH79ugkhxS8QWoOMYcAYCve4A/d5Arg6cvovdros7d4cFYPL+hCnTluZBuVdrtgoCKV6xBTCLFgayAK4r5AQM0JfJO44L1wU6wgKTHXWe/XyjYvazs/vEfpykvtgCQAiwz0KtUhKAIRdAqHVxuYWXnmrg9FwVLywUFSjTRh9SvNh9IsUt438ClRJgmAYsqwCraMIuFVAoGBImKrYAr62NTS4BRNkChEMo7D5xiNCRIeZIz7+O0zUX5ZIpkzdQkskXZRGKdgF20cDciQF4vfEN8OLnOxQVKNOmlBS/2H0ixS3jJ+CX7TIWTg6wcXcXRXs4AetrHSxOCfy0NQZ2em3tfvLe4Wijz9PTWNl9Io29vD3MrW9XxKUrCwpRMm94eUn+DmSE4wj1EJQiLi/Z6pXETt9sN9FojINypVZVMnXK4T3DOvc6KNh94qD8g/BMkh5t2ZhtFinCLy8/XFK6csivXtcBX4VSVB9yyaHCeOphOUonj3z6kuCT91YNIklMHFcVoNUwMVVTIvzyI1Mm3n56TO1Rr5fka9BFV/4fOFEvKxt95FBhPGPDcpROHvn0ZQ2V9YwswHRNifDLj01Ze+c7VS/Als+AUsnCQ/UhF/LyOIxnrDTBL0fp5JFD3wExfN0EyVG2ICOk8W804TerTOZkctNVQ9n98oPHlFvZnztr4dSkLWHh0tL9wngcxjOWZL8cpZNHDn1/XWkKPhe2v7TEvQ8h1l8dE7TR58PwcD6DFAM2xtz7CGL7C7nPrXm154/PNANF4vNMxgU+KsP6mInWA8Ok/LKfOV0x0L5oSRTRnAjcW9EYz1gqfjlKJ48c+iZv/Gl0v7oDd/YCjAnAsPoYdf1287wgRvmN49LTmIE4VsPv125j8dZm4KB8gIaLYJbnr4Colgy1hmXqHibW3wTh6f51v3i/z4vxbPLI2CvC2RU4G5NKpz2MmWe/N4iwnTr36PzQhFs9GZk8OUyeRaDsQU0AFR6MK+GXqXvoPynfAhKe7l/9MX6ZnLAeZWMClYurBlf6DwPGco9w5729vr5x2wi/RUx78nkjS3iHy2rdm4CsDpD1fXUBsu5A1vc/igkIvHuzTjDu/kdRgMC7N+4AWfuPogBZ55To/roAicqVQ7KegBw2NVFKegISlSuHZD0BOWxqopRyPwFx1dAFiKtQ3v16AvLe4bj89ATEVSjvfj0Bee9wXH56AuIqlHe/noC8dzguPz0BcRXKu19PQN46nDQfPQFJK5Y3vp6AvHU0aT56ApJWLG98PQF562jSfPQEJK1Y3vh6AvLW0aT56AlIWrG88fUE/N87+l/P/w8AAAD///OocmcAAAAGSURBVAMAGMKgkO/seZ0AAAAASUVORK5CYII=',
    '公子小丑魚': 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABAUlEQVR4nO3WrZLCMBDA8U2mKEQRnOgJangcLBrPE/AIpxHnT5+9xwFRBDGYGgwizGLoMIXw0Ztpyf8300k63V2R5stIQJZlviiKUz/P81NbfV9NDzfz+8udkRazEjkrHeIXI68zMtoB+A9WImclclYiZyVy5tVzfvzbk1D+ZUy15iP3BD0FPn8O4px76m5Rl59Ih5ivjYlmCaTp0CttX4np7ACoweBDmoi5JZEW0H1oO+s9PN3L8rx/6PqufqvbK+pqWukQ//ft9WmyZhIKWLt9ICK9Iz8N1tQ/FmIm86uz4p781i4B9+Sx1nQNAAAAAAAAAAAAAAAAAAAAAAAgb+EIZahtPj4yi94AAAAASUVORK5CYII=',
    '虎皮魚':    'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABJElEQVR4nO3WMU7DMBSA4WerU9hQGWDo3qEM5QacoDNHYOYQDMw9AnPugWDJ0L0DDM0cdTN6loxCcGmqplIt/5/09OzGdq3XJrGRPTarFydHuJo+GTljVjJnJSGfs4nTyLYAp2AlcyNJyG3dDL6mlcxZyZzV9/z4euxD291+n0Wm988+Yv0h1h+KvkH0e5N9BtRftcnmFiiKwrmVOM3HjEm2AOrirpAhxpx9ARYPC3/Ca+emaUyIXfPaY7rzYyfGm2pt/txG2+3m56Gk7Vg/RDiKdj/fN/+/vu6hz+bDuF3XYkVM5h/wOJvLsvr4lWP0F9SIXevO19zH6JCNXr69yymUr6UptVGtJeRD+cK05vsMAAAAAAAAAAAAAAAAAAAAAAAkR99N8gH6pG24MwAAAABJRU5ErkJggg==',
    '吳郭魚':   'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABkUlEQVR4nO3WsS9DQRwH8N+93F7XMJsoSQeGWiphICZiMhps/gAJOjf+BAsdjCZhEh0MaqgIkiaUyczSRYrhyb3k1fU5d+9VJeW+n+V3v773u7577+69Y2QxvzTnm46vr20a6/O5KUY9zCPHefSH5Gcm/NzkuHFG/usb8Bs8cpxHjvPIcR45jsnv/G3tPkhGs8NBjOY2tnpTfrR/zJJ8Bd6a73RxdtXR3kLWN19e6fL8plXPRZ9onaC2dbmNrf6n/VfK1a5vqrgQyg1Q2rrcxlafpP9Uqt9/elykgcEDajSeWafn2HAh0soFfbZ1uY2tPmn/cmA2cc4x4b2wBFZWl/36wx1lhkYojKXtvbYnOrsw3bYDPDk8ZepTl+tbrZcxumR0S4gnmQHF4lYQC4WNrs6A6OBl1Kld14OYHct8ORatl7FSrtKvvANEzN/j5nEvXjfwUNybGMXTylNR27q8tLtj7MxW/10eTvdw0LrByylv+m85vU31AAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAzvgAUhCfI+pctDMAAAAASUVORK5CYII=',
    '黃鱸(手改)': 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAB7ElEQVR4nO3WIUzDQBQG4FeyICrWLOnEzLJkBjVBEBMIFAgmUDhCFlA4EvQEmgSHYiEEh0IMj5gAg5iqmUEwsSZNKyowJdfS7Xbcto7eYCP/lyy93t4u9+7eXabRFO2LYhC3n309fFZ1nyb18f1nDUsjRVpX6+FcaievysbMqBiEJR8nPKkvLavrkmoZFYOwRPmE55E8s1Y2Fm8BqhOSFY/FUlZAZaM4aJecaALZXHE0hog8x6XSoMegSi7erbf/XQH0lbysLztYhCWuAM9x6fQhal/uRc+jG3fwzpJk39u2T3fH0VE4uPbJNHVq1tVO9s8qwLajhIY76oZ9RHq4QFH7+288hxa/ArynzSDe0WY9SpC98zuaBL9Aphn1sfdx48fv2a229lsV0D8shP8j8rc9bWoFmKYubSf9XlZBYh+7LGeR9g9QT1KpK+OCZWWdJpaPSRJvFozgvbMdsGeaGF7B1MNPogVIm4AKlZ0XJTF8BYhVkBkXLF56spIXz/xPzyWbFNsZ/ll5dEfKvXVeHtnlWqOr2b1hTJJxxDETV8C4W14FdiGJkxbLNGZZfviRSbKIMtpH/z7R+ZmX1fy+Ju4gf0tPqgAxprNrBLMkv1ALAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQIp8AtYOAgRc2c+qAAAAAElFTkSuQmCC',
}

# ── 工具函式 ────────────────────────────────────────────────────
def decode_skin_to_tmpfile(b64_str):
    """把 base64 PNG 解碼，儲存成暫存 PNG，回傳路徑"""
    data = base64.b64decode(b64_str)
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    tmp.write(data)
    tmp.close()
    return tmp.name

def bg(c, dark=False):
    c.setFillColor(DARK_BG if dark else PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def accent_bar_top(c, dark=False):
    """頂部藍色細線"""
    c.setStrokeColor(ACCENT)
    c.setLineWidth(2)
    c.line(0, H-2, W, H-2)

def chrome_min(c, left_txt, right_txt, dark=False):
    txt_col = WHITE if dark else GREY3
    c.setFont(MONO, 9)
    c.setFillColor(txt_col)
    c.drawString(32, H-22, left_txt.upper())
    c.drawRightString(W-32, H-22, right_txt.upper())
    c.setStrokeColor(GREY2 if not dark else colors.HexColor('#2a2a2a'))
    c.setLineWidth(0.5)
    c.line(32, H-28, W-32, H-28)

def footer(c, page_num, total=10, dark=False):
    txt_col = colors.HexColor('#555555') if dark else GREY3
    c.setFont(MONO, 8)
    c.setFillColor(txt_col)
    c.drawString(32, 16, f'EBREWING × AI AGENT  ·  2026.11')
    c.drawCentredString(W/2, 16, f'{page_num:02d} / {total:02d}')
    c.drawRightString(W-32, 16, 'NDHU')

def accent_block(c, x, y, w, h, text, font_size=11, text_color=WHITE):
    c.setFillColor(ACCENT)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont(ZH_B, font_size)
    c.drawCentredString(x + w/2, y + h/2 - font_size*0.35, text)

def card_fill(c, x, y, w, h, title, body, title_size=11, body_size=9):
    c.setFillColor(GREY1)
    c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(ACCENT)
    c.rect(x, y+h-3, w, 3, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont(ZH_B, title_size)
    c.drawString(x+10, y+h-title_size-10, title)
    c.setFont(ZH, body_size)
    c.setFillColor(GREY3)
    # 簡單換行
    words = body
    c.drawString(x+10, y+h-title_size-24, words[:28])
    if len(words) > 28:
        c.drawString(x+10, y+h-title_size-35, words[28:56])

def hairline(c, x1, y1, x2, y2, dark=False):
    c.setStrokeColor(GREY2 if not dark else colors.HexColor('#2a2a2a'))
    c.setLineWidth(0.5)
    c.line(x1, y1, x2, y2)

def draw_skin_pixelated(c, b64_str, x, y, size=80, label='', label_dark=False):
    """解碼並繪製魚皮膚"""
    path = decode_skin_to_tmpfile(b64_str)
    # 放大：PIL resample NEAREST 保持像素感
    img = Image.open(path).convert('RGBA')
    big = img.resize((size*4, size*4), Image.NEAREST)
    tmp2 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    big.save(tmp2.name)
    tmp2.close()
    c.drawImage(tmp2.name, x, y, width=size, height=size, preserveAspectRatio=True, mask='auto')
    # 框線
    c.setStrokeColor(GREY2)
    c.setLineWidth(0.5)
    c.rect(x, y, size, size, fill=0, stroke=1)
    # 標籤
    if label:
        lbl_col = WHITE if label_dark else GREY3
        c.setFont(ZH, 8)
        c.setFillColor(lbl_col)
        c.drawCentredString(x + size/2, y - 11, label)
    os.unlink(path)
    os.unlink(tmp2.name)

# ── 10 頁投影片 ─────────────────────────────────────────────────
def build_pdf(out_path):
    c = rl_canvas.Canvas(out_path, pagesize=(W, H))
    c.setTitle('ebrewing × AI Agent · 課堂報告')

    # ─ P1 封面 ─────────────────────────────────────────────────
    bg(c, dark=True)
    accent_bar_top(c, dark=True)
    # 大藍色標題塊
    c.setFillColor(ACCENT)
    c.rect(0, H*0.35, W*0.62, H*0.4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(ZH_B, 38)
    c.drawString(32, H*0.6, 'ebrewing × AI Agent')
    c.setFont(ZH, 14)
    c.setFillColor(colors.HexColor('#aaccff'))
    c.drawString(32, H*0.49, '用 Wiki 描述讓 AI 從零生成資料包與像素藝術')
    # 右側 meta 欄
    meta_x = W*0.66
    items = [
        ('COURSE', 'AI 應用與程式設計'),
        ('DATE',   '2026 · 11 · 01'),
        ('REPO',   'Eric200710 / mcepakc'),
        ('VER',    'Minecraft Java 1.21.1'),
    ]
    for i, (k, v) in enumerate(items):
        yy = H*0.72 - i*62
        c.setFillColor(GREY3)
        c.setFont(MONO, 8)
        c.drawString(meta_x, yy+14, k)
        c.setFillColor(WHITE)
        c.setFont(ZH, 11)
        c.drawString(meta_x, yy, v)
        hairline(c, meta_x, yy-6, W-32, yy-6, dark=True)
    chrome_min(c, 'NDHU / AI × MINECRAFT', 'AGENT SKILL DEMO', dark=True)
    footer(c, 1, dark=True)
    c.showPage()

    # ─ P2 問題 vs 解決方案 ──────────────────────────────────────
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'MOTIVATION · 01', 'WHY AGENT?')
    # 左右分割
    hairline(c, W/2, 60, W/2, H-40)
    # 左
    c.setFillColor(ACCENT)
    c.setFont(MONO, 9); c.drawString(32, H-60, 'BEFORE')
    c.setFillColor(INK)
    c.setFont(ZH_B, 26)
    c.drawString(32, H-110, '手寫 JSON')
    c.setFont(ZH_B, 26)
    c.drawString(32, H-142, '曠日費時')
    c.setFont(ZH, 11); c.setFillColor(GREY3)
    lines_l = [
        '每個物品 = 3 種文件',
        'advancement / loot_table / function',
        '61 杯飲料 × 3 = 183+ 個 JSON',
        '133 魚條目 × 生態域 = 手動爆炸',
        '',
        '出錯率高 · 格式繁瑣 · 重複性極強',
    ]
    for i, ln in enumerate(lines_l):
        c.drawString(32, H-180 - i*17, ln)
    # 右
    c.setFillColor(ACCENT)
    c.setFont(MONO, 9); c.drawString(W/2+24, H-60, 'AFTER')
    c.setFillColor(INK)
    c.setFont(ZH_B, 26)
    c.drawString(W/2+24, H-110, 'AI Agent')
    c.setFont(ZH_B, 26)
    c.drawString(W/2+24, H-142, '一句話搞定')
    c.setFont(ZH, 11); c.setFillColor(GREY3)
    lines_r = [
        '描述創意 → Skill 自動生成所有格式',
        '自動驗證 · 去重 · 注入戰利品表',
        '減壓腳本讓 AI 只處理創意部分',
        'Token 消耗降低 10×',
        '',
        '可複用 · 可擴充 · 零版權問題',
    ]
    for i, ln in enumerate(lines_r):
        c.drawString(W/2+24, H-180 - i*17, ln)
    footer(c, 2)
    c.showPage()

    # ─ P3 四大 Skill 時間線 ─────────────────────────────────────
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'SYSTEM OVERVIEW · 02', '4 AGENT SKILLS')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '四大 Agent Skill 工作流')
    # 時間軸橫線
    TL_Y = H/2 - 10
    c.setStrokeColor(GREY2); c.setLineWidth(1.5)
    c.line(60, TL_Y, W-60, TL_Y)
    skills = [
        ('01', 'ebrewing-\ndrink-builder', '輸入創意描述\n→ 自動生成飲料 JSON\n+ advancement'),
        ('02', 'ebrewing-\nspecial-builder', '特殊效果設定\n→ 觸發函數\n+ 消費 advancement 鏈'),
        ('03', 'ebrewing-\nfish-builder', '魚種規格 JSON\n→ 自動注入\n12 個生態域戰利品表'),
        ('04', 'minecraft-skin-\ngenerator', 'Wiki 文字描述\n→ 程序化繪製\n64×64 像素藝術 PNG'),
    ]
    spacing = (W - 120) / 4
    for i, (num, name, desc) in enumerate(skills):
        cx = 60 + spacing * i + spacing/2
        # 節點圓點
        c.setFillColor(ACCENT); c.setStrokeColor(PAPER)
        c.setLineWidth(2)
        c.circle(cx, TL_Y, 10, fill=1, stroke=1)
        c.setFillColor(WHITE); c.setFont(SANS_B, 9)
        c.drawCentredString(cx, TL_Y-3.5, num)
        # 上方名稱
        c.setFillColor(INK); c.setFont(ZH_B, 10)
        for j, part in enumerate(name.split('\n')):
            c.drawCentredString(cx, TL_Y + 28 + (len(name.split('\n'))-1-j)*14, part)
        # 下方描述
        c.setFillColor(GREY3); c.setFont(ZH, 8.5)
        for j, part in enumerate(desc.split('\n')):
            c.drawCentredString(cx, TL_Y - 35 - j*13, part)
    footer(c, 3)
    c.showPage()

    # ─ P4 Wiki → 像素藝術系統圖（dark）──────────────────────────
    bg(c, dark=True)
    accent_bar_top(c, dark=True)
    chrome_min(c, 'SKILL ANATOMY · 03', 'WIKI → PIXEL ART', dark=True)
    c.setFillColor(WHITE); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, 'Skill 解剖：Wiki → 像素藝術')

    layers = [
        (ACCENT,                    WHITE,  '輸入層', 'Wikipedia API  →  物種學名 / 形態 / 體色描述文字'),
        (colors.HexColor('#1a3a7a'), WHITE,  '處理層', 'procedural_aquatic_generator.py  →  UV 佈局解析 / 身體形狀模板 / 條紋演算 / 眼口外層疊加'),
        (colors.HexColor('#0a2050'), colors.HexColor('#aaccff'), '輸出層', '64×64 PNG  →  Base64 encode  →  minecraft:profile 寫入玩家頭顱'),
    ]
    box_h = 72; gap = 18; start_y = H - 130
    for i, (bg_c, fg_c, lbl, desc) in enumerate(layers):
        by = start_y - i*(box_h + gap)
        c.setFillColor(bg_c)
        c.rect(32, by, W-64, box_h, fill=1, stroke=0)
        c.setFillColor(fg_c)
        c.setFont(MONO, 8); c.drawString(44, by+box_h-16, lbl.upper())
        c.setFont(ZH, 11); c.drawString(44, by+box_h-38, desc)
        # 箭頭（除最後一個）
        if i < len(layers)-1:
            arr_y = by - gap/2
            c.setFillColor(GREY3)
            c.setFont(SANS, 14); c.drawCentredString(W/2, arr_y-6, '▼')

    # 右側重點
    notes = ['· 魚 / 甲殼類 / 軟體動物 / 頭足類 各自對應模板',
             '· 外層帽子 UV (32..63) 做 3D 鰭片 / 眼睛 / 嘴',
             '· 無版權問題 · Token 消耗僅 1/10']
    c.setFillColor(colors.HexColor('#aaccff'))
    c.setFont(ZH, 9.5)
    for i, n in enumerate(notes):
        c.drawString(44, 52 - i*16, n)

    footer(c, 4, dark=True)
    c.showPage()

    # ─ P5 魚皮膚展示 ────────────────────────────────────────────
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'PIXEL ART SHOWCASE · 04', 'PROCEDURAL FISH SKINS')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '程序化生成的魚皮膚')

    skins_list = list(SKIN_B64.items())  # 5 隻魚
    skin_size = 100
    total_w = len(skins_list) * skin_size + (len(skins_list)-1) * 36
    start_x = (W - total_w) / 2
    skin_y = H/2 - skin_size/2 - 10

    for i, (name, b64) in enumerate(skins_list):
        sx = start_x + i * (skin_size + 36)
        draw_skin_pixelated(c, b64, sx, skin_y, size=skin_size, label=name)

    # KPI 三欄
    kpis = [('5', '魚種'), ('64×64', '像素解析度'), ('0', '版權問題')]
    kw = 180
    kx_start = (W - kw*3 - 40) / 2
    for i, (num, lbl) in enumerate(kpis):
        kx = kx_start + i*(kw+20)
        c.setFillColor(ACCENT); c.setFont(ZH_B, 28)
        c.drawCentredString(kx+kw/2, 68, num)
        c.setFillColor(GREY3); c.setFont(ZH, 10)
        c.drawCentredString(kx+kw/2, 52, lbl)
        if i < 2:
            hairline(c, kx+kw+10, 44, kx+kw+10, 88)

    footer(c, 5)
    c.showPage()

    # ─ P6 減壓腳本閉環（dark）────────────────────────────────────
    bg(c, dark=True)
    accent_bar_top(c, dark=True)
    chrome_min(c, 'AUTOMATION · 05', 'DECOMPRESSION SCRIPT LOOP', dark=True)
    c.setFillColor(WHITE); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '減壓腳本工作閉環')

    cx_loop, cy_loop = W/2, H/2 - 10
    r_loop = 130
    loop_steps = [
        (0,   'AI 生成規格 JSON',    '名稱 / 效果 / 描述 / 貼圖 Base64'),
        (90,  'add_fish.py 解析',   '建構 loot_table Entry 物件'),
        (180, '自動注入生態域 JSON', '去重保留 · UTF-8 驗證'),
        (270, '/reload 即時生效',   'Minecraft 無需重啟伺服器'),
    ]
    import math
    for ang, title, sub in loop_steps:
        rad = math.radians(ang)
        bx = cx_loop + r_loop * math.sin(rad)
        by = cy_loop + r_loop * math.cos(rad)
        # 節點圓
        c.setFillColor(ACCENT); c.circle(bx, by, 18, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont(ZH_B, 8)
        c.drawCentredString(bx, by-3, title[:6])
        # 箭頭方向的說明文字
        tx = bx + 30*math.sin(rad) * (1 if ang in [0,90] else -1.2)
        ty = by + 16*math.cos(rad) * (1 if ang in [90,180] else -1.5) + (24 if ang == 0 else 0)
        c.setFillColor(WHITE); c.setFont(ZH_B, 10)
        c.drawCentredString(tx + (70 if ang == 0 else -70 if ang == 180 else 0),
                            by + (40 if ang == 90 else -40 if ang == 270 else 0), title)
        c.setFillColor(GREY3); c.setFont(ZH, 9)
        c.drawCentredString(tx + (70 if ang == 0 else -70 if ang == 180 else 0),
                            by + (24 if ang == 90 else -56 if ang == 270 else -16), sub)
    # 圓環虛線
    c.setStrokeColor(colors.HexColor('#2a4a8a')); c.setLineWidth(1.5)
    c.setDash([6, 4])
    c.circle(cx_loop, cy_loop, r_loop, fill=0, stroke=1)
    c.setDash()
    # 中心
    c.setFillColor(colors.HexColor('#0a1a4a'))
    c.circle(cx_loop, cy_loop, 32, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.setFont(ZH_B, 9)
    c.drawCentredString(cx_loop, cy_loop+4, '自動化')
    c.setFillColor(GREY3); c.setFont(ZH, 8)
    c.drawCentredString(cx_loop, cy_loop-8, 'LOOP')

    footer(c, 6, dark=True)
    c.showPage()

    # ─ P7 資料包規模橫條圖 ──────────────────────────────────────
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'DATAPACK STATS · 06', 'BY THE NUMBERS')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '資料包規模一覽')

    bars = [
        ('自訂飲料',   61,  200, '三品質階層 · Sugar / Golden / Diamond'),
        ('釣魚條目',  133,  200, '含傳說魚王 · 各生態域獨立機率'),
        ('Advancements', 73, 200, '含消費觸發鏈 · 標籤百科'),
        ('生態域分表',  12,  200, '熱帶→深海→地底→天空全覆蓋'),
        ('Agent Skills', 4,  200, '可複用減壓腳本工具包'),
    ]
    max_val = 133
    bar_h = 28; gap = 16; lbl_w = 130; num_w = 50
    avail_w = W - 64 - lbl_w - num_w - 20
    start_y_bars = H - 105
    for i, (label, val, _, desc) in enumerate(bars):
        by = start_y_bars - i*(bar_h + gap)
        bar_w = avail_w * val / max_val
        # 標籤
        c.setFillColor(INK); c.setFont(ZH, 11)
        c.drawRightString(32 + lbl_w, by + bar_h/2 - 4, label)
        # 底部灰條
        c.setFillColor(GREY1)
        c.rect(32 + lbl_w + 8, by, avail_w, bar_h, fill=1, stroke=0)
        # 實際藍條
        c.setFillColor(ACCENT)
        c.rect(32 + lbl_w + 8, by, bar_w, bar_h, fill=1, stroke=0)
        # 數字
        c.setFillColor(INK); c.setFont(SANS_B, 13)
        c.drawString(32 + lbl_w + 8 + bar_w + 6, by + bar_h/2 - 5, str(val))
        # 說明
        c.setFillColor(GREY3); c.setFont(ZH, 8)
        c.drawString(32 + lbl_w + 8 + avail_w + num_w - 10, by + bar_h/2 - 4, desc)

    footer(c, 7)
    c.showPage()

    # ─ P8 物品展示牆 ────────────────────────────────────────────
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'ITEM SYSTEM · 07', 'AUTO-GENERATED ITEMS')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '自動生成的物品體系')

    cards = [
        ('🧪', '基礎藥水', 'Sugar Tier', '23 種 · 一般魔藥與特調飲料，每杯含獨立效果配方'),
        ('🥃', '世界名酒', 'Golden Tier','12 種 · 威士忌/伏特加/龍舌蘭，附真實風味 lore'),
        ('🍺', '酒精系列', 'Alcohol',   '7 種 · 啤酒與烈酒，飲用後觸發特殊 debuff'),
        ('✨', '特殊調酒', 'Special Brew','14 種 · 自訂消費觸發 advancement 鏈'),
        ('🐟', '普通魚種', 'Biome Fish', '依生態域隨機 · 帶飽食效果 · 成對生成'),
        ('👑', '傳說魚王', 'King Fish',  '極低機率 · 雙倍效果 · dark_red 稀有品質'),
    ]
    cols = 3; card_w = (W - 80) / cols; card_h = 100; rows_c = 2
    for i, (emoji, title, sub, desc) in enumerate(cards):
        col = i % cols; row = i // cols
        cx2 = 32 + col * (card_w + 8)
        cy2 = H - 120 - row * (card_h + 12)
        c.setFillColor(GREY1)
        c.rect(cx2, cy2, card_w, card_h, fill=1, stroke=0)
        # accent 頂線
        c.setFillColor(ACCENT)
        c.rect(cx2, cy2+card_h-3, card_w, 3, fill=1, stroke=0)
        # emoji（用文字替代）
        c.setFillColor(INK); c.setFont(ZH, 22)
        c.drawString(cx2+10, cy2+card_h-36, emoji)
        c.setFont(ZH_B, 12)
        c.drawString(cx2+46, cy2+card_h-28, title)
        c.setFillColor(ACCENT); c.setFont(MONO, 8)
        c.drawString(cx2+46, cy2+card_h-42, sub)
        c.setFillColor(GREY3); c.setFont(ZH, 8.5)
        c.drawString(cx2+10, cy2+card_h-58, desc[:32])
        if len(desc) > 32:
            c.drawString(cx2+10, cy2+card_h-70, desc[32:])

    footer(c, 8)
    c.showPage()

    # ─ P9 核心金句（dark）────────────────────────────────────────
    bg(c, dark=True)
    accent_bar_top(c, dark=True)
    chrome_min(c, 'STATEMENT · 08', 'CORE INSIGHT', dark=True)

    c.setFillColor(ACCENT)
    c.rect(0, H*0.38, W, H*0.31, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont(ZH_B, 28)
    c.drawCentredString(W/2, H*0.56, '「一段 Wiki 描述，')
    c.drawCentredString(W/2, H*0.56-38, '  AI 即刻化為像素生命」')

    c.setFillColor(GREY3); c.setFont(ZH, 11)
    sub_lines = [
        'Wiki API  →  形態解析  →  程序化繪製  →  資料包注入',
        '全流程自動化 · 從描述到遊戲內物品只需一條指令',
    ]
    for i, ln in enumerate(sub_lines):
        c.drawCentredString(W/2, H*0.33 - i*18, ln)

    # 點陣裝飾
    c.setFillColor(colors.HexColor('#1a2a5a'))
    for row in range(8):
        for col in range(22):
            px = col * 44 + 20; py = 28 + row * 12
            c.circle(px, py, 1.2, fill=1, stroke=0)

    footer(c, 9, dark=True)
    c.showPage()

    # ─ P10 結語（dark）───────────────────────────────────────────
    bg(c, dark=True)
    accent_bar_top(c, dark=True)
    chrome_min(c, 'CLOSING · 09', 'THANK YOU', dark=True)

    # 左半大字
    c.setFillColor(WHITE); c.setFont(ZH_B, 48)
    c.drawString(32, H*0.6, 'Thank')
    c.drawString(32, H*0.6-56, 'You')
    c.setFillColor(ACCENT); c.setFont(ZH, 14)
    c.drawString(32, H*0.6-90, 'AI × Minecraft Datapack Automation')

    hairline(c, W/2, 60, W/2, H-40, dark=True)

    # 右半資訊
    rx = W/2 + 28
    items2 = [
        ('GITHUB', 'github.com/Eric200710/mcepakc'),
        ('ENGINE', 'Antigravity AI Agent + Python'),
        ('TARGET', 'Minecraft Java Edition 1.21.1'),
        ('SKILLS', '4 個可複用 Agent Skill 腳本'),
        ('ITEMS',  '61 飲料 · 133 魚條目 · 73 advancements'),
    ]
    for i, (k, v) in enumerate(items2):
        yy = H*0.73 - i*58
        c.setFillColor(GREY3); c.setFont(MONO, 8)
        c.drawString(rx, yy+14, k)
        c.setFillColor(WHITE); c.setFont(ZH, 12)
        c.drawString(rx, yy, v)
        hairline(c, rx, yy-8, W-32, yy-8, dark=True)

    footer(c, 10, dark=True)
    c.showPage()

    c.save()
    print(f'[完成] PDF 輸出至：{out_path}')

# ── 執行 ────────────────────────────────────────────────────────
os.makedirs(r'D:\ag\mcepack\ppt', exist_ok=True)
build_pdf(r'D:\ag\mcepack\ppt\ebrewing_report.pdf')
