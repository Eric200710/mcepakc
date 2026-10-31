# -*- coding: utf-8 -*-
"""
ebrewing × AI Agent — 課堂報告 PDF 生成腳本 (繁體中文微軟正黑體修復版)
Swiss Style · IKB 克萊因藍 · 16:9 (960×540pt)
"""
import sys, io, os, base64, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from PIL import Image, ImageDraw, ImageFont
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

# ── 字型 (使用標準微軟正黑體，完整支援繁體中文不缺字) ───────────────
FONT_DIR = r'C:\Windows\Fonts'
pdfmetrics.registerFont(TTFont('MSJH', os.path.join(FONT_DIR, 'msjh.ttc'), subfontIndex=0))
pdfmetrics.registerFont(TTFont('MSJH-Bold', os.path.join(FONT_DIR, 'msjhbd.ttc'), subfontIndex=0))

ZH = 'MSJH'
ZH_B = 'MSJH-Bold'
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
EMOJI_CACHE = {}

def get_emoji_image(emoji_char, size=48):
    """將 Emoji 透過 Windows 系統字型渲染為 PNG 圖片，避免 PDF 字型不支援出現方塊"""
    if emoji_char in EMOJI_CACHE:
        return EMOJI_CACHE[emoji_char]
    font_path = r'C:\Windows\Fonts\seguiemj.ttf'
    img = Image.new('RGBA', (size*2, size*2), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    try:
        f = ImageFont.truetype(font_path, int(size*1.3))
        d.text((size*0.35, size*0.1), emoji_char, font=f, embedded_color=True)
    except:
        f = ImageFont.truetype(r'C:\Windows\Fonts\msjhbd.ttc', int(size))
        d.text((size*0.2, size*0.2), emoji_char, fill=(0,0,0,255), font=f)
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    img.save(tmp.name)
    tmp.close()
    EMOJI_CACHE[emoji_char] = tmp.name
    return tmp.name

def decode_skin_to_tmpfile(b64_str):
    data = base64.b64decode(b64_str)
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    tmp.write(data)
    tmp.close()
    return tmp.name

def bg(c, dark=False):
    c.setFillColor(DARK_BG if dark else PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def accent_bar_top(c, dark=False):
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
    c.drawString(32, 16, 'EBREWING × AI AGENT  ·  2026.11')
    c.drawCentredString(W/2, 16, f'{page_num:02d} / {total:02d}')
    c.drawRightString(W-32, 16, 'NDHU')

def hairline(c, x1, y1, x2, y2, dark=False):
    c.setStrokeColor(GREY2 if not dark else colors.HexColor('#2a2a2a'))
    c.setLineWidth(0.5)
    c.line(x1, y1, x2, y2)

def draw_skin_pixelated(c, b64_str, x, y, size=80, label='', label_dark=False):
    path = decode_skin_to_tmpfile(b64_str)
    img = Image.open(path).convert('RGBA')
    big = img.resize((size*4, size*4), Image.NEAREST)
    tmp2 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    big.save(tmp2.name)
    tmp2.close()
    c.drawImage(tmp2.name, x, y, width=size, height=size, preserveAspectRatio=True, mask='auto')
    c.setStrokeColor(GREY2)
    c.setLineWidth(0.5)
    c.rect(x, y, size, size, fill=0, stroke=1)
    if label:
        lbl_col = WHITE if label_dark else GREY3
        c.setFont(ZH, 8.5)
        c.setFillColor(lbl_col)
        c.drawCentredString(x + size/2, y - 13, label)
    os.unlink(path)
    os.unlink(tmp2.name)

# ── 10 頁投影片 ─────────────────────────────────────────────────
def build_pdf(out_path):
    c = rl_canvas.Canvas(out_path, pagesize=(W, H))
    c.setTitle('ebrewing × AI Agent · 課堂報告')

    # ─ P1 封面 ─────────────────────────────────────────────────
    bg(c, dark=True)
    accent_bar_top(c, dark=True)
    c.setFillColor(ACCENT)
    c.rect(0, H*0.35, W*0.62, H*0.4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(ZH_B, 36)
    c.drawString(32, H*0.6, 'ebrewing × AI Agent')
    c.setFont(ZH, 14)
    c.setFillColor(colors.HexColor('#aaccff'))
    c.drawString(32, H*0.49, '從 Wiki 描述到遊戲內像素實體：資料包自動化工程')
    meta_x = W*0.66
    items = [
        ('COURSE', 'AI 應用與程式設計專題'),
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

    # ─ P2 痛點 vs 解決方案 ──────────────────────────────────────
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'MOTIVATION · 01', 'WHY AGENT?')
    hairline(c, W/2, 60, W/2, H-40)
    # 左側
    c.setFillColor(ACCENT)
    c.setFont(MONO, 9); c.drawString(32, H-60, 'BEFORE · 手工配置痛點')
    c.setFillColor(INK)
    c.setFont(ZH_B, 26)
    c.drawString(32, H-110, '手寫 JSON')
    c.drawString(32, H-142, '耗時且易錯')
    c.setFont(ZH, 11); c.setFillColor(GREY3)
    lines_l = [
        '單一物品需維護：advancement、loot_table、function',
        '61 杯自訂飲料 × 3 類關聯檔案 = 183+ 個 JSON',
        '133 條釣魚條目 × 12 種生態域 = 龐大重複性工作',
        '括號遺漏、標籤格式錯誤即導致資料包載入失敗',
        '',
        '傳統開發模式阻礙創意，重複勞動占比過高',
    ]
    for i, ln in enumerate(lines_l):
        c.drawString(32, H-180 - i*18, ln)
    # 右側
    c.setFillColor(ACCENT)
    c.setFont(MONO, 9); c.drawString(W/2+24, H-60, 'AFTER · 智慧減壓架構')
    c.setFillColor(INK)
    c.setFont(ZH_B, 26)
    c.drawString(W/2+24, H-110, 'AI Agent')
    c.drawString(W/2+24, H-142, '創意即刻成型')
    c.setFont(ZH, 11); c.setFillColor(GREY3)
    lines_r = [
        'AI 專注於名稱、風味描述、特殊效果與色彩規劃',
        '減壓腳本自動處理組件語法、去重與戰利品表注入',
        'Token 消耗減少 90% 以上，避免長篇上下文膨脹',
        'Minecraft 1.21.1 custom_data 與 profile 一鍵封裝',
        '',
        '兼具高度可複用性、系統穩定度與零版權風險',
    ]
    for i, ln in enumerate(lines_r):
        c.drawString(W/2+24, H-180 - i*18, ln)
    footer(c, 2)
    c.showPage()

    # ─ P3 四大 Skill 時間線 ─────────────────────────────────────
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'SYSTEM OVERVIEW · 02', '4 AGENT SKILLS')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '四大模組化 Agent Skill 架構')
    TL_Y = H/2 - 10
    c.setStrokeColor(GREY2); c.setLineWidth(1.5)
    c.line(60, TL_Y, W-60, TL_Y)
    skills = [
        ('01', 'ebrewing-\ndrink-builder', '飲料自動生成\n輸入風味與配方\n自動生成進度與標籤'),
        ('02', 'ebrewing-\nspecial-builder', '特殊釀造擴充\n客製飲用觸發事件\n自動綁定函數指令鏈'),
        ('03', 'ebrewing-\nfish-builder', '成對魚種生成\n普通版 + 傳奇魚王\n自動注入 12 生態域池'),
        ('04', 'minecraft-skin-\ngenerator', '程序化生物繪圖\nWiki 描述轉特徵\n生成 64×64 頭顱貼圖'),
    ]
    spacing = (W - 120) / 4
    for i, (num, name, desc) in enumerate(skills):
        cx = 60 + spacing * i + spacing/2
        c.setFillColor(ACCENT); c.setStrokeColor(PAPER)
        c.setLineWidth(2)
        c.circle(cx, TL_Y, 11, fill=1, stroke=1)
        c.setFillColor(WHITE); c.setFont(SANS_B, 9)
        c.drawCentredString(cx, TL_Y-3.5, num)
        c.setFillColor(INK); c.setFont(ZH_B, 10.5)
        for j, part in enumerate(name.split('\n')):
            c.drawCentredString(cx, TL_Y + 28 + (len(name.split('\n'))-1-j)*14, part)
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
    c.drawString(32, H-68, '技能技術解剖：從百科描述到像素藝術')

    layers = [
        (ACCENT, WHITE, '輸入層 · 資料採集', 'Wikipedia API 擷取學名、背鰭構造、側線斑紋、體態特徵等結構化文本'),
        (colors.HexColor('#1a3a7a'), WHITE, '處理層 · 程序化演算', '解析 MC 頭顱 UV 映射：內層 32×16 基礎軀幹 + 外層帽子 32×16 立體凸起 (眼/鰭/口)'),
        (colors.HexColor('#0a2050'), colors.HexColor('#aaccff'), '輸出層 · 遊戲實體注入', '產生標準 64×64 PNG → Base64 編碼 → 自動寫入 player_head textures 屬性'),
    ]
    box_h = 72; gap = 18; start_y = H - 130
    for i, (bg_c, fg_c, lbl, desc) in enumerate(layers):
        by = start_y - i*(box_h + gap)
        c.setFillColor(bg_c)
        c.rect(32, by, W-64, box_h, fill=1, stroke=0)
        c.setFillColor(fg_c)
        c.setFont(ZH_B, 9); c.drawString(44, by+box_h-16, lbl)
        c.setFont(ZH, 11); c.drawString(44, by+box_h-38, desc)
        if i < len(layers)-1:
            arr_y = by - gap/2
            c.setFillColor(GREY3)
            c.setFont(ZH, 14); c.drawCentredString(W/2, arr_y-6, '▼')

    notes = [
        '◆ 支援硬骨魚、軟骨魚、甲殼類、雙殼貝與頭足類等多生物模板切換',
        '◆ 外層帽子圖層具備 0.5 像素視覺浮雕，呈現精緻立體背鰭與外凸眼珠',
        '◆ 產出兼具輕量、零侵權風險與高辨識度之 Minecraft 原生美學',
    ]
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
    c.drawString(32, H-68, '程序化像素魚皮膚實體展示')

    skins_list = list(SKIN_B64.items())
    skin_size = 100
    total_w = len(skins_list) * skin_size + (len(skins_list)-1) * 36
    start_x = (W - total_w) / 2
    skin_y = H/2 - skin_size/2 - 10

    for i, (name, b64) in enumerate(skins_list):
        sx = start_x + i * (skin_size + 36)
        draw_skin_pixelated(c, b64, sx, skin_y, size=skin_size, label=name)

    kpis = [('5 款', '生物模板庫展示'), ('64×64', '標準頭顱解析度'), ('0 侵權', '完全自主程序化演算法')]
    kw = 180
    kx_start = (W - kw*3 - 40) / 2
    for i, (num, lbl) in enumerate(kpis):
        kx = kx_start + i*(kw+20)
        c.setFillColor(ACCENT); c.setFont(ZH_B, 24)
        c.drawCentredString(kx+kw/2, 68, num)
        c.setFillColor(GREY3); c.setFont(ZH, 10)
        c.drawCentredString(kx+kw/2, 50, lbl)
        if i < 2:
            hairline(c, kx+kw+10, 44, kx+kw+10, 88)

    footer(c, 5)
    c.showPage()

    # ─ P6 減壓腳本閉環（dark）────────────────────────────────────
    bg(c, dark=True)
    accent_bar_top(c, dark=True)
    chrome_min(c, 'AUTOMATION · 05', 'DECOMPRESSION SCRIPT LOOP', dark=True)
    c.setFillColor(WHITE); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '自動化減壓腳本執行閉環')

    cx_loop, cy_loop = W/2, H/2 - 10
    r_loop = 130
    loop_steps = [
        (0,   'AI 產出規格 JSON',     '名稱 / 數值 / 描述 / Base64'),
        (90,  '減壓腳本自動解析',    '建構標準 loot_table 物件'),
        (180, '注入生態域戰利品表', '去重排程 · UTF-8 格式校驗'),
        (270, '遊戲內 /reload 即用', '熱重載立即生效，無需重啟'),
    ]
    for ang, title, sub in loop_steps:
        rad = math.radians(ang)
        bx = cx_loop + r_loop * math.sin(rad)
        by = cy_loop + r_loop * math.cos(rad)
        c.setFillColor(ACCENT); c.circle(bx, by, 18, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont(ZH_B, 8)
        c.drawCentredString(bx, by-3, title[:6])
        tx = bx + 30*math.sin(rad) * (1 if ang in [0,90] else -1.2)
        ty = by + 16*math.cos(rad) * (1 if ang in [90,180] else -1.5) + (24 if ang == 0 else 0)
        c.setFillColor(WHITE); c.setFont(ZH_B, 10.5)
        c.drawCentredString(tx + (70 if ang == 0 else -70 if ang == 180 else 0),
                            by + (40 if ang == 90 else -40 if ang == 270 else 0), title)
        c.setFillColor(GREY3); c.setFont(ZH, 9)
        c.drawCentredString(tx + (70 if ang == 0 else -70 if ang == 180 else 0),
                            by + (24 if ang == 90 else -56 if ang == 270 else -16), sub)
    c.setStrokeColor(colors.HexColor('#2a4a8a')); c.setLineWidth(1.5)
    c.setDash([6, 4])
    c.circle(cx_loop, cy_loop, r_loop, fill=0, stroke=1)
    c.setDash()
    c.setFillColor(colors.HexColor('#0a1a4a'))
    c.circle(cx_loop, cy_loop, 32, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.setFont(ZH_B, 9.5)
    c.drawCentredString(cx_loop, cy_loop+4, '閉環流程')
    c.setFillColor(GREY3); c.setFont(ZH, 8)
    c.drawCentredString(cx_loop, cy_loop-8, 'LOOP')

    footer(c, 6, dark=True)
    c.showPage()

    # ─ P7 資料包規模橫條圖 ──────────────────────────────────────
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'DATAPACK STATS · 06', 'BY THE NUMBERS')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '資料包實體規模統計一覽')

    bars = [
        ('自訂特調飲料', 61,  '三種品質階層 · 涵蓋 16 色系自訂標籤與百科條目'),
        ('釣魚戰利品條目', 133, '成對設計 · 包含普通魚種與極低機率傳奇魚王'),
        ('進度成就節點', 73,  '樹狀結構 · 完整飲用消耗判定與合成進度鏈'),
        ('生態域專屬水域', 12,  '淺海/深海/河流/天空/地底/深暗全維度分流'),
        ('模組化技能工具', 4,   '完全自動化 Python 減壓指令腳本'),
    ]
    max_val = 133
    bar_h = 28; gap = 16; lbl_w = 140; num_w = 50
    avail_w = W - 64 - lbl_w - num_w - 20
    start_y_bars = H - 105
    for i, (label, val, desc) in enumerate(bars):
        by = start_y_bars - i*(bar_h + gap)
        bar_w = avail_w * val / max_val
        c.setFillColor(INK); c.setFont(ZH, 11)
        c.drawRightString(32 + lbl_w, by + bar_h/2 - 4, label)
        c.setFillColor(GREY1)
        c.rect(32 + lbl_w + 8, by, avail_w, bar_h, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(32 + lbl_w + 8, by, bar_w, bar_h, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont(SANS_B, 13)
        c.drawString(32 + lbl_w + 8 + bar_w + 6, by + bar_h/2 - 5, str(val))
        c.setFillColor(GREY3); c.setFont(ZH, 8.5)
        c.drawString(32 + lbl_w + 8 + avail_w + num_w - 10, by + bar_h/2 - 4, desc)

    footer(c, 7)
    c.showPage()

    # ─ P8 物品展示牆 (Emoji 圖片化，徹底解決方塊破圖) ──────────────
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'ITEM SYSTEM · 07', 'AUTO-GENERATED ITEMS')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '自動生成的龐大物品體系')

    cards = [
        ('🧪', '基礎常規藥水', 'Sugar Tier', '23 種 · 傳統藥水特調風格，每款具備專屬增益與冷卻機制'),
        ('🥃', '世界經典名酒', 'Golden Tier','12 種 · 威士忌/琴酒/龍舌蘭，附考究產地 lore 描述'),
        ('🍺', '酒精特調系列', 'Alcohol',   '7 種 · 啤酒與陳釀烈酒，飲用後觸發專屬醉酒視覺反應'),
        ('✨', '傳奇特殊調酒', 'Special Brew','14 種 · 複雜合成公式，自動綁定 advancement 偵測執行函數'),
        ('🐟', '生態域常態魚', 'Biome Fish', '依水域與深度隨機分佈，提供不同飽食度與短暫屬性加成'),
        ('👑', '傳奇深海魚王', 'King Fish',  '極低機率捕獲，暗紅特殊字色、雙倍增益與高達 10 倍飽和度'),
    ]
    cols = 3; card_w = (W - 80) / cols; card_h = 100
    for i, (emoji, title, sub, desc) in enumerate(cards):
        col = i % cols; row = i // cols
        cx2 = 32 + col * (card_w + 8)
        cy2 = H - 120 - row * (card_h + 12)
        c.setFillColor(GREY1)
        c.rect(cx2, cy2, card_w, card_h, fill=1, stroke=0)
        c.setFillColor(ACCENT)
        c.rect(cx2, cy2+card_h-3, card_w, 3, fill=1, stroke=0)
        # 繪製 Emoji 圖示 (避免缺字破圖)
        emoji_img = get_emoji_image(emoji, size=32)
        c.drawImage(emoji_img, cx2+8, cy2+card_h-38, width=30, height=30, preserveAspectRatio=True, mask='auto')
        c.setFillColor(INK); c.setFont(ZH_B, 12)
        c.drawString(cx2+44, cy2+card_h-26, title)
        c.setFillColor(ACCENT); c.setFont(MONO, 8)
        c.drawString(cx2+44, cy2+card_h-40, sub)
        c.setFillColor(GREY3); c.setFont(ZH, 8.5)
        c.drawString(cx2+10, cy2+card_h-58, desc[:28])
        if len(desc) > 28:
            c.drawString(cx2+10, cy2+card_h-72, desc[28:])

    footer(c, 8)
    c.showPage()

    # ─ P9 核心金句（dark）────────────────────────────────────────
    bg(c, dark=True)
    accent_bar_top(c, dark=True)
    chrome_min(c, 'STATEMENT · 08', 'CORE INSIGHT', dark=True)

    c.setFillColor(ACCENT)
    c.rect(0, H*0.38, W, H*0.31, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont(ZH_B, 28)
    c.drawCentredString(W/2, H*0.56, '「一段 Wiki 生物描述，')
    c.drawCentredString(W/2, H*0.56-38, '  AI 即刻化為遊戲內像素生命」')

    c.setFillColor(GREY3); c.setFont(ZH, 11)
    sub_lines = [
        '維基百科 API  →  生物形態演算法  →  程序化像素繪圖  →  資料包自動注入',
        '全流程無縫整合 · 實現從自然語言創意到遊戲實體的可複製自動化管線',
    ]
    for i, ln in enumerate(sub_lines):
        c.drawCentredString(W/2, H*0.33 - i*18, ln)

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

    c.setFillColor(WHITE); c.setFont(ZH_B, 48)
    c.drawString(32, H*0.6, 'Thank')
    c.drawString(32, H*0.6-56, 'You')
    c.setFillColor(ACCENT); c.setFont(ZH, 14)
    c.drawString(32, H*0.6-90, 'AI × Minecraft 資料包自動化專案')

    hairline(c, W/2, 60, W/2, H-40, dark=True)

    rx = W/2 + 28
    items2 = [
        ('GITHUB 專案庫', 'github.com/Eric200710/mcepakc'),
        ('核心開發架構', 'Antigravity AI Agent + Python 減壓工具鏈'),
        ('目標執行環境', 'Minecraft Java Edition 1.21.1 原生資料包'),
        ('模組化技能庫', '4 組具高通用性之自訂 Agent 技能'),
        ('自動化產出成果', '61 款自訂飲料 · 133 條魚類戰利品 · 73 項成就進度'),
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
    print(f'[成功] 繁體中文微軟正黑體 PDF 已重新生成：{out_path}')

# ── 執行 ────────────────────────────────────────────────────────
os.makedirs(r'D:\ag\mcepack\ppt', exist_ok=True)
build_pdf(r'D:\ag\mcepack\ppt\ebrewing_report.pdf')
