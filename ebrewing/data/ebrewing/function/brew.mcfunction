# =================================================================
# 【中央調度器】依據第一格（Slot 0）的物品進行高效率分流
# =================================================================

# 【大分類 A】如果第一格是「糖」➔ 執行糖系飲品（如：烈焰粉釀、金蘋果釀等）
execute if items block ~ ~ ~ container.0 minecraft:sugar run function ebrewing:brew_sugar

# 【大分類 B】如果第一格是「發酵蜘蛛眼」➔ 執行酒系飲品（如：經典啤酒、頂級紅酒等）
execute if items block ~ ~ ~ container.0 minecraft:fermented_spider_eye run function ebrewing:brew_alcohol

# 【大分類 C】如果第一格是「鑽石」➔ 執行奢華/神話系飲品
execute if items block ~ ~ ~ container.0 minecraft:diamond run function ebrewing:brew_diamond

# 【大分類 D】如果第一格是「黃金」➔ 執行奢華/經典名酒
execute if items block ~ ~ ~ container.0 minecraft:gold_ingot run function ebrewing:brew_gold

# 【大分類 S】如果第一格是「飲料」➔ 執行特調
execute if items block ~ ~ ~ container.0 minecraft:player_head run function ebrewing:plus


# =================================================================
# 【通用強制消耗】只要第一格的「分類材料」符合，且成品槽成功觸發，一律清空
# =================================================================
execute if items block ~ ~ ~ container.0 minecraft:sugar run function ebrewing:consume_slots
execute if items block ~ ~ ~ container.0 minecraft:fermented_spider_eye run function ebrewing:consume_slots
execute if items block ~ ~ ~ container.0 minecraft:gold_ingot run function ebrewing:consume_slots
execute if items block ~ ~ ~ container.0 minecraft:diamond run function ebrewing:consume_slots
