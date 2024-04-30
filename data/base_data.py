from enums import OrderStatus


company = {
    'post': 'Почта / СДЭК',
    'master': 'Мастер',
    'putilin': 'Путилин',
    'master_spb': 'Мастер СПБ'
}

order_status_data = {
    OrderStatus.SUC.value: 'Доставлен',
    OrderStatus.ACTIVE.value: 'На руках',
    OrderStatus.ACTIVE_TAKE.value: 'На руках',
    OrderStatus.REF.value: 'Отказ',
    OrderStatus.TAKE.value: 'Принят',
    OrderStatus.SUC_TAKE.value: 'Забран',
    OrderStatus.REF_TAKE.value: 'Отказан',
    'Доставлен': OrderStatus.SUC.value,
    'На руках': OrderStatus.ACTIVE.value,
    'На руках (забрать)': OrderStatus.ACTIVE_TAKE.value,
    'Отказ': OrderStatus.REF.value,
    'Принят': OrderStatus.TAKE.value,
    'Забран': OrderStatus.SUC_TAKE.value,
    'Отказан': OrderStatus.REF_TAKE.value
}


expensis_dlv = {
    'b': 'Разное',
    'c': 'Связь / SIM',
    'd': 'Достависта',
    'e': 'Такси / Самокат / Транспорт',
    'f': 'Проездной',
    'g': 'МЦ',
    'h': 'Комус',
    'i': 'Почта / СДЭК',
    'k': 'ЗП'
}
