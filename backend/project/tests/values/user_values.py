import random, string


USER_1 = dict(
    email='freedom@bix.com',
    password='Test3r$',
    address='130 Fake Street, Homeburg, VIC 6969',
    phone='0456758474'
)

USER_1_NEW_PASSWD = dict(
    USER_1,
    password='f15her$'
)

USER_2 = dict(
    email='gavin.manspreader@hotmail.com',
    password= 'F@kt5',
    address='99 Golburn Street, Holmeshill, VIC 3333',
    phone='0456758474'
)

INVALID_TOKEN = ''.join(random.choices(string.ascii_letters + string.digits,
                                       k=16))
