# 只要成品槽（Slot 26）不是空氣，就代表製作成功，把前三格清空
execute unless items block ~ ~ ~ container.26 minecraft:air run item replace block ~ ~ ~ container.0 with minecraft:air
execute unless items block ~ ~ ~ container.26 minecraft:air run item replace block ~ ~ ~ container.1 with minecraft:air
execute unless items block ~ ~ ~ container.26 minecraft:air run item replace block ~ ~ ~ container.2 with minecraft:air
