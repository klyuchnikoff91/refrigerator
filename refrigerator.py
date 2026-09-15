from decimal import Decimal, InvalidOperation
import datetime

DATE_FORMAT = '%Y-%m-%d'


def add(items, title, amount, expiration_date=None):
    """Добавляет запись покупки в хранилище в формате наименование,
    количество, срок годности."""
    if title in items:
        if expiration_date is not None:
            date_expiration = datetime.datetime.strptime(expiration_date, DATE_FORMAT).date()
        else:
            date_expiration = None
        items[title].append({'amount': Decimal(amount),
                             'expiration_date': date_expiration})
    else:
        items[title] = []
        if expiration_date is not None:
            date_expiration = datetime.datetime.strptime(expiration_date, DATE_FORMAT).date()
        else:
            date_expiration = None
        items[title].append({'amount': Decimal(amount),
                             'expiration_date': date_expiration})


def add_by_note(items, note):
    """Добавляет функционал к add, получает параметры из текстовых данных,
    разбирает строку на наименование - вся подстрока до числа, число - в количество,
    и подстрока после числа должна являться сроком годности, либо ее не должно быть."""
    args_by_note = note.split()
    title = []
    amount = ''
    expiration_date = None
    for index in range(0, len(args_by_note)):
        try:
            amount = Decimal(args_by_note[index])
            if index != len(args_by_note) - 1:
                expiration_date = args_by_note[index+1]
            break
        except InvalidOperation:
            title.append(args_by_note[index])
    title = ' '.join(title)
    add(items, title, amount, expiration_date)


def find(items, needle):
    """Ищет наименование в всех записях и возвращает список совпадений."""
    # Декоративная lambda-функция для human-readable
    needle_found_in = lambda item: item.lower().find(needle) >= 0
    result = [item for item in items if needle_found_in(item)]
    return result


def get_amount(items, needle):
    """Находит общее количество по наименованию."""
    product_amount = Decimal('0')
    for title in find(items, needle):
        for item in items[title]:
            product_amount += item['amount']
    return product_amount


def get_expired(items, in_advance_days=0):
    """Находит просроченные наименования и их количество."""
    result = []
    today = datetime.date.today()
    for title, parts in items.items():
        amount = Decimal('0')
        for part in parts:
            part_is_expired = (part['expiration_date'] is not None and
                               part['expiration_date'] <= (today + datetime.timedelta(days=in_advance_days)))
            if part_is_expired:
                amount += part['amount']
        if amount > 0:
            result.append((title, amount))
    return result


goods = {
    'Пельмени Универсальные': [
        # Первая партия продукта 'Пельмени Универсальные':
        {'amount': Decimal('0.5'), 'expiration_date': datetime.date(2023, 7, 15)},
        # Вторая партия продукта 'Пельмени Универсальные':
        {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 1)},
    ],
    'Вода': [
        {'amount': Decimal('1.5'), 'expiration_date': None}
    ],
}
