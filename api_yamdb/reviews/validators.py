from django.core.exceptions import ValidationError
from django.utils import timezone


def title_year_validator(value):
    if value < 1900 or value > timezone.now().year:
        raise ValidationError(
            ('%(value)s - слишком давно это было, давай что то посвежее'),
            params={'value': value},
        )
