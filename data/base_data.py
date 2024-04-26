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
    # OrderStatus.ACTIVE_TAKE.value: 'На руках',
    OrderStatus.REF.value: 'Отказ',
    OrderStatus.TAKE.value: 'Принят',
    OrderStatus.SUC_TAKE.value: 'Забран',
    OrderStatus.REF_TAKE.value: 'Отказан'
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
