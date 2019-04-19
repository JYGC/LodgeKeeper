class UserValues():
    def __init__(self, email=None, password=None, address=None, phone=None):
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone
        self.password2 = None

test_user_values = {
    'user_1': UserValues(
        email='freedom@bix.com',
        password='Test3r$',
        address='130 Fake Street, Homeburg, VIC 6969',
        phone='0456758474'
    ),
    'user_2': UserValues(
        email='gavin.manspreader@hotmail.com',
        password= 'F@kt5',
        address='99 Golburn Street, Holmeshill, VIC 3333',
        phone='0456758474'
    )
}
