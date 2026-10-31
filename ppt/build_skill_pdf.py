# -*- coding: utf-8 -*-
"""
AI Agent Skill 專題深入報告 — PDF 生成腳本
專注：AI Agent Skill 系統架構、減壓腳本技術、程式碼範例展示、安裝與使用教學
16:9 (960×540pt) · Swiss Style (IKB 克萊因藍) · 微軟正黑體
"""
import sys, io, os, base64
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as rl_canvas
from PIL import Image, ImageDraw, ImageFont
import tempfile

# ── 尺寸 16:9 ──────────────────────────────────────────────────
W, H = 960, 540

# ── 配色 ───────────────────────────────────────────────────────
INK     = colors.HexColor('#0a0a0a')
PAPER   = colors.HexColor('#fafaf8')
GREY1   = colors.HexColor('#f0f0ee')
GREY2   = colors.HexColor('#d4d4d2')
GREY3   = colors.HexColor('#737373')
ACCENT  = colors.HexColor('#002FA7')   # IKB
CODE_BG = colors.HexColor('#16181d')   # 程式碼深色背景
WHITE   = colors.white
DARK_BG = colors.HexColor('#0f0f0f')

# ── 字型 ───────────────────────────────────────────────────────
FONT_DIR = r'C:\Windows\Fonts'
pdfmetrics.registerFont(TTFont('MSJH', os.path.join(FONT_DIR, 'msjh.ttc'), subfontIndex=0))
pdfmetrics.registerFont(TTFont('MSJH-Bold', os.path.join(FONT_DIR, 'msjhbd.ttc'), subfontIndex=0))

ZH = 'MSJH'
ZH_B = 'MSJH-Bold'
MONO = 'Courier'
MONO_B = 'Courier-Bold'
SANS = 'Helvetica'
SANS_B = 'Helvetica-Bold'

# ── 魚皮膚 Base64 ─────────────────────────────────────────────
CLOWN_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAABAUlEQVR4nO3WrZLCMBDA8U2mKEQRnOgJangcLBrPE/AIpxHnT5+9xwFRBDGYGgwizGLoMIXw0Ztpyf8300k63V2R5stIQJZlviiKUz/P81NbfV9NDzfz+8udkRazEjkrHeIXI68zMtoB+A9WImclclYiZyVy5tVzfvzbk1D+ZUy15iP3BD0FPn8O4px76m5Rl59Ih5ivjYlmCaTp0CttX4np7ACoweBDmoi5JZEW0H1oO+s9PN3L8rx/6PqufqvbK+pqWukQ//ft9WmyZhIKWLt9ICK9Iz8N1tQ/FmIm86uz4p781i4B9+Sx1nQNAAAAAAAAAAAAAAAAAAAAAAAgb+EIZahtPj4yi94AAAAASUVORK5CYII='
PERCH_B64 = 'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAEr0lEQVR4AexWPWwbZRh+7nw+O2ljY9ehsUKtJpGgKCRNRVQ6BFSJkYEBlbKgbkggKOLHSEwIBANq2dj4U2cWOnRnyIAYGOiABCogFgbShKRRHNvn+/iez1x6dzrncuGiE6fv5Mff+/O8333vj+9sIuZ697Uzon11Xrzefly88s4T4uX2eSkvi08/Pic+u3ZOXP/gjMLq9Zbww7PHbJ/I/db7K4JIFBRDji3AbnkcO+Xj2HUL6PVc9PsCnYGJn/+20XcNtf2F8R18tzMeAG3KmeLXH79ugkhxS8QWoOMYcAYCve4A/d5Arg6cvovdros7d4cFYPL+hCnTluZBuVdrtgoCKV6xBTCLFgayAK4r5AQM0JfJO44L1wU6wgKTHXWe/XyjYvazs/vEfpykvtgCQAiwz0KtUhKAIRdAqHVxuYWXnmrg9FwVLywUFSjTRh9SvNh9IsUt438ClRJgmAYsqwCraMIuFVAoGBImKrYAr62NTS4BRNkChEMo7D5xiNCRIeZIz7+O0zUX5ZIpkzdQkskXZRGKdgF20cDciQF4vfEN8OLnOxQVKNOmlBS/2H0ixS3jJ+CX7TIWTg6wcXcXRXs4AetrHSxOCfy0NQZ2em3tfvLe4Wijz9PTWNl9Io29vD3MrW9XxKUrCwpRMm94eUn+DmSE4wj1EJQiLi/Z6pXETt9sN9FojINypVZVMnXK4T3DOvc6KNh94qD8g/BMkh5t2ZhtFinCLy8/XFK6csivXtcBX4VSVB9yyaHCeOphOUonj3z6kuCT91YNIklMHFcVoNUwMVVTIvzyI1Mm3n56TO1Rr5fka9BFV/4fOFEvKxt95FBhPGPDcpROHvn0ZQ2V9YwswHRNifDLj01Ze+c7VS/Als+AUsnCQ/UhF/LyOIxnrDTBL0fp5JFD3wExfN0EyVG2ICOk8W804TerTOZkctNVQ9n98oPHlFvZnztr4dSkLWHh0tL9wngcxjOWZL8cpZNHDn1/XWkKPhe2v7TEvQ8h1l8dE7TR58PwcD6DFAM2xtz7CGL7C7nPrXm154/PNANF4vNMxgU+KsP6mInWA8Ok/LKfOV0x0L5oSRTRnAjcW9EYz1gqfjlKJ48c+iZv/Gl0v7oDd/YCjAnAsPoYdf1287wgRvmN49LTmIE4VsPv125j8dZm4KB8gIaLYJbnr4Colgy1hmXqHibW3wTh6f51v3i/z4vxbPLI2CvC2RU4G5NKpz2MmWe/N4iwnTr36PzQhFs9GZk8OUyeRaDsQU0AFR6MK+GXqXvoPynfAhKe7l/9MX6ZnLAeZWMClYurBlf6DwPGco9w5729vr5x2wi/RUx78nkjS3iHy2rdm4CsDpD1fXUBsu5A1vc/igkIvHuzTjDu/kdRgMC7N+4AWfuPogBZ55To/roAicqVQ7KegBw2NVFKegISlSuHZD0BOWxqopRyPwFx1dAFiKtQ3v16AvLe4bj89ATEVSjvfj0Bee9wXH56AuIqlHe/noC8dzguPz0BcRXKu19PQN46nDQfPQFJK5Y3vp6AvHU0aT56ApJWLG98PQF562jSfPQEJK1Y3vh6AvLW0aT56AlIWrG88fUE/N87+l/P/w8AAAD///OocmcAAAAGSURBVAMAGMKgkO/seZ0AAAAASUVORK5CYII='

# ── 工具函式 ────────────────────────────────────────────────────
def bg(c, dark=False):
    c.setFillColor(DARK_BG if dark else PAPER)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def accent_bar_top(c):
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

def footer(c, page_num, total=7, dark=False):
    txt_col = colors.HexColor('#555555') if dark else GREY3
    c.setFont(MONO, 8)
    c.setFillColor(txt_col)
    c.drawString(32, 16, 'AI AGENT SKILL ARCHITECTURE  ·  ANTIGRAVITY ECOSYSTEM')
    c.drawCentredString(W/2, 16, f'{page_num:02d} / {total:02d}')
    c.drawRightString(W-32, 16, 'ERIC200710')

def hairline(c, x1, y1, x2, y2, dark=False):
    c.setStrokeColor(GREY2 if not dark else colors.HexColor('#2a2a2a'))
    c.setLineWidth(0.5)
    c.line(x1, y1, x2, y2)

def draw_skin_img(c, b64_str, x, y, size=70, label=''):
    data = base64.b64decode(b64_str)
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    tmp.write(data)
    tmp.close()
    img = Image.open(tmp.name).convert('RGBA')
    big = img.resize((size*4, size*4), Image.NEAREST)
    tmp2 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    big.save(tmp2.name)
    tmp2.close()
    c.drawImage(tmp2.name, x, y, width=size, height=size, preserveAspectRatio=True, mask='auto')
    c.setStrokeColor(GREY2)
    c.setLineWidth(0.5)
    c.rect(x, y, size, size, fill=0, stroke=1)
    if label:
        c.setFont(ZH, 8.5)
        c.setFillColor(GREY3)
        c.drawCentredString(x + size/2, y - 12, label)
    os.unlink(tmp.name)
    os.unlink(tmp2.name)

# ── 7 頁核心投影片 ───────────────────────────────────────────────
def build_agent_skill_pdf(out_path):
    c = rl_canvas.Canvas(out_path, pagesize=(W, H))
    c.setTitle('AI Agent Skill 架構與減壓腳本技術深度報告')

    # ═════════════════════════════════════════════════════════════════
    # P1 封面：AI Agent Skill 核心概念
    # ═════════════════════════════════════════════════════════════════
    bg(c, dark=True)
    accent_bar_top(c)
    c.setFillColor(ACCENT)
    c.rect(0, H*0.35, W*0.62, H*0.4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont(ZH_B, 34)
    c.drawString(32, H*0.61, 'AI Agent Skill 架構設計')
    c.setFont(ZH, 14)
    c.setFillColor(colors.HexColor('#aaccff'))
    c.drawString(32, H*0.50, '解耦創意與重複性語法：減壓腳本技術與生態實踐')

    meta_x = W*0.66
    items = [
        ('TOPIC',    'AI Agent 模組化技能體系'),
        ('PARADIGM', '減壓腳本 (Decompression Script)'),
        ('ENGINE',   'Google Antigravity / Claude / GPT'),
        ('REPO',     'github.com/Eric200710/mcepakc'),
    ]
    for i, (k, v) in enumerate(items):
        yy = H*0.72 - i*62
        c.setFillColor(GREY3); c.setFont(MONO, 8)
        c.drawString(meta_x, yy+14, k)
        c.setFillColor(WHITE); c.setFont(ZH, 11)
        c.drawString(meta_x, yy, v)
        hairline(c, meta_x, yy-6, W-32, yy-6, dark=True)

    chrome_min(c, 'AI ARCHITECTURE · REPORT', 'SKILL-FIRST DESIGN', dark=True)
    footer(c, 1, dark=True)
    c.showPage()

    # ═════════════════════════════════════════════════════════════════
    # P2 什麼是 Agent Skill？薄上下文與厚能力的解法
    # ═════════════════════════════════════════════════════════════════
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'CONCEPT · 01', 'WHAT IS AGENT SKILL?')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '什麼是 Agent Skill？為什麼需要它？')

    # 左側：問題對比
    c.setFillColor(GREY1); c.rect(32, 60, 420, H-150, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.rect(32, H-93, 420, 3, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(ZH_B, 14); c.drawString(48, H-120, '傳統 Prompt / 人工手寫模式')
    bad_points = [
        '◆ 上下文耗損極大：每次都要向模型重複解釋數百行語法規則',
        '◆ 幻覺與格式錯誤：JSON 括號不對稱、版本標籤混淆 (1.20 vs 1.21)',
        '◆ 輸出重複勞動：AI 大量時間都在吐重複的固定樣板代碼',
        '◆ 難以複用：下一次開新對話，所有規則與上下文全部歸零',
    ]
    c.setFont(ZH, 10); c.setFillColor(GREY3)
    for i, pt in enumerate(bad_points):
        c.drawString(48, H-155 - i*42, pt[:24])
        if len(pt) > 24:
            c.drawString(64, H-172 - i*42, pt[24:])

    # 右側：Skill 解法
    c.setFillColor(GREY1); c.rect(W/2 + 16, 60, 420, H-150, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.rect(W/2 + 16, H-93, 420, 3, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(ZH_B, 14); c.drawString(W/2 + 32, H-120, 'Agent Skill 模組化解法')
    good_points = [
        '◆ 標準化封裝：將「領域知識 + 本地工具腳本」封裝成單一資料夾',
        '◆ 隨插即用 (On-Demand)：AI 需要時才動態載入 SKILL.md 定義',
        '◆ 職責分離：AI 負責發想創意，本地 Python 負責格式化與寫檔',
        '◆ 系統級可移植：跨專案、跨模型（Claude/Gemini/GPT）皆可無縫調用',
    ]
    c.setFont(ZH, 10); c.setFillColor(GREY3)
    for i, pt in enumerate(good_points):
        c.drawString(W/2 + 32, H-155 - i*42, pt[:24])
        if len(pt) > 24:
            c.drawString(W/2 + 48, H-172 - i*42, pt[24:])

    footer(c, 2)
    c.showPage()

    # ═════════════════════════════════════════════════════════════════
    # P3 減壓腳本 (Decompression Script) 核心機制
    # ═════════════════════════════════════════════════════════════════
    bg(c, dark=True)
    accent_bar_top(c)
    chrome_min(c, 'ARCHITECTURE · 02', 'DECOMPRESSION PATTERN', dark=True)
    c.setFillColor(WHITE); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '核心專利思維：減壓腳本 (Decompression Script)')

    # 流程三區塊
    b_w = 260; b_h = 240; b_y = 130
    steps = [
        ('1. 高密度創意輸入 (AI)', 'AI 僅產出最精簡的 Spec JSON：\n- 魚種名稱 / 階級顏色\n- 描述 Lore / 數值效果\n- 生態域目標\n\n★ 僅消耗 80~120 Tokens！'),
        ('2. 減壓腳本自動膨脹 (Python)', '本機 add_fish.py 接手運算：\n- 自動生成「普通版 + 魚王版」\n- 注入 1.21.1 custom_data\n- 匹配 12 類生態域戰利品表\n- 執行去重與 UTF-8 覆寫'),
        ('3. 完整遊戲資產落地 (Game)', '瞬間產生標準 400+ 行設定：\n- 玩家頭顱 Base64 貼圖綁定\n- 雙版本機率權重演算分配\n- 遊戲內熱重載直接生效\n\n★ 膨脹率達 10x ~ 15x！'),
    ]
    for i, (st, sc) in enumerate(steps):
        sx = 32 + i*(b_w + 50)
        c.setFillColor(colors.HexColor('#1a1c23'))
        c.rect(sx, b_y, b_w, b_h, fill=1, stroke=0)
        c.setFillColor(ACCENT); c.rect(sx, b_y+b_h-3, b_w, 3, fill=1, stroke=0)
        c.setFillColor(WHITE); c.setFont(ZH_B, 11)
        c.drawString(sx+12, b_y+b_h-24, st)
        c.setFont(ZH, 9.5); c.setFillColor(GREY3)
        for j, line in enumerate(sc.split('\n')):
            c.drawString(sx+12, b_y+b_h-50 - j*17, line)
        if i < 2:
            arr_x = sx + b_w + 14
            c.setFillColor(ACCENT); c.setFont(ZH_B, 22)
            c.drawString(arr_x, b_y + b_h/2 - 10, '→')

    c.setFillColor(colors.HexColor('#aaccff')); c.setFont(ZH, 10.5)
    c.drawCentredString(W/2, 80, '成果效益：大幅節省模型上下文、杜絕語法出錯，讓 AI 代理人發揮純粹的創造價值。')

    footer(c, 3, dark=True)
    c.showPage()

    # ═════════════════════════════════════════════════════════════════
    # P4 產生成品展示頁：程式碼 + 魚皮膚圖
    # ═════════════════════════════════════════════════════════════════
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'ARTIFACT SHOWCASE · 03', 'GENERATED CODE & SKINS')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '成品展示：一鍵生成的代碼與生物像素實體')

    # 左側：飲料 advancement 代碼展示
    c.setFillColor(CODE_BG); c.rect(32, 60, 430, H-150, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.rect(32, H-93, 430, 3, fill=1, stroke=0)
    c.setFillColor(WHITE); c.setFont(ZH_B, 11); c.drawString(44, H-115, '自訂飲料實體規格 (Component JSON)')
    code_lines = [
        '{',
        '  "minecraft:item_name": {"text":"龍舌蘭日出","color":"gold"},',
        '  "minecraft:lore": ["🏷️【標籤】特調雞尾酒 | 烈酒"],',
        '  "minecraft:custom_data": {"ebrew":["tequila","special"]},',
        '  "minecraft:consumable": {',
        '    "animation": "drink",',
        '    "sound": "entity.generic.drink",',
        '    "on_consume_effects": [',
        '      {"id":"minecraft:speed","duration":400,"amplifier":1},',
        '      {"id":"minecraft:strength","duration":200,"amplifier":0}',
        '    ]',
        '  }',
        '}'
    ]
    c.setFont(MONO, 8.5); c.setFillColor(colors.HexColor('#85e89d'))
    for i, cl in enumerate(code_lines):
        c.drawString(44, H-140 - i*16, cl)

    # 右側：魚皮膚與實體展示
    c.setFillColor(GREY1); c.rect(W/2 + 16, 60, 430, H-150, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.rect(W/2 + 16, H-93, 430, 3, fill=1, stroke=0)
    c.setFillColor(INK); c.setFont(ZH_B, 11); c.drawString(W/2 + 28, H-115, '程序化像素皮膚 (Wikipedia API 驅動生成)')

    # 放兩張代表魚
    draw_skin_img(c, CLOWN_B64, W/2 + 45, H-225, size=85, label='公子小丑魚 (Ocellaris)')
    draw_skin_img(c, PERCH_B64, W/2 + 185, H-225, size=85, label='黃鱸 (Yellow Perch)')

    desc_text = [
        '◆ 條紋演算：自動生成 3 道黑邊白環帶 / 縱向漸層',
        '◆ 立體浮雕：利用 Minecraft 頭顱外層帽子圖層 (Hat UV)',
        '  將魚鰭、立體珠眼與突出魚口以 0.5px 浮雕感呈現',
        '◆ 資料包整合：Base64 貼圖直寫玩家頭顱 profile',
    ]
    c.setFont(ZH, 9.5); c.setFillColor(GREY3)
    for i, dt in enumerate(desc_text):
        c.drawString(W/2 + 28, H-270 - i*20, dt)

    footer(c, 4)
    c.showPage()

    # ═════════════════════════════════════════════════════════════════
    # P5 本專案自研四大 Skill 模組解構
    # ═════════════════════════════════════════════════════════════════
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'MODULES · 04', 'THE 4 CUSTOM SKILLS')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '本專案自研四大 Agent Skill 模組')

    skills_data = [
        ('ebrewing-drink-builder', '飲料自動生成技能',
         '功能：處理糖類、黃金、鑽石三品質飲料\n'
         '特性：自動補齊 MC 16 色標籤與百科 entry\n'
         '產出：Advancement 達成判定與自訂 Lore'),
        ('ebrewing-fish-builder', '生態域釣魚生成技能',
         '功能：自動成對生成普通魚與傳奇魚王\n'
         '特性：按照 8 階顏色配置權重、飽和度自動翻倍\n'
         '產出：直寫 12 生態域與特殊魚餌戰利品表'),
        ('ebrewing-special-builder', '特殊釀造擴充技能',
         '功能：客製化複雜合成調酒配方\n'
         '特性：自動注入 special_brew.mcfunction 辨識\n'
         '產出：綁定 consumption 偵測與自訂效果函數'),
        ('minecraft-skin-generator', '水生生物繪圖技能',
         '功能：百科文本轉 64×64 像素頭顱貼圖\n'
         '特性：硬骨/軟骨/甲殼/貝類等 5 大形態學模板\n'
         '產出：標準 Base64 貼圖，無侵權風險'),
    ]
    sw = 425; sh = 135
    for i, (sname, stitle, sdesc) in enumerate(skills_data):
        col = i % 2; row = i // 2
        sx = 32 + col*(sw + 26)
        sy = H - 120 - row*(sh + 20) - sh
        c.setFillColor(GREY1); c.rect(sx, sy, sw, sh, fill=1, stroke=0)
        c.setFillColor(ACCENT); c.rect(sx, sy+sh-3, sw, 3, fill=1, stroke=0)
        c.setFillColor(INK); c.setFont(ZH_B, 11)
        c.drawString(sx+12, sy+sh-22, f'{stitle}')
        c.setFillColor(ACCENT); c.setFont(MONO, 8)
        c.drawString(sx+12, sy+sh-36, sname)
        c.setFont(ZH, 8.5); c.setFillColor(GREY3)
        for j, line in enumerate(sdesc.split('\n')):
            c.drawString(sx+12, sy+sh-58 - j*16, line)

    footer(c, 5)
    c.showPage()

    # ═════════════════════════════════════════════════════════════════
    # P6 如何安裝與使用這個 Skill？
    # ═════════════════════════════════════════════════════════════════
    bg(c)
    accent_bar_top(c)
    chrome_min(c, 'INSTALLATION · 05', 'HOW TO INSTALL & USE')
    c.setFillColor(INK); c.setFont(ZH_B, 22)
    c.drawString(32, H-68, '如何安裝與使用這些 Agent Skills？')

    c.setFillColor(CODE_BG); c.rect(32, 60, W-64, H-150, fill=1, stroke=0)
    c.setFillColor(ACCENT); c.rect(32, H-93, W-64, 3, fill=1, stroke=0)

    install_guide = [
        ('# 步驟 1：取得專案庫 (Clone Repository)', colors.HexColor('#79c0ff')),
        ('git clone https://github.com/Eric200710/mcepakc.git', colors.HexColor('#85e89d')),
        ('', colors.white),
        ('# 步驟 2：將 Skills 安裝到 Antigravity 全域技能目錄 (Windows)', colors.HexColor('#79c0ff')),
        ('Copy-Item -Recurse -Force "mcepakc\\minecraft-agent-skills\\*" "$env:USERPROFILE\\.gemini\\antigravity\\skills\\"', colors.HexColor('#85e89d')),
        ('', colors.white),
        ('# 步驟 3：在 AI 對話中直接下達自然語言指令使用', colors.HexColor('#79c0ff')),
        ('> "幫我在 warm_ocean 新增一條神話級金小丑魚，帶有海豚的恩惠效果"', colors.HexColor('#e1e4e8')),
        ('', colors.white),
        ('# 步驟 4：AI 會自動調用對應 Skill 並執行減壓腳本', colors.HexColor('#79c0ff')),
        ('[ebrewing-fish-builder] 已自動生成 ★ 金小丑魚 ★ 與 👑 傳說之王：金小丑魚皇 👑', colors.HexColor('#b392f0')),
        ('[ebrewing-fish-builder] 已將 2 筆條目注入 warm_ocean.json 與 special_bait.json！', colors.HexColor('#b392f0')),
    ]
    c.setFont(MONO, 10)
    for i, (text, col) in enumerate(install_guide):
        c.setFillColor(col)
        c.drawString(48, H-125 - i*20, text)

    footer(c, 6)
    c.showPage()

    # ═════════════════════════════════════════════════════════════════
    # P7 總結與問答
    # ═════════════════════════════════════════════════════════════════
    bg(c, dark=True)
    accent_bar_top(c)
    chrome_min(c, 'SUMMARY · 06', 'CONCLUSION & QA', dark=True)

    c.setFillColor(WHITE); c.setFont(ZH_B, 42)
    c.drawString(32, H*0.62, '結論與願景')
    c.drawString(32, H*0.62-52, 'Conclusion')
    c.setFillColor(ACCENT); c.setFont(ZH, 13)
    c.drawString(32, H*0.62-84, '打造真正實用、高效、可擴充的 AI Agent 工作流')

    hairline(c, W/2, 60, W/2, H-40, dark=True)

    rx = W/2 + 28
    summary_items = [
        ('核心貢獻', '提出「減壓腳本」概念，成功將 AI 生成 Token 降至 1/10'),
        ('多源整合', '打通 Wikipedia API、程序化像素繪圖與 Minecraft 原生資料包'),
        ('開源開放', '4 大模組化技能均開源於 GitHub，支援一鍵複製安裝'),
        ('未來擴充', '可無縫遷移至其他遊戲模組、自動化設定檔或企業級微服務系統'),
    ]
    for i, (k, v) in enumerate(summary_items):
        yy = H*0.72 - i*72
        c.setFillColor(GREY3); c.setFont(MONO, 8)
        c.drawString(rx, yy+14, k)
        c.setFillColor(WHITE); c.setFont(ZH, 12)
        c.drawString(rx, yy, v)
        hairline(c, rx, yy-8, W-32, yy-8, dark=True)

    footer(c, 7, dark=True)
    c.showPage()

    c.save()
    print(f'[成功] AI Agent Skill 專題深入報告 PDF 已生成：{out_path}')

# ── 執行 ────────────────────────────────────────────────────────
out_pdf = r'D:\ag\mcepack\ppt\ai_agent_skill_report.pdf'
build_agent_skill_pdf(out_pdf)
