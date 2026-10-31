# =================================================================
# 熔岩/煉金系統：效果相加並同步狀態（保持數量不變）
# =================================================================

# -----------------------------------------------------------------
# 中途觸發：第六格特調檢測
# -----------------------------------------------------------------
execute if items block ~ ~ ~ container.5 * run function ebrewing:special_brew


# -----------------------------------------------------------------
# 階段二：將後四格（Slot 1b ~ 4b）的藥水效果追加（append）到第一格上
# -----------------------------------------------------------------
execute if data block ~ ~ ~ Items[{Slot:1b}].components."minecraft:consumable".on_consume_effects run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:consumable".on_consume_effects append from block ~ ~ ~ Items[{Slot:1b}].components."minecraft:consumable".on_consume_effects[]

execute if data block ~ ~ ~ Items[{Slot:2b}].components."minecraft:consumable".on_consume_effects run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:consumable".on_consume_effects append from block ~ ~ ~ Items[{Slot:2b}].components."minecraft:consumable".on_consume_effects[]

execute if data block ~ ~ ~ Items[{Slot:3b}].components."minecraft:consumable".on_consume_effects run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:consumable".on_consume_effects append from block ~ ~ ~ Items[{Slot:3b}].components."minecraft:consumable".on_consume_effects[]

execute if data block ~ ~ ~ Items[{Slot:4b}].components."minecraft:consumable".on_consume_effects run data modify block ~ ~ ~ Items[{Slot:0b}].components."minecraft:consumable".on_consume_effects append from block ~ ~ ~ Items[{Slot:4b}].components."minecraft:consumable".on_consume_effects[]


# -----------------------------------------------------------------
# 階段三：將第一格（Slot 0b）的所有組件狀態，完整覆蓋到後四格（不影響 Count 數量）
# -----------------------------------------------------------------
# 利用 1.21+ 的 components 頂層覆蓋，只同步屬性，完美保留各格子原本的 Count 數量
execute if data block ~ ~ ~ Items[{Slot:1b}] run data modify block ~ ~ ~ Items[{Slot:1b}].components set from block ~ ~ ~ Items[{Slot:0b}].components
execute if data block ~ ~ ~ Items[{Slot:2b}] run data modify block ~ ~ ~ Items[{Slot:2b}].components set from block ~ ~ ~ Items[{Slot:0b}].components
execute if data block ~ ~ ~ Items[{Slot:3b}] run data modify block ~ ~ ~ Items[{Slot:3b}].components set from block ~ ~ ~ Items[{Slot:0b}].components
execute if data block ~ ~ ~ Items[{Slot:4b}] run data modify block ~ ~ ~ Items[{Slot:4b}].components set from block ~ ~ ~ Items[{Slot:0b}].components

