from src.skill_router import ExaSkillRouter

router = ExaSkillRouter()

# 查询CRCL股票信息和讨论
twitter_results = router.search_and_format(
    "CRCL",
    num_results=10
)
print(twitter_results)

# 搜索更多推特特定内容
twitter_results = router.search_and_format(
    "twitter Apple stock discussion sentiment",
    num_results=15
)
print(twitter_results)
