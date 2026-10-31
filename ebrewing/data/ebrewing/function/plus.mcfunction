# =================================================================
# 熔岩/煉金系統：效果相加並同步狀態（保持數量不變）
# =================================================================

# -----------------------------------------------------------------
# 中途觸發：第六格特調檢測
# -----------------------------------------------------------------
execute if items block ~ ~ ~ container.5 * run function ebrewing:special_brew


# -----------------------------------------------------------------
# 階段二：將後四格（Slot 1b ~ 4b）的藥水效果與自訂標籤追加（append）到第一格上
# -----------------------------------------------------------------
# 1. 效果追加
execute if data block ~ ~ ~ Items[{Slot:1b}].components."minecraft:consumable".on_consume_effects run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:consumable".on_consume_effects append from block ~ ~ ~ Items[{Slot:1b}].components."minecraft:consumable".on_consume_effects[]

execute if data block ~ ~ ~ Items[{Slot:2b}].components."minecraft:consumable".on_consume_effects run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:consumable".on_consume_effects append from block ~ ~ ~ Items[{Slot:2b}].components."minecraft:consumable".on_consume_effects[]

execute if data block ~ ~ ~ Items[{Slot:3b}].components."minecraft:consumable".on_consume_effects run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:consumable".on_consume_effects append from block ~ ~ ~ Items[{Slot:3b}].components."minecraft:consumable".on_consume_effects[]

execute if data block ~ ~ ~ Items[{Slot:4b}].components."minecraft:consumable".on_consume_effects run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:consumable".on_consume_effects append from block ~ ~ ~ Items[{Slot:4b}].components."minecraft:consumable".on_consume_effects[]

# 2. 自訂標籤追加（若第一格原本無標籤且後續格有標籤時先建立，有的話進行追加合併）
execute unless data block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew if data block ~ ~ ~ Items[{Slot:1b}].components."minecraft:custom_data".ebrew run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew set from block ~ ~ ~ Items[{Slot:1b}].components."minecraft:custom_data".ebrew
execute if data block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew if data block ~ ~ ~ Items[{Slot:1b}].components."minecraft:custom_data".ebrew run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew append from block ~ ~ ~ Items[{Slot:1b}].components."minecraft:custom_data".ebrew[]

execute unless data block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew if data block ~ ~ ~ Items[{Slot:2b}].components."minecraft:custom_data".ebrew run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew set from block ~ ~ ~ Items[{Slot:2b}].components."minecraft:custom_data".ebrew
execute if data block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew if data block ~ ~ ~ Items[{Slot:2b}].components."minecraft:custom_data".ebrew run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew append from block ~ ~ ~ Items[{Slot:2b}].components."minecraft:custom_data".ebrew[]

execute unless data block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew if data block ~ ~ ~ Items[{Slot:3b}].components."minecraft:custom_data".ebrew run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew set from block ~ ~ ~ Items[{Slot:3b}].components."minecraft:custom_data".ebrew
execute if data block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew if data block ~ ~ ~ Items[{Slot:3b}].components."minecraft:custom_data".ebrew run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew append from block ~ ~ ~ Items[{Slot:3b}].components."minecraft:custom_data".ebrew[]

execute unless data block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew if data block ~ ~ ~ Items[{Slot:4b}].components."minecraft:custom_data".ebrew run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew set from block ~ ~ ~ Items[{Slot:4b}].components."minecraft:custom_data".ebrew
execute if data block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew if data block ~ ~ ~ Items[{Slot:4b}].components."minecraft:custom_data".ebrew run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:custom_data".ebrew append from block ~ ~ ~ Items[{Slot:4b}].components."minecraft:custom_data".ebrew[]


# -----------------------------------------------------------------
# 階段三：將第一格（Slot 0b）的所有組件狀態，完整覆蓋到後四格（不影響 Count 數量）
# -----------------------------------------------------------------
# 利用 1.21+ 的 components 頂層覆蓋，只同步屬性，完美保留各格子原本的 Count 數量
execute if data block ~ ~ ~ Items[{Slot:1b}] run data modify block ~ ~ ~ Items[{Slot:1b}].components set from block ~ ~ ~ Items[{Slot:0b}].components
execute if data block ~ ~ ~ Items[{Slot:2b}] run data modify block ~ ~ ~ Items[{Slot:2b}].components set from block ~ ~ ~ Items[{Slot:0b}].components
execute if data block ~ ~ ~ Items[{Slot:3b}] run data modify block ~ ~ ~ Items[{Slot:3b}].components set from block ~ ~ ~ Items[{Slot:0b}].components
execute if data block ~ ~ ~ Items[{Slot:4b}] run data modify block ~ ~ ~ Items[{Slot:4b}].components set from block ~ ~ ~ Items[{Slot:0b}].components

