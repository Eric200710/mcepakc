# 1. 立即重設成就，確保下次喝還能重複觸發
advancement revoke @s only ebrewing:consume/consume_frostburn

# 2. 炫酷的「霜燃」粒子效果 (結合靈魂火焰與冰霜雪花)
particle minecraft:soul_fire_flame ~ ~1 ~ 0.4 0.5 0.4 0.05 40
particle minecraft:snowflake ~ ~1 ~ 0.4 0.5 0.4 0.02 30

# 播放音效
playsound minecraft:block.glass.break player @a ~ ~1 ~ 1 1.5
playsound minecraft:entity.blaze.shoot player @a ~ ~1 ~ 1 0.7

# 3. 動作欄位提示文字
title @s actionbar {"text":"❄️ 霜燃之血在體內沸騰，開始侵蝕周圍環境！ 🔥","color":"gold","bold":true}


# ==================== 環境判定區 ====================

# 【功能 A】如果在水中，將周圍 (3x4x3 範圍) 的水替換成玄武岩
fill ~-1 ~-1 ~-1 ~1 ~2 ~1 minecraft:basalt replace minecraft:water

# 【功能 B】如果在黑曜石中，將身體上下兩格的黑曜石清除變為空氣 (避免卡窒息)
fill ~ ~ ~ ~ ~1 ~ minecraft:air replace minecraft:obsidian

# 【功能 C】如果玩家身處地獄 (Nether)，直接在腳下強行放置一格水
execute if dimension minecraft:the_nether run setblock ~ ~ ~ minecraft:water
