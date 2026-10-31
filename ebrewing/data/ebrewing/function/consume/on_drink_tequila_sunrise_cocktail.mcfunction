advancement revoke @s only ebrewing:consume/consume_tequila_sunrise_cocktail
particle minecraft:flame ~ ~1.2 ~ 0.4 0.6 0.4 0.05 40
particle minecraft:wax_off ~ ~1.2 ~ 0.5 0.5 0.5 0.1 25
playsound minecraft:entity.blaze.shoot player @a ~ ~1 ~ 1 1.2
playsound minecraft:block.amethyst_block.chime player @a ~ ~1 ~ 1.5 1.5
title @s actionbar {"text":"🌅 破曉朝陽昇起！周遭生物已沐浴在晨曦中！","color":"gold","bold":true}
execute at @s run effect give @e[distance=..15] minecraft:glowing 15 0
