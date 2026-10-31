# ========================================================================
# 函數名稱：copy_and_clear_head
# 功能：當射線精準撞擊頭顱時，複製其 NBT 並將其化為空氣
# ========================================================================

# 1. 在精準鎖定的頭顱位置生成一個空的物品實體
summon minecraft:item ~ ~ ~ {tags:["head_drop_temp"],PickupDelay:10,Item:{id:"minecraft:player_head",count:1}}


# 2. 將方塊的所有組件與 NBT 完整轉移到物品實體中
data modify entity @e[type=minecraft:item,tag=head_drop_temp,limit=1] Item.components merge from block ~ ~ ~
data modify entity @e[type=minecraft:item,tag=head_drop_temp,limit=1] Item.components."minecraft:custom_data" merge from block ~ ~ ~ custom_data

# 3. 移除暫存標籤
tag @e[type=minecraft:item,tag=head_drop_temp] remove head_drop_temp

# 4. 播放碎裂效果
playsound minecraft:block.wood.break block @a ~ ~ ~ 1 1
particle minecraft:block minecraft:player_head ~ ~ ~ 0.2 0.2 0.2 0.1 10

# 5. 將該位置的頭顱化為空氣
setblock ~ ~ ~ minecraft:air

# 6. 將計分板設為最大值，強制中斷還在排隊的射線後續步進
scoreboard players set @s ebrew_ray 99

# 7. 重置你的偵測用成就
advancement revoke @s only ebrewing:detect_break_head
