from enums import OrderStatus


company = {
    'post': 'Почта / СДЭК',
    'master': 'Мастер',
    'putilin': 'Путилин',
    'master_spb': 'Мастер СПБ'
}

order_status_data = {
    OrderStatus.NEW.value: '',
    OrderStatus.SUC.value: 'доставлен',
    OrderStatus.ACTIVE.value: 'на руках',
    OrderStatus.ACTIVE_TAKE.value: 'на руках',
    OrderStatus.REF.value: 'отказ',
    OrderStatus.TAKE.value: 'принят',
    OrderStatus.SUC_TAKE.value: 'забран',
    OrderStatus.REF_TAKE.value: 'отказан',
    OrderStatus.REMAKE.value: 'переделка',
    OrderStatus.SEND.value: 'отправлен',
    OrderStatus.NOT_COME.value: 'не явился',
    '': OrderStatus.NEW.value,
    'доставлен': OrderStatus.SUC.value,
    'на руках': OrderStatus.ACTIVE.value,
    'на руках (забрать)': OrderStatus.ACTIVE_TAKE.value,
    'отказ': OrderStatus.REF.value,
    'принят': OrderStatus.TAKE.value,
    'забран': OrderStatus.SUC_TAKE.value,
    'отказан': OrderStatus.REF_TAKE.value,
    'переделка': OrderStatus.REMAKE.value,
    'отправлен': OrderStatus.SEND.value,
    'не явился': OrderStatus.NOT_COME.value,
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
