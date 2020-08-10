from django.core.exceptions import ValidationError


def email_name(value):
    if value.find('@') == -1:
        print('<ы не ввели @')
        raise ValidationError(
            'Вы не ввели @'
        )


def domen_name(value):
    domen_name = value[value.find('@') + 1:]

    if len(domen_name) < 7:
        print('<доменное')
        raise ValidationError(
            'Введено не правильное доменное имя'
        )
