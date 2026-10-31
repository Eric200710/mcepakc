
advancement revoke @s only ebrewing:consume/consume_exp


# 1. 播放極具層次感的魂光音效（直接以觸發玩家為中心發聲）
playsound minecraft:entity.experience_orb.pickup player @a ~ ~ ~ 1 1.2
playsound minecraft:entity.experience_orb.pickup player @a ~ ~ ~ 1 0.8
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 0.8 1.5

# 2. 爆發璀璨的經驗魂光粒子特效（直接在觸發玩家身上炸開）
particle minecraft:happy_villager ~ ~1 ~ 0.5 0.5 0.5 0.1 80 normal
particle minecraft:totem_of_undying ~ ~1 ~ 0.3 0.5 0.3 0.2 40 normal
particle minecraft:composter ~ ~1 ~ 0.4 0.6 0.4 0.05 60 normal

# 3. 在玩家原地精準生成 15 個經驗瓶實體
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~
summon minecraft:experience_bottle ~ ~0.5 ~

# 4. 提示文字（使用正確的新版 actionbar 語法）
title @s actionbar {"text":"✨ 體內的純淨魂光開始共鳴，福澤降臨...","color":"green","bold":true}

