import datetime

from django.core.exceptions import ValidationError


def year_validator(value):
    if value > datetime.datetime.now().year:
        raise ValidationError(
            ('%(value)s вы указали год, который еще не наступил!'),
            params={'value': value},
        )
