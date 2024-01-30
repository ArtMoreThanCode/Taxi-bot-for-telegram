from telebot import types
from db import USER, TAXI, SUM, PASS, ADMIN, NOTIFICATION
import telebot
from config import TOKEN, OWN_ADMIN

bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')

count_zakaz = 0

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    user = USER.check_user(message.chat.id)
    user_bun = USER.check_bun_user(message.chat.id)

    count = SUM.get_sum('city')[0]
    count2 = SUM.get_sum('suburb')[0]

    if user_bun != True:
        if user == None:
            markup = types.InlineKeyboardMarkup()
            item_1 = types.InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')
            markup.add(item_1)

            bot.send_message(message.chat.id, 'Вы не зарегистрированы! \n\nНажмите кнопку для регистрации', reply_markup=markup)

        else:
            if message.chat.id == OWN_ADMIN:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn_1 = types.KeyboardButton(text='Выставить цену тарифов')
                btn_2 = types.KeyboardButton(text='Выставить цену деревни')
                btn_3 = types.KeyboardButton(text='Добавить водителя')
                btn_4 = types.KeyboardButton(text='Заблокировать пользователя')
                btn_5 = types.KeyboardButton(text='Редактировать водителя')
                btn_6 = types.KeyboardButton(text='Список пользователей')
                btn_7 = types.KeyboardButton(text='Список водителей')
                btn_8 = types.KeyboardButton(text='Колл-во пользователей')
                btn_9 = types.KeyboardButton(text='Колл-во заказов за сегодня')
                btn_10 = types.KeyboardButton(text='Сделать рассылку сообщений таксистам')
                btn_11 = types.KeyboardButton(text='Сделать рассылку сообщений всем пользователям')
                item_1 = types.KeyboardButton(text='Заказать машину 🚕')
                item_2 = types.KeyboardButton(text='Тех. поддержка ☎')
                markup.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_8, btn_9, btn_10, btn_11, item_1, item_2)

                bot.send_message(message.chat.id, f'Нажмите на кнопку если хотите изменить цену тарифов. \n\nРекомендованная цена тарифа для города: {count}руб.\nЦены тарифа для пригорода уточняйте у водителя!', reply_markup=markup)
            else:
                if TAXI.check_taxist(message.chat.id) == True:
                    if TAXI.get_tru_taxi(message.chat.id) == True:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item_1 = types.KeyboardButton(text='Выйти c линии')
                        balance = types.KeyboardButton(text='Выручка за сегодня')
                        item_2 = types.KeyboardButton(text='Заказать машину 🚕')
                        item_3 = types.KeyboardButton(text='Тех. поддержка ☎')
                        markup.add(item_1, item_2, item_3)

                        bot.send_message(message.chat.id, f'Привет! Через этого бота ты можешь работать в такси нажав на кнопку. Или сообщить о проблеме в Тех. поддержку \n\nРекомендованная цена тарифа для города: {count}руб.\nЦены тарифа для пригорода уточняйте у водителя!', reply_markup=markup)
                    else:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item_1 = types.KeyboardButton(text='Выйти на линию')
                        item_2 = types.KeyboardButton(text='Заказать машину 🚕')
                        item_3 = types.KeyboardButton(text='Тех. поддержка ☎')
                        markup.add(item_1, item_2)

                        bot.send_message(message.chat.id, f'Привет! Через этого бота ты можешь работать в такси нажав на кнопку. Или сообщить о проблеме в Тех. поддержку \n\nРекомендованная цена тарифа для города: {count}руб.\nЦены тарифа для пригорода уточняйте у водителя!', reply_markup=markup)
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item_1 = types.KeyboardButton(text='Заказать машину 🚕')
                    item_2 = types.KeyboardButton(text='Тех. поддержка ☎')
                    markup.add(item_2, item_1)

                    bot.send_message(message.chat.id, f'Привет! В этом боте ты можешь заказать машину нажав на кнопку. Или сообщить о проблеме в Тех. поддержку \n\nРекомендованная цена тарифа для города: {count}руб.\nЦены тарифа для пригорода уточняйте у водителя!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Вы заблокированы! \nУ вас нет доступа к функциям этого бота!')

@bot.message_handler(content_types=['text'])
def text(message: types.Message):
    user_id = message.chat.id

    try:
        if message.text == 'Заказать машину 🚕':
            user = TAXI.check_client(user_id)
            
            rt = TAXI.random_taxist()

            if rt == None:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='start')
                markup.add(item)
                
                bot.send_message(message.chat.id, 'В данный момент водителей на линии нет. Попробуйте повторить заказ через 5 минут', reply_markup=markup)
            else:
                if user == None:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                    btn1 = types.KeyboardButton(text='Город 🏙')
                    btn2 = types.KeyboardButton(text='Пригород 🌳')
                    markup.add(btn1, btn2)
        
                    bot.send_message(user_id, 'Выберите тариф', reply_markup=markup)
                    bot.register_next_step_handler(message, ta)
                else:
                    bot.send_message(user_id, 'Вы уже заказали машину, ожидайте!')

        elif message.text == 'Тех. поддержка ☎':
            bot.send_message(message.chat.id, 'Напишите сообщение, и я отправлю его в Тех. Поддержку')
            bot.register_next_step_handler(message, rep)

        elif message.text == 'Вернуться в главное меню':
            start(message)
        
        elif message.text == 'Выставить цену тарифов':
            if message.chat.id == OWN_ADMIN:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                btn1 = types.KeyboardButton(text='Город 🏙')
                btn2 = types.KeyboardButton(text='Пригород 🌳')
                markup.add(btn1, btn2)

                bot.send_message(user_id, 'Выберите область в которой хотите изменить цену', reply_markup=markup)
                bot.register_next_step_handler(message, rate)
        
        elif message.text == 'Выйти на линию':
            if TAXI.check_taxist(message.chat.id) == True:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item_1 = types.KeyboardButton(text='Выйти с линии')
                item_2 = types.KeyboardButton(text='Тех. поддержка ☎')
                markup.add(item_1, item_2)

                TAXI.insert_taxist_line(user_id)
                bot.send_message(user_id, 'Вы успешно вышли на линию! Ищем для вас заказ ⏳', reply_markup=markup)
        
        elif message.text == 'Выйти c линии':
            if TAXI.check_taxist(message.chat.id) == True:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item_1 = types.KeyboardButton(text='Выйти на линию')
                item_2 = types.KeyboardButton(text='Тех. поддержка ☎')
                markup.add(item_1, item_2)

                TAXI.del_taxist_line(user_id)
                bot.send_message(user_id, 'До связи!', reply_markup=markup)
        
        elif message.text == 'Добавить водителя':
            if user_id == OWN_ADMIN:
                bot.send_message(user_id, 'Введите пароль для водителя.')
                bot.register_next_step_handler(message, insert_taxist)
        
        elif message.text == 'Заблокировать пользовател':
            if user_id == OWN_ADMIN:
                bot.send_message(user_id, 'Введите `ID` пользователя')
                bot.register_next_step_handler(message, bun_user)

        elif message.text == 'Список пользователей':
            if user_id == OWN_ADMIN:
                user = USER.user_list()
        
                for row in user:
                    id = row[0]
                    name = row[1]
                    phone = row[2]

                    bot.send_message(user_id, f'\n\n__<------------------------------------------------->\n\nПользователь: `{name}` \nID: `{id}` \nСотовый телефон: `{phone}`\n\n<------------------------------------------------->__\n\n')
        
        elif message.text == 'Список водителей':
            if user_id == OWN_ADMIN:
                user = USER.tax_list()
        
                for row in user:
                    id = row[0]
                    name = row[1]
                    phone = row[2]

                    bot.send_message(user_id, f'\n\n__<------------------------------------------------->\n\nПользователь: `{name}` \nID: `{id}` \nСотовый телефон: `{phone}`\n\n<------------------------------------------------->__\n\n')

        elif message.text == 'Колл-во пользователей':
            if user_id == OWN_ADMIN:
                count_user = USER.count_users()
                bot.send_message(user_id, f'На данный момент в боте: `{count_user}` пользователей')

        elif message.text == 'Колл-во заказов за сегодня':
            if user_id == OWN_ADMIN:
                bot.send_message(user_id, f'Сегодня было сделано: `{count_zakaz}` заказов')
        
        elif message.text == 'Выручка за всё время':
            if TAXI.check_taxist(message.chat.id) == True:
                sum_day = USER.get_sum_day(user_id)

                bot.send_message(user_id, f'Ваша выручка за всё время состовляет: `{sum_day}`руб.')
        
        elif message.text == 'Редактировать водителя':
            if user_id == OWN_ADMIN:
                bot.send_message(user_id, 'Введите ФИО водителя которого хотите изменить')
                bot.register_next_step_handler(message, edit_taxists)
        
        elif message.text == 'Сделать рассылку сообщений таксистам':
            admin = ADMIN.get_admin()

            admins = []
            
            for row in admin:
                admins.append(int(row[0]))

            if user_id == OWN_ADMIN:
                bot.send_message(user_id, 'Введите текст рассылки')
                bot.register_next_step_handler(message, tax_notific)
            else:
                print(admins)
                if user_id in admins:
                    bot.send_message(user_id, 'Введите текст рассылки')
                    bot.register_next_step_handler(message, tax_notific)

        elif message.text == 'Сделать рассылку сообщений всем пользователям':
            adm = ADMIN.get_admin()
            for row in adm:
                if user_id == OWN_ADMIN or user_id in adm[0]:
                    bot.send_message(user_id, 'Введите текст рассылки')
                    bot.register_next_step_handler(message, notific)

        else:
            if message.text == PASS.get_pass(message.text)[0]:
                bot.send_message(message.chat.id, 'Напишите ваше ФИО')
                bot.register_next_step_handler(message, reg_taxist)
                PASS.del_pred_pass(message.text)
            else:
                bot.send_message(user_id, 'Я не знаю такую команду :/')
    except:
        pass

def tax_notific(message):
    text = message.text
    users = NOTIFICATION.notific_taxist()

    list = []

    for row in users:
        list.append(row[0])
    for user in list:
        print(user)
        bot.send_message(user, text)

    bot.send_message(message.chat.id, 'Сообщение успешно отправлено!')

def notific(message):
    text = message.text
    users = NOTIFICATION.notific()
    
    list = []

    for row in users:
        list.append(row[0])
    for user in list:
        print(user)
        bot.send_message(user, text)

    bot.send_message(message.chat.id, 'Сообщение успешно отправлено!')

def edit_taxists(message):
    user = message.text

    if USER.check_taxist(user) == True:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        name = types.KeyboardButton(text='Изменить информацию о ФИО')
        phone = types.KeyboardButton(text='Изменить информацию о номере телефона')
        car = types.KeyboardButton(text='Изменить информацию о машине')
        markup.add(name, phone, car)

        bot.send_message(message.chat.id, 'Отлично! Теперь выберите что хотите изменить у этого водителя', reply_markup=markup)
        bot.register_next_step_handler(message, edit_taxists_next, user)
    else:
        bot.send_message(message.chat.id, 'Такого водителя нет в базе!')
        start(message)

def edit_taxists_next(message, user):
    edited = message.text

    if edited == 'Изменить информацию о ФИО':
        bot.send_message(message.chat.id, 'Введите данные которые хотите записать вместо старых')
        bot.register_next_step_handler(message, edit_name, user)
    elif edited == 'Изменить информацию о номере телефона':
        bot.send_message(message.chat.id, 'Введите данные которые хотите записать вместо старых')
        bot.register_next_step_handler(message, edit_phone, user)
    elif edited == 'Изменить информацию о машине':
        bot.send_message(message.chat.id, 'Введите данные которые хотите записать вместо старых')
        bot.register_next_step_handler(message, edit_car, user)

def edit_name(message, user):
    name = message.text
    USER.edit_driver(user, 'full_name', name)
    bot.send_message(message.chat.id, 'Отлично! Вы успешно изменили данные!')
    start(message)

def edit_phone(message, user):
    phone = message.text
    USER.edit_driver(user, 'phone', phone)
    bot.send_message(message.chat.id, 'Отлично! Вы успешно изменили данные!')
    start(message)

def edit_car(message, user):
    car = message.text
    USER.edit_driver(user, 'car', car)
    bot.send_message(message.chat.id, 'Отлично! Вы успешно изменили данные!')
    start(message)

def bun_user(message):
    id = message.text

    try:
        bun = USER.check_bun_user(id)
        if bun == True:
            bot.send_message(message.chat.id, 'Этот пользователь уже заблокирован!')
        else:
            USER.bun_user(id)
            bot.send_message(message.chat.id, 'Вы успешно заблокировали пользователя!')
            start(message)
            bot.send_message(id, 'Вас заблокировали! \nЭта блокировка не временная, вы больше не получите доступ к функциям этого бота. \nУдачи!')
    except:
        bot.send_message(message.chat.id, 'Возникла ошибка!')
        start(message)

def reports(user, text):
    adm = ADMIN.get_admin()
    for row in adm:
        ad = row[0]
        bot.send_message(ad, f'Сообщение от польователя: @{user} \n\nСообщение: `{text}`')

def rep(message):
    text = message.text

    reports(message.from_user.username, text)
    
    bot.send_message(message.chat.id, 'Сообщение отправленно в Тех. Поддержку')

def reg(message):
    phone = message.text
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='start')
    markup.add(item)
    
    user = USER.register(message.chat.id, message.from_user.first_name, phone)
    
    bot.send_message(message.chat.id, user, reply_markup=markup)

def insert_taxist(message):
    password = message.text
    PASS.set_pass(password)
    bot.send_message(message.chat.id, f'Отлично! Теперь отправьте этот пароль: `{password}` водителю.')

def reg_taxist(message):
    full_name = message.text
    bot.send_message(message.chat.id, 'Теперь введите свой номер телефона в таком виде: +71002003040')
    bot.register_next_step_handler(message, reg_car, full_name)

def reg_car(message, full_name):
    phone = message.text
    bot.send_message(message.chat.id, 'Теперь введите свой номер машины в таком виде: *123*')
    bot.register_next_step_handler(message, reg_tax, full_name, phone)

def reg_tax(message, full_name, phone):
    car = message.text
    user_id = message.chat.id
    
    tax = USER.check_taxist(user_id)

    if tax == True:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.InlineKeyboardButton(text='Вернуться в главное меню', callback_data='start')
        markup.add(item)

        bot.send_message(user_id, 'Вы уже зарегистрированы как водитель!', reply_markup=markup)

    USER.reg_taxist(user_id, full_name, phone, car)

    bot.send_message(message.chat.id, f'Превосходно! Рады видеть вас: `{full_name}` в нашей команде!')

def rate(message):
    rate = message.text

    bot.send_message(message.chat.id, "Отлично! Теперь введите сумму для этой области")
    bot.register_next_step_handler(message, sum_rate, rate)

def sum_rate(message, rate):
    sum = int(message.text)

    if sum != int:
        bot.send_message(message.chat.id, 'Это не число!')
        start(message)
    
    if rate == 'Город 🏙':
        SUM.insert_sum(sum, 'city')

    elif rate == 'Пригород 🌳':
        SUM.insert_sum(sum, 'suburb')

    bot.send_message(message.chat.id, f'Вы успешно установили цену: `{sum}`руб. для: `{rate}`')
    start(message)

def ta(message):
    rate = message.text

    if "Город" in rate or "Пригород" in rate:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Отлично! Теперь отправьте адрес откуда вас нужно забрать', reply_markup=markup)
        bot.register_next_step_handler(message, tax, rate)
    else:
        bot.send_message(message.chat.id, 'Такой тариф не найден... Повторите заказ!')
        start(message)

def tax(message, rate):
    _in = message.text
    bot.send_message(message.chat.id, 'Отлично! Теперь отправьте адрес куда вас нужно отвезти')
    bot.register_next_step_handler(message, taxi, rate, _in)
    
def taxi(message, rate, _in, _out=None, client_id=None, ret=3, clos=0, mes_id=0):
    if rate == 'Город 🏙' or rate == 'city':
        count = SUM.get_sum('city')[0]

    if rate == 'Пригород 🌳' or rate == 'suburb':
        count = SUM.get_sum('suburb')[0]

    if clos == 0:
        remove = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'Ваш заказ ожидает принятия водителем. Ожидайте⌛', reply_markup=remove)
            
    if ret == 1:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text='Завершить заказ', callback_data='cloz_zakaz')
        btn1 = types.InlineKeyboardButton(text='Я на месте', callback_data='i_go')
        markup.add(btn, btn1)

        cl_markup = types.ReplyKeyboardRemove()

        TAXI.accept(message.chat.id, client_id)
        TAXI.del_taxi(client_id)

        taxist_nm = TAXI.get_taxist_name(message.chat.id)[0]
        taxist_ph = TAXI.get_taxist_phone(message.chat.id)[0]
        taxist_car = TAXI.get_taxist_car(message.chat.id)[0]

        count_zakaz + 1

        USER.insert_sum_day(message.chat.id, count)
        
        bot.send_message(message.chat.id, 'Вы приняли заказ! Когда приедите на место откуда надо забрать - нажмите кнопку: `Я на месте` \n\nЧто бы звершить поездку, нажмите на кнопку: `Завершить заказ`', reply_markup=markup)
        
        bot.send_message(client_id, f'Водитель: `{taxist_nm}` принял ваш заказ! \n\nЕго номер телефон для связи: `{taxist_ph}` \nЕго машина: `{taxist_car}` \n\nКогда ваша поездка закончится, попросите водителя завершить заказ!', reply_markup=cl_markup)
    
    if ret == 2:
        user = TAXI.random_taxist()

        if user != None:
            markup = types.InlineKeyboardMarkup(row_width=1)
            accept = types.InlineKeyboardButton(text='Принять заказ ✅', callback_data=f'accept_{message.chat.id}')
            close = types.InlineKeyboardButton(text='Отменить заказ ❌', callback_data=f'close_{message.chat.id}')
            markup.add(accept, close)

            bot.send_message(user, f'Новый заказ! \n\nИз: `{_in}`\n В: `{_out}` \n\nСумма: `{count}`руб.', reply_markup=markup)
        
    if ret == 3:
        _out = message.text
            
        TAXI.client(message.chat.id, rate, _in, _out)
        user = TAXI.random_taxist()

        if user != None:
            markup = types.InlineKeyboardMarkup(row_width=1)
            accept = types.InlineKeyboardButton(text='Принять заказ ✅', callback_data=f'accept_{message.chat.id}')
            close = types.InlineKeyboardButton(text='Отменить заказ ❌', callback_data=f'close_{message.chat.id}')
            markup.add(accept, close)

            bot.send_message(user, f'Новый заказ! \n\nОкруг: `{rate}` \n\nИз: `{_in}`\n В: `{_out}`\n\n Сумма: `{count}`', reply_markup=markup)
        
def comment(message, client, user_id):
    tax_name = TAXI.get_taxist_name(user_id)[0]

    coment = message.text

    bot.send_message(OWN_ADMIN, f'Новый отзыв о водителе! \n\nИмя водителя: `{tax_name}` \nОтзыв: *{coment}*')

    bot.send_message(client, 'Спасибо за отзыв! С помощью вас мы делаем наш сервис лучше!')

@bot.callback_query_handler(func=lambda call: True)
def callback(call: types.CallbackQuery):
    user_id = call.message.chat.id
    message = call.message

    if call.data == 'reg':
        bot.send_message(user_id, 'Введите свой номер телефона в таком виде: +71002003040')
        bot.register_next_step_handler(message, reg)
    
    elif call.data == 'start':
        start(message)

    elif 'accept' in call.data:
        us_id = call.data.split('_')[1]
        user = TAXI.get_taxi(us_id)

        for row in user:
            usr_id = row[0]
            rate = row[1]
            _in = row[2]
            _out = row[3]
            
            markup = types.ReplyKeyboardMarkup()
            bot.edit_message_reply_markup(user_id, message.id, reply_markup=markup)

            taxi(message, rate=rate, _in=_in, _out=_out, client_id=usr_id, ret=1, clos=1, mes_id=message.id)


    elif 'close' in call.data:
        bot.delete_message(user_id, message.id)

        client_id = call.data.split('_')[1]
        
        user = TAXI.get_taxi(client_id)

        for row in user:
            usr_id = row[0]
            rate = row[1]
            _in = row[2]
            _out = row[3]

            taxi(message, rate=rate, _in=_in, _out=_out, client_id=client_id, ret=2, clos=1)
    
    elif 'cloz_zakaz' in call.data:
        bot.delete_message(user_id, message.id)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_1 = types.KeyboardButton(text='Заказать машину 🚕')
        item_2 = types.KeyboardButton(text='Тех. поддержка ☎')
        markup.add(item_2, item_1)

        tax_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_1 = types.KeyboardButton(text='Выйти c линии')
        item_2 = types.KeyboardButton(text='Тех. поддержка ☎')
        markup.add(item_1, item_2)

        user = TAXI.get_client_taxi(user_id)[0]

        if user != None:
            TAXI.close_zakaz(user_id)

            bot.send_message(user_id, 'Вы успешно завершили поездку!', reply_markup=tax_markup)
            
            msg = bot.send_message(user, 'Поездка завершена! Оставьте отзыв о водителе:')
            bot.register_next_step_handler(msg, comment, user, user_id)
        else:
            bot.send_message(user_id, 'У вас нет поездки что бы её завершить!')
    
    elif 'i_go' in call.data:
        taxist = TAXI.check_taxist(user_id)

        if taxist == True:
            client = TAXI.get_client_taxi(user_id)[0]            
            
            if client != None:
                bot.send_message(client, 'Водитель подъехал к вам!')
    
    elif call.data == 'insert_sum':
        SUM.insert_sum(int(message.text))
        bot.send_message(user_id, f'Вы успешно установили сумму заказов на {message.text}')

if __name__ == '__main__':
    try:
        print('Бот в сети!')
        bot.polling()   
    except Exception as e:
        for adm in ADMIN.get_admin()[0]:
            admin = adm
            bot.send_message(admin, f'Ошибка бота! \n\nОписание ошибки: {e}')
        
        bot.polling()