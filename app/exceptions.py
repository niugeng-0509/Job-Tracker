"""项目中使用的自定义异常。"""


class JobTrackerError(Exception):
    """Job Tracker 所有业务异常的基类。"""


class ValidationError(JobTrackerError):
    """输入或业务数据不符合要求。"""


class JobNotFoundError(JobTrackerError):
    """没有找到指定岗位。"""


class StorageError(JobTrackerError):
    """读取或保存数据失败。"""