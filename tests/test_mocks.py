from .mock_client import MockDataFrameClient
from .mock_client_v2 import MockDataFrameClientV2


def test_v1():
    v1 = MockDataFrameClient()
    v1.activity_df()
    v1.bedtime_df()
    v1.readiness_df()
    v1.user_info_df()


def test_v2():
    v2 = MockDataFrameClientV2()
    v2.activity_df()
    v2.heart_rate_df()
    v2.personal_info_df()
    v2.sessions_df()
    v2.tags_df()
    v2.workouts_df()
