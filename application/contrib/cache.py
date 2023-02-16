from flask_redis import FlaskRedis


class Cache(FlaskRedis):
    """
    redis 常用操作 http://www.imooc.com/wiki/pythonlesson2/pyredis.html
    """
    _ROOM_USERS_KEY = "ROOM_{}_USERS_KEY"  # 房间用户列表KEY
    _ROOM_KEY = "ROOM_{}_KEY"  # 房间用户列表KEY
    _HEATBEAT_ROOM_USER_KEY = "HB_ROOM_{}_USER_{}"  # 用户心跳记录

    CHAT_USER_KEY = "USER_{}_KEY"

    def push(self, openid, data):
        self.rpush(self.CHAT_USER_KEY.format(openid), data)

    def pop(self, openid):
        return self.rpop(self.CHAT_USER_KEY.format(openid))
