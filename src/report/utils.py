# coding=utf-8


def get_verbose_date(dt):
    months = ['января', 'февраля', 'марта', 'апреля',
              'мая', 'июня', 'июля', 'августа',
              'сентября', 'октября', 'ноября', 'декабря']

    return '{} {} {} года'.format(dt.day, months[dt.month - 1], dt.year)
