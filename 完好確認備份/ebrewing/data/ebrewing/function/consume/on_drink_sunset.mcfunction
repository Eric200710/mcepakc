# 1. 立即重設成就，確保下次喝還能重複觸發
advancement revoke @s only ebrewing:consume/consume_sunset

# 2. 金黃色的落日夕陽粒子效果（金色烈焰 + 太陽閃光）
particle minecraft:flame ~ ~1 ~ 0.5 0.5 0.5 0.02 30
particle minecraft:glow ~ ~1 ~ 0.6 0.6 0.6 0.01 40

# 播放溫暖舒緩又帶著神聖感的音效
# 播放火焰彈爆發與火熄滅的焦糖煙燻音效
playsound minecraft:entity.blaze.shoot player @a ~ ~1 ~ 1 0.9
playsound minecraft:block.fire.extinguish player @a ~ ~1 ~ 1 1.2

# 3. 動作欄位文字
title @s actionbar {"text":"☀ 落日的餘暉在心中暈開，世界染上了金黃...","color":"gold","bold":true}


# ==================== 特殊功能區 ====================




# 【功能 C：暮光之盾（修正版）】
# 點燃附近 5 格內除了玩家自己、盔甲座、展示框、互動實體和 Marker 以外的所有實體，並讓它們發光。
# 使用 damage 指令給予 4 點火焰傷害，並讓目標著火 5 秒（100 ticks）

# 讓符合條件的生物獲得發光效果 5 秒
execute as @e[distance=..5,type=!minecraft:player,type=!minecraft:armor_stand,type=!minecraft:item_frame,type=!minecraft:glow_item_frame,type=!minecraft:interaction,type=!minecraft:marker] run effect give @s minecraft:glowing 5 0

# 讓符合條件的生物直接受到來自玩家的火焰傷害（會直接著火 5 秒）




# 讓指定生物（例如最近的殭屍）著火 30 秒（30秒 × 20刻 = 600t）
execute as @e[distance=..8,type=!minecraft:player,type=!minecraft:armor_stand,type=!minecraft:item_frame,type=!minecraft:glow_item_frame,type=!minecraft:interaction,type=!minecraft:marker] run data modify entity @s Fire set value 300s




execute as @e[distance=..8,type=!minecraft:player,type=!minecraft:armor_stand,type=!minecraft:item_frame,type=!minecraft:glow_item_frame,type=!minecraft:interaction,type=!minecraft:marker] run damage @s 8 minecraft:on_fire by @s



