# 1. 立即重設成就，確保下次喝還能重複觸發
advancement revoke @s only ebrewing:consume/consume_summer

# 2. 清涼的「夏日泳池」藍色水花粒子效果
particle minecraft:splash ~ ~1 ~ 0.5 0.5 0.5 0.1 50
particle minecraft:bubble ~ ~1 ~ 0.4 0.6 0.4 0.05 30

# 播放清脆的戲水音效
playsound minecraft:entity.player.splash player @a ~ ~1 ~ 1 1.2

# 3. 動作欄位提示文字
title @s actionbar {"text":"🐬 泳池派對，衝啊！","color":"aqua","bold":true}


# ==================== 風彈 + 順爆苦力怕 聯動推進區 ====================

# 【第一波：風彈】在身後 0.8 格召喚 3 個立即爆炸的風彈
execute at @s anchored eyes run summon minecraft:wind_charge ^ ^ ^-0.8 {ExplosionPower:1,Motion:[0.0,-10.0,0.0]}
execute at @s anchored eyes run summon minecraft:wind_charge ^ ^ ^-0.8 {ExplosionPower:1,Motion:[0.0,-10.0,0.0]}
execute at @s anchored eyes run summon minecraft:wind_charge ^ ^ ^-0.8 {ExplosionPower:1,Motion:[0.0,-10.0,0.0]}

# 【第二波：微型苦力怕】在風彈後方一點點（^-0.85）召喚一隻威力最小、不破壞方塊且瞬間爆炸的苦力怕
# ExplosionRadius:1b -> 爆炸範圍調到最小 (預設是 3)

