"""岗位状态业务枚举。"""

from enum import Enum


class JobStatus(str, Enum):
    """岗位当前所处的求职阶段。"""

    PENDING = "待投递"
    APPLIED = "已投递"
    WRITTEN_TEST = "笔试"
    INTERVIEW = "面试"
    OFFER = "Offer"
    REJECTED = "已拒绝"
