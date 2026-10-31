# 讓全世界上所有帶有 aging_in_progress 標籤的展示文字實體，在它們各自的木桶座標上執行完成檔案
execute as @e[type=minecraft:text_display,tag=aging_in_progress] at @s run function ebrewing:apply_aging_effect
