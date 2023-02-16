from enum import IntEnum, Enum


class VisibleRange(Enum):
    owner = "owner"
    part = "part"
    all = "all"

    class Config:
        use_enum_values = True


class QuestionType(IntEnum):
    SINGLE = 1
    MULTIPLE = 2
    BOOLEAN = 3


class FileFormat(Enum):
    VIDEO = "video"
    LIVE = "live"

    class Config:
        use_enum_values = True


class CourseAction(Enum):
    DELETE = "delete"
    LAUNCH = "launch"
    UNLAUNCH = "unlaunch"


class MaterialType(Enum):
    """
    素材类型
    """
    IMAGE = 'image'
    VIDEO = 'video'
    AUDIO = 'audio'


class CommentType(Enum):
    IMAGE = 'image'
    VIDEO = 'video'
    TEXT = 'text'


class TransferStatus(Enum):
    """
    转码状态
    """
    FINISH = 'FINISH'
    PROCESSING = 'PROCESSING'


class CourseQueryType(Enum):
    NEWEST = "newest"
    BROWSE = "browse"


class StudyStatus(IntEnum):
    NO_START = 0  # 未开始学习
    LEARNING = 1  # 学习中
    FINISH = 2  # 已学完（考试还未通过）
    END = 3  # 已学完并且考试通过 （或者没有考试）


class PageType(Enum):
    MICRO_PAGE = 'micro_page'
    MESSAGE = 'message'
    MINE = 'mine'
    CUSTOM = 'custom'
    MAIN = 'main'
    ME = 'me'
    VIDEO = 'video'  # 视频详情
    TEXT = 'text'  # 图文详情


class NotificationCategory(IntEnum):
    SYSTEM = 2  # 系统消息
    NEWS = 1  # 资讯消息


class StatDimension(Enum):
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR = 'year'


class TagComputeState(IntEnum):
    """
    标签计算状态
    """
    FINISH = 2
    COMPUTING = 1


class TagType(IntEnum):
    """
    标签类型
    """
    MANUAL = 1  # 手动
    AUTO = 2  # 自动


class ActivityShowType(Enum):
    ONCE = 'once'  # 显示一次
    REPEAT = 'repeat'  # 重复显示


class ActivityStatus(Enum):
    NO_START = "no_start"
    ONGOING = 'ongoing'
    ENDED = 'ended'
    DISABLED = 'disabled'


class RankStatus(Enum):
    NO_START = "no_start"
    ONGOING = 'ongoing'
    ENDED = 'ended'
    DISABLED = 'disabled'


class RankShareChannel(IntEnum):
    POSTER = 1
    WECHAT = 2
    LINK = 3


class LiveStatus(Enum):
    PREPARE = 'prepare'  # 预告
    LIVE = "live"  # 直播中
    REPLAY = 'replay'  # 回放中


class PlayDirection(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = 'vertical'


class CourseMenuItemCode(Enum):
    DESCRIPTION = "introduce"
    LIST = "list"
    chat = "chat"


class CopyrightStat(IntEnum):
    NO_ORIGINAL = 100
    ORIGINAL = 11


class CourseKind(Enum):
    TEXT = "text"
    VIDEO = "video"


class ResourceKind(Enum):
    IMAGE = "image"
    COURSE = "course"
