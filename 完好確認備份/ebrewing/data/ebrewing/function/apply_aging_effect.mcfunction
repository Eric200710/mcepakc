# =================================================================
# 【通用陳釀機制】自動抓取 Slot 26 藥水時間並 +30 秒 (600 ticks)
# =================================================================

# 1. 建立一個臨時記分板（如果之前建過，這行會自動跳過，很安全）
scoreboard objectives add ebrew_temp dummy

# 2. 將 Slot 26 藥水的第一個效果的 duration 數值，存入當前 Text Display 實體的記分板中
execute store result score @s ebrew_temp run data get block ~ ~ ~ container.26.components."minecraft:consumable".on_consume_effects[0].effects[0].duration

# 3. 建立一個常數用來做加法（讓一個虛擬玩家 config 的分數等於 600 tick，也就是 30 秒）
scoreboard players set #add_time ebrew_temp 600

# 4. 在記分板內進行加法運算：自己的分數 = 自己的分數 + 600
scoreboard players operation @s ebrew_temp += #add_time ebrew_temp

# 5. 把記分板算好的新時間，直接寫回木桶 Slot 26 的藥水組件中！
execute store result block ~ ~ ~ container.26.components."minecraft:consumable".on_consume_effects[0].effects[0].duration int 1 run scoreboard players get @s ebrew_temp


# =================================================================
# 【名字與外觀點綴】(自由選用) 幫藥水名字加上「【陳釀】」前綴
# =================================================================
# 如果你想讓它更有儀式感，這行指令會直接在它原本的名字前面強制貼上【陳釀】兩個字
data modify block ~ ~ ~ container.26.components."minecraft:custom_name" set value '{"text":"【陳釀】"}'



# =================================================================
# 【善後工作】
# =================================================================
# 功成身退，殺掉自己（文字顯示實體）
kill @s
