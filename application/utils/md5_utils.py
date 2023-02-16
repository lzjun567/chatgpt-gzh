import hashlib


def md5_hash(content):
    md5 = hashlib.md5()
    md5.update(content.encode("utf-8"))
    password = md5.hexdigest()
    return str(password)


def generate_password_hash(plaintext, salt=None):
    md5 = hashlib.md5()
    md5.update(plaintext.encode("utf-8"))
    password = md5.hexdigest()
    if salt:
        plaintext = password + salt
        md5 = hashlib.md5()
        md5.update(plaintext.encode("utf-8"))
        password = md5.hexdigest()

    return str(password)


def check_password_hash(pass_hash, password, salt=None):
    md5 = hashlib.md5()
    md5.update(password.encode("utf-8"))
    hash_str = md5.hexdigest()
    if salt:
        plaintext = hash_str + salt
        md5 = hashlib.md5()
        md5.update(plaintext.encode("utf-8"))
        hash_str = md5.hexdigest()
    return pass_hash == hash_str
