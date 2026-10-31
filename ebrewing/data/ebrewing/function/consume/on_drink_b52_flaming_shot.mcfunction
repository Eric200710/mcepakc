advancement revoke @s only ebrewing:consume/consume_b52_flaming_shot
particle minecraft:explosion_emitter ~ ~1 ~ 1 1 1 0.0 1
particle minecraft:campfire_cosy_smoke ~ ~1 ~ 0.3 0.5 0.3 0.05 30
playsound minecraft:entity.generic.explode player @a ~ ~1 ~ 1.2 1.4
playsound minecraft:entity.firework_rocket.blast player @a ~ ~1 ~ 1.5 0.8
title @s actionbar {"text":"💥 B-52 爆裂轟炸！全速衝擊！","color":"light_purple","bold":true}
execute at @s anchored eyes run summon minecraft:wind_charge ^ ^ ^-1 {ExplosionPower:1,Motion:[0.0,-5.0,0.0]}
