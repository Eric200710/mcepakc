# ========================================================================
# 觸發事件：飲用 香醇淬煉牛乳 (on_drink_pure_milk)
# 特效效果：聖光粒子、清除負面狀態、神聖音效，並重置觸發成就
# ========================================================================

# 1. 播放神聖且治癒的清脆音效
playsound minecraft:entity.player.levelup player @a ~ ~ ~ 1 1.5
playsound minecraft:block.amethyst_block.chime player @a ~ ~ ~ 1 1.2

# 2. 噴射大量代表純淨牛乳與聖光的純白、發光粒子
# 純白煙霧 (牛乳蒸汽)
particle minecraft:poof ~ ~1 ~ 0.5 0.5 0.5 0.02 20
# 耀眼閃光 (聖光音符或火花)

particle minecraft:instant_effect ~ ~1 ~ 0.5 0.5 0.5 0 30

# 3. 特殊技能：淨化身體（清除常見的惡性負面狀態，但保留你的良性 Buff）
effect clear @s minecraft:poison
effect clear @s minecraft:wither
effect clear @s minecraft:slowness
effect clear @s minecraft:weakness
effect clear @s minecraft:nausea
effect clear @s minecraft:bad_omen

# 4. 【重要】移除觸發成就，以便下次飲用時能再次觸發
advancement revoke @s only ebrewing:consume/consume_pure_milk
