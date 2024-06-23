from datetime import datetime, timezone
from enum import Enum



def strptime_to_timestamp(string: str) -> float:
    date_part, frac_seconds_with_z = string.split(".")
    frac_seconds = frac_seconds_with_z[:-1]
    frac_seconds_truncated = frac_seconds[:6]
    adjusted_timestamp = f"{date_part}.{frac_seconds_truncated}Z"
    dt = datetime.strptime(adjusted_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()


class TimeDescriptionTranslationEN(Enum):
    DAY = "d"
    HOUR = "h"
    MINUTE = "m"
    SECOND = "s"

class TimeDescriptionTranslationZH(Enum):
    DAY = " 天 "
    HOUR = " 小时 "
    MINUTE = " 分钟 "
    SECOND = " 秒 "

# 多语言枚举字典
language_enum_dict = {
    'en': TimeDescriptionTranslationEN,
    'zh': TimeDescriptionTranslationZH,
}

# 多语言转换函数
def timestamp_to_describe_str(timestamp: int, lang: str = 'zh') -> str:
    TimeDesc = language_enum_dict[lang]
    
    parts = []
    if timestamp > 60 * 60 * 24:
        parts.append(f"{int(timestamp // (60*60*24))}{TimeDesc.DAY.value}")
        timestamp %= 60 * 60 * 24
    if timestamp > 60 * 60:
        parts.append(f"{int(timestamp // (60*60))}{TimeDesc.HOUR.value}")
        timestamp %= 60 * 60
    if timestamp > 60:
        parts.append(f"{int(timestamp // 60)}{TimeDesc.MINUTE.value}")
        timestamp %= 60
    if timestamp > 0:
        parts.append(f"{int(timestamp)}{TimeDesc.SECOND.value}")
    return "".join(parts).strip()