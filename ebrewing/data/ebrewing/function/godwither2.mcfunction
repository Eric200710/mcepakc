# 讓所有帶有標籤的玩家執行接下來的懲罰/自爆效果，並清除標籤
kill @a[tag=drank_godwither]
execute as @a[tag=drank_godwither] run tellraw @a [{"text":"☠️ ","color":"dark_red"},{"selector":"@s","color":"gold","bold":true},{"text":" 燃盡了凋零的力量，形神俱滅...","color":"red"}]

tag @a[tag=drank_godwither] remove drank_godwither

