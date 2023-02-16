import datetime

from flask.json import JSONEncoder
import enum
import decimal
from application.models.base import BaseModel


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, BaseModel):
                return obj.to_dict()
            elif isinstance(obj, enum.Enum):
                return obj.value
            elif type(obj) is datetime.date:
                return datetime.datetime(obj.year, obj.month, obj.day).isoformat()
            elif type(obj) is datetime.datetime:
                return obj.isoformat()
            elif type(obj) is datetime.time:
                return str(obj)
            elif isinstance(obj, decimal.Decimal):
                return float(obj)
            # 时间区间
            elif isinstance(obj, datetime.timedelta):
                return int(obj.total_seconds() * 1000)
            else:
                return str(obj)
            # iterable = iter(obj)
        except TypeError:
            pass
        # else:
        #    return list(iterable)
        return JSONEncoder.default(self, obj)
