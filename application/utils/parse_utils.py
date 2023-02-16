from dateutil.parser import parse


def parse_datetime(string):
    return parse(string)


def parse_date(string):
    return parse(string).date()


def parse_bool(string):
    if string == '0':
        return False
    else:
        return True
