from django.core import validators


class PhonenumberValidator(validators.RegexValidator):
    regex = '^1(3|4|5|7|8)\d{9}$'
    message = "您输入的电话号码不合法"
