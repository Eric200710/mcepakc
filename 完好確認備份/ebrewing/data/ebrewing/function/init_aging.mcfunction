# 1. 移除「未完成」標籤，避免它等一下又被重複初始化
tag @s remove aging_uncompleted

# 2. 加上「正式陳釀中」的標籤，作為 600 秒後伺服器尋找它的依據
tag @s add aging_in_progress

# 3. 觸發 6 秒（120 tick）後的排程
schedule function ebrewing:finish_aging_delay 120t append
