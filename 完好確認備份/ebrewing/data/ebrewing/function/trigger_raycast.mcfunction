# =================================================================
# 1. 剝奪成就（以便下次按右鍵能再次觸發）
# =================================================================
advancement revoke @s only ebrewing:use_cooler_stick

# =================================================================
# 2. 在玩家眼前 1.5 格處：顯示提示粒子，並直接嘗試觸發釀造偵測
# =================================================================
# 粒子提示：在眼前 1.5 格處產生一個小小的女巫紫色魔法粒子（或你可以換成 flame、happy_villager 等）
execute at @s anchored eyes run particle minecraft:witch ^ ^ ^1.5 0 0 0 0 1 normal

# 觸發偵測：直接以眼前 1.5 格的坐標執行原本的 brew 檢查
execute at @s anchored eyes positioned ^ ^ ^1.5 run function ebrewing:brew

# 1. 檢查 Slot 9 是不是鐵錠，如果是，就召喚一個「帶有未完成標籤」的展示文字實體
# (這裡將文字設定為懸浮在木桶的位置，並帶有 aging_uncompleted 標籤)
execute if items block ~ ~ ~ container.9 minecraft:iron_ingot[count=1] run summon minecraft:text_display ~ ~ ~ {Tags:["aging_uncompleted"],text:'{"text":"⏳ 陳釀中...","color":"red","bold":true}'}

# 2. 消耗掉 Slot 9 的鐵錠材料
execute if items block ~ ~ ~ container.9 minecraft:iron_ingot[count=1] run item replace block ~ ~ ~ container.9 with minecraft:air

# 3. 馬上對著這個剛誕生、帶有「未完成標籤」的實體執行初始化 Function
execute as @e[type=minecraft:text_display,tag=aging_uncompleted] at @s run function ebrewing:init_aging
