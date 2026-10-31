# 1. 重設成就
advancement revoke @s only ebrewing:consume/consume_lumberjack

# 2. 特效：木屑爆裂與森林震動
particle minecraft:happy_villager ~ ~1 ~ 5 5 5 0.1 50
particle minecraft:explosion_emitter ~ ~1 ~ 1 1 1 0.0 1
playsound minecraft:block.wood.break player @a ~ ~1 ~ 2 0.5

# 3. 動作欄位提示
title @s actionbar {"text":"🪓 伐木狂熱：範圍內的樹木已被粉碎並收集！","color":"green","bold":true}

# ==================== 範圍破壞區 (20*20*15) ====================
# 以玩家為中心：X 與 Z 範圍 -10 ~ 10 (共 21 格，約 20*20)，Y 範圍 -5 ~ 10 (共 15 格)
# 使用 fill ... destroy 會讓所有被覆蓋的方塊以「掉落物」形式噴出來

# 破壞橡木與深色橡木等相關原木 
execute at @s run fill ~-10 ~-5 ~-10 ~10 ~10 ~10 minecraft:air destroy replace minecraft:oak_log
execute at @s run fill ~-10 ~-5 ~-10 ~10 ~10 ~10 minecraft:air destroy replace minecraft:spruce_log
execute at @s run fill ~-10 ~-5 ~-10 ~10 ~10 ~10 minecraft:birch_log
execute at @s run fill ~-10 ~-5 ~-10 ~10 ~10 ~10 minecraft:jungle_log
execute at @s run fill ~-10 ~-5 ~-10 ~10 ~10 ~10 minecraft:acacia_log
execute at @s run fill ~-10 ~-5 ~-10 ~10 ~10 ~10 minecraft:dark_oak_log
execute at @s run fill ~-10 ~-5 ~-10 ~10 ~10 ~10 minecraft:cherry_log
execute at @s run fill ~-10 ~-5 ~-10 ~10 ~10 ~10 minecraft:mangrove_log

# 若想連樹葉一起清除（可選，建議加上以免樹木浮空）
execute at @s run fill ~-10 ~-5 ~-10 ~10 ~10 ~10 minecraft:air destroy replace #minecraft:leaves
!!!!!!!¡
