import random
import string
import time
import uuid



def random_order_number(prefix=None):
    """生成随机订单号"""

    def f():
        r = int(time.time() * 1000)
        if prefix:
            r = str(prefix) + str(r)
        r = str(r)
        return r

    return f


def random_str(length=16, prefix=""):
    """
    生成随机字符串, 由大小写字母和数字组成
    :param length:
    :param prefix:  前缀
    """
    return prefix + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))


def random_num_str(length=4):
    """
    随机数字
    """
    return "".join([str(random.randint(0, 9)) for i in range(length)])


def random_base16_num_str(length=16):
    return ''.join(random.choice("0123456789abcdef") for _ in range(length))


def random_uuid_str():
    return uuid.uuid1().hex[:16]


def random_mac_address():
    mac = [random.randrange(256) for _ in range(6)]
    mac = ":".join('%02x' % b for b in mac)
    return mac


def random_en_name():
    return faker.Faker().name()


def objectid():
    return str(ObjectId())
