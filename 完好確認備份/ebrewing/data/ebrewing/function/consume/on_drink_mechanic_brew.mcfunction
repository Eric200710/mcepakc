# ========================================================================
# 觸發事件：飲用 機械匠的私釀 (on_drink_mechanic_brew)
# 特效效果：重工業金屬火花、蒸汽與鐵巨人現身，並重置觸發成就
# ========================================================================

# 1. 播放震撼的鐵砧與金屬撞擊音效（模擬齒輪和機甲啟動）
playsound minecraft:block.anvil.use player @a ~ ~ ~ 1 0.8
playsound minecraft:block.iron_door.open player @a ~ ~ ~ 1 0.5
playsound minecraft:entity.iron_golem.damage player @a ~ ~ ~ 1 1.2

# 2. 噴射大量的蒸汽與鍛造火花粒子效果
# 蒸汽效果 (雲霧粒子)
particle minecraft:cloud ~ ~1 ~ 0.5 0.5 0.5 0.05 30
# 鍛造火花 (熔岩或附魔粒子)
particle minecraft:lava ~ ~1 ~ 0.3 0.5 0.3 0.1 15
particle minecraft:crit ~ ~1 ~ 0.5 0.5 0.5 0.2 25

# 3. 在玩家的原地生成一隻「鐵巨人」
# 加上 PlayerCreated:1b 標籤，這隻鐵巨人就不會攻擊玩家與村民，會忠心守護創作者
summon minecraft:iron_golem ~ ~ ~ {PlayerCreated:1b,CustomName:{"text":"工坊守衛","color":"zinc","bold":true}}

# 4. 加碼一小段視覺特效：給玩家一個短暫的盲目來模擬大腦被重工業蒸汽衝擊的「微醺感」
effect give @s minecraft:blindness 1 0 true

# ========================================================================
# 5. 【重要】移除觸發成就，以便下次飲用時能再次觸發
# ========================================================================
advancement revoke @s only ebrewing:consume/consume_mechanic_brew

