from enums import OrderStatus, CompanyDLV, OrderAction, Letter


company = {
    CompanyDLV.POST.value: 'Почта / СДЭК',
    CompanyDLV.MASTER.value: 'Мастер',
    CompanyDLV.PUTILIN.value: 'Путилин',
    CompanyDLV.MASTER_SPB.value: 'Мастер СПБ'
}

order_status_data = {
    OrderStatus.NEW.value: '',
    OrderStatus.SUC.value: 'доставлен',
    OrderStatus.ACTIVE.value: 'на руках',
    OrderStatus.ACTIVE_TAKE.value: 'на руках (забрать)',
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
    1: {'emoji': '💵', 'text': 'ЗП', 'column': 'k', 'photo': 0, 'comment': 0},
    2: {'emoji': '📱', 'text': 'Связь', 'column': 'c', 'photo': 1, 'comment': 0},
    3: {'emoji': '📦', 'text': 'Достависта', 'column': 'd', 'photo': 1, 'comment': 0},
    4: {'emoji': '🚕', 'text': 'Такси', 'column': 'e', 'photo': 1, 'comment': 0},
    5: {'emoji': '🚌', 'text': 'Транспорт', 'column': 'e', 'photo': 1, 'comment': 0},
    6: {'emoji': '🛴', 'text': 'Самокат', 'column': 'e', 'photo': 1, 'comment': 0},
    7: {'emoji': '🚃', 'text': 'Проездной Метро', 'column': 'f', 'photo': 1, 'comment': 0},
    8: {'emoji': '🏥', 'text': 'МЦ', 'column': 'g', 'photo': 0, 'comment': 1},
    9: {'emoji': '🖇', 'text': 'Канцелярия', 'column': 'h', 'photo': 1, 'comment': 0},
    10: {'emoji': '✉️', 'text': 'Почта / СДЭК', 'column': 'i', 'photo': 0, 'comment': 0},
    11: {'emoji': '💰', 'text': 'Премия', 'column': 'b', 'photo': 0, 'comment': 0},
    12: {'emoji': '🏧', 'text': 'Подписка на переводы', 'column': 'b', 'photo': 1, 'comment': 0},
    13: {'emoji': '💸', 'text': 'Разное', 'column': 'b', 'photo': 0, 'comment': 1},
}


letters = {
    Letter.D.value: 'День',
    Letter.V.value: 'Вечер',
    Letter.A.value: 'Адрес',
}

'''
💵 ЗП - в колонку K (запрос фото не требует, комментарий требует - День Вечер Адрес на основании этих данных формирует ЗП по формуле)
📱Связь - в колонку C (запрос фото требует, описание не требует)
📦 Достависта - в колонку D (запрос фото требует, описание не требует)
🚕 Такси - в колонку E (запрос фото требует, описание не требует)
🚌 Транспорт - в колонку E (запрос фото требует, описание не требует)
🛴 Самокат - в колонку E (запрос фото требует, описание не требует)
🚃 Проездной Метро - в колонку F (запрос фото требует, описание не требует)
🏥 МЦ - в колонку G (запрос фото не требует, описание требует)
🖇 Канцелярия - в колонку H (запрос фото требует, описание не требует)
✉️ Почта / СДЭК - в колонку I (запрос фото не требует, описание не требует)
💰Премия - в колонку B (запрос фото не требует, описание не требует)
🏧 Подписка на переводы - в колонку B (запрос фото требует, описание не требует)
💸 Разное - в колонку B (запрос фото не требует, описание требует)
'''

order_actions = {
    OrderAction.COST.value: 'Скидка',
    OrderAction.DELI.value: 'Доставка',
}
