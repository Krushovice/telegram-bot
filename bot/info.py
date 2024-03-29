
HELP = """
 <em>Наш бот в кратчайшие сроки поможет вам получить
статус квалифицированного инвестора для вашего брокера💼 Нам понадобиться от вас :
ваша почта📫,выписка со счёта вашего банка 🏦в формате .pdf,
а так же выбрать вашего брокера 📊
из предложенного списка(брокер не должен совпадать с банком в выписке).
Для того чтобы это сделать, из всплывающего меню выберите пункт '💵Получить услугу'</em>
"""

HELLO = """
Здравствуйте, меня зовут Арнольд!
Я помогу вам стать квалифицированным инвестором.
Пожалуйста заполните карточку клиента.
Дополнительную информацию можно получить,
воспользовавшись командой /help

"""


terms = '''\
    Для того чтобы получить услугу, необходимо произвести оплату,
    воспользовавшись командой /buy
    '''

item_title = 'Cправка'
item_description = 'Пожалуйста, перейдите по ссылке на оплату'
succesful_payment = ''' Платеж на сумму 10000 рублей успешно произведен!
В течение 24 часов на вашу почту прийдет готовая справка'''

MESSAGES = {
    'Help': HELP,
    'Hello': HELLO,
    'terms': terms,
    'succesful_payment': succesful_payment,
    'tm_title': item_title,
    'tm_description': item_description
}
