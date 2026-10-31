# ========================================================================
# 觸發事件：飲用 地底熔金財寶釀 (on_drink_underground_coin)
# 特效效果：金幣碰撞音效、黃金財寶粒子，並重置觸發成就
# ========================================================================

# 1. 播放極具財富感的金幣碰撞與清脆叮噹聲
playsound minecraft:entity.experience_orb.pickup player @a ~ ~ ~ 1 0.5
playsound minecraft:block.amethyst_block.break player @a ~ ~ ~ 1 1.8
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 0.5 2.0

# 2. 噴射代表純金與發財的粒子特效
# 耀眼的黃金火花
particle minecraft:totem_of_undying ~ ~1 ~ 0.4 0.6 0.4 0.1 25
# 交易成功的財富綠色粒子
particle minecraft:happy_villager ~ ~1 ~ 0.5 0.5 0.5 0 15
# 深沉的熔金蒸汽 (環境粒子)
particle minecraft:dust{color:[0.85,0.65,0.12],scale:1.0} ~ ~1 ~ 0.4 0.5 0.4 0.02 20

# 3. 【重要】移除觸發成就，以便下次飲用時能再次觸發
advancement revoke @s only ebrewing:consume/consume_underground_coin

execute in minecraft:the_nether at @s run fill ~-7 ~ ~-7 ~7 ~14 ~7 minecraft:air replace minecraft:netherrack
execute in minecraft:the_nether at @s run fill ~-7 ~ ~-7 ~7 ~14 ~7 minecraft:glass replace minecraft:lava

