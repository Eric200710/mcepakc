# 1. 立即重設成就，確保下次喝還能重複觸發
advancement revoke @s only ebrewing:consume/consume_cranberry

# 2. 粉紅交響曲專屬特效（浪漫櫻花花瓣 + 戀愛愛心粒子）
particle minecraft:cherry_leaves ~ ~1 ~ 0.6 0.5 0.6 0.05 40
particle minecraft:heart ~ ~1.2 ~ 0.3 0.3 0.3 0.01 5

# 播放優雅、輕快又帶著閃爍感的音效
playsound minecraft:block.amethyst_block.chime player @a ~ ~1 ~ 1 1.2
playsound minecraft:entity.allay.item_thrown player @a ~ ~1 ~ 0.8 1.5

# 3. 動作欄位提示文字
title @s actionbar {"text":"🌸 粉紅交響曲響起，無數甜美莓果在四周綻放！","color":"light_purple","bold":true}


# ==================== 維度判定方塊生成區 ====================

# 【主世界 Overworld】從 Y = -63 一路向上填滿到你目前站立的高度
execute if dimension minecraft:overworld run fill ~ -63 ~ ~ ~ ~ minecraft:sweet_berry_bush[age=3] replace minecraft:air

# 【地獄 The Nether】從 Y = 0 一路向上填滿到你目前站立的高度
execute if dimension minecraft:the_nether run fill ~ 0 ~ ~ ~ ~ minecraft:sweet_berry_bush[age=3] replace minecraft:air

# 【終界 The End】從 Y = 0 一路向上填滿到你目前站立的高度
execute if dimension minecraft:the_end run fill ~ 0 ~ ~ ~ ~ minecraft:sweet_berry_bush[age=3] replace minecraft:air
