advancement revoke @s only ebrewing:consume/consume_godwither


# 1. 播放震撼的地獄神話音效（終界龍咆哮，聲音大且低沉）
playsound minecraft:entity.ender_dragon.growl player @a ~ ~ ~ 1 0.5

# 2. 產生環繞玩家的凋零與靈魂粒子特效
particle minecraft:ash ~ ~1 ~ 0.5 0.5 0.5 0.1 100 normal
particle minecraft:soul_fire_flame ~ ~1 ~ 0.3 0.5 0.3 0.05 50 normal
particle minecraft:large_smoke ~ ~1 ~ 0.5 0.8 0.5 0.02 40 normal

# 3. 畫面震動提示（短暫盲目）
effect give @s minecraft:blindness 1 0 true

# 4. 核心修正：為當前玩家貼上標籤，防止 5 分鐘後 schedule 找不到人
tag @s add drank_godwither

# 5. 核心排程：5分鐘（6000刻）後執行
schedule function ebrewing:godwither2 6000t append

# 6. 畫面文字提示（新版 actionbar 語法）
title @s actionbar {"text":"☠️ 凋零與古神的低語在腦海迴盪...毀滅倒數開始","color":"dark_red","bold":true}

effect give @s minecraft:strength 300 24
