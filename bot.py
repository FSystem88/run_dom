#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Dev: https://github.com/FSystem88
# Tg: https://t.me/FSystem88

import requests as r, threading, random
from datetime import datetime as dt
from datetime import timedelta as tdl
from telebot import *
from telebot.types import *

TOKEN = ""
bot = TeleBot(TOKEN, parse_mode="html")
dev = 355821673
dir = "/root/rundom"
url = "http://127.0.0.1/rundom.php"
admins = [355821673]

bot.send_message(dev, "<b>Restart</b>", disable_notification=True)

def getuser(message: Message):
	if message.chat.type == "private":
		res = r.post(url, data={ "data":"getuser", "chatid":message.chat.id } ).json()
		if res == []:
			r.post(url, data={ "data":"adduser", "chatid":message.chat.id, "name":f"{message.chat.first_name}", "username":message.chat.username} )
		else:
			r.post(url, data={ "data":"updateuser", "chatid":message.chat.id, "name":f"{message.chat.first_name}", "username":message.chat.username} )
		user = r.post(url, data={ "data":"getuser", "chatid":message.chat.id } ).json()[0]
		return user


@bot.message_handler(commands=['start'])
def START(message:Message):
	chatid = message.chat.id
	if message.chat.type == "private":
		if getuser(message)['ban'] == "1":
			bot.send_message(chatid, "<i>Заявка на доступ к боту отправлена администратору!</i>" )
			for admin in admins:
				key = InlineKeyboardMarkup()
				but1 = InlineKeyboardButton(text="❌ Запретить", callback_data=f"ban_{chatid}")
				but2 = InlineKeyboardButton(text="✅ Разрешить", callback_data=f"allow_{chatid}")
				key.add(but1, but2)
				bot.send_message(admin, f"<b>New user:</b> <a href='tg://user?id={chatid}'>{message.chat.first_name}</a>\n<b>Username:</b> @{message.chat.username}\n<b>ID:</b> <code>{chatid}</code>\n", reply_markup=key)
		else:
			key = ReplyKeyboardMarkup(resize_keyboard=True)
			if chatid in admins:
				key.row("Создать")
			bot.send_message(chatid, "Привет! Я бот для отбора участников футбольных матчей.\nЖди регистрации и не выключай уведомления!", reply_markup=key)

def main(chatid):
	key = ReplyKeyboardMarkup(resize_keyboard=True)
	if int(chatid) in admins:
		key.row("Создать")
	bot.send_message(chatid, "Привет! Я бот для отбора участников футбольных матчей.\nЖди регистрации и не выключай уведомления!", reply_markup=key)


@bot.message_handler(commands=['profile'])
def profile(message:Message):
	user = getuser(message)
	if message.chat.type == "private" and user['ban'] != "1":
		if user['luck'] != "0":
			date = dt.strftime(dt.strptime(user['date_luck'], "%d.%m.%Y %H:%M") + tdl(weeks=3), "%d.%m.%Y %H:%M")
			text = f"У Вас есть счастливый билет, который даёт Вам 100% проход на следующую игру. Успейте им воспользоваться до {date}."
		else:
			text = "У Вас нет счастливого билета. Он даётся тем, кто зарегистрировался на игру, но не прошел отбор. Билет даётся со сроком на 3 недели, он даёт возможность 1 раз пройти регистрацию со 100% выигрышем."
		bot.send_message(message.chat.id, f"Имя: {user['name']}\n\n{text}")


@bot.message_handler(commands=['rules'])
def text(message:Message):
	bot.send_message(message.chat.id, """
	Правила:
	# НЕОБХОДИМО НАПИСАТЬ ПРАВИЛА УЧАСТИЯ 
	""")


@bot.message_handler(commands=['active'])
def text(message:Message):
	game = r.post(url, data={ "data":"activegame" }).json()
	if game == []:
		bot.send_message(message.chat.id, "Активных регистраций на матч нету! Не выключай уведомления и дождись открытия регистрации!")
	else:
		game = game[0]
		text = ""
		key = InlineKeyboardMarkup()
		key.add( InlineKeyboardButton( text="Зарегистрироваться", callback_data=f"reg_{game['id']}" ) )
		users = str(game['users']).split(" ")
		users.remove("")
		if len(users) > 0:
			text = "<u>Участники</u>:\n"
			for user in users:
				user = r.post(url, data={ "data":"getuser", "chatid":user }).json()[0]
				text += f"<a href='tg://user?id={user['chatid']}'>{user['name']}</a>\n"
		luckers = str(game['luckers']).split(" ")
		luckers.remove("")
		if len(luckers) > 0:
			text += "<u>Счастливчики</u>:\n"
			for user in luckers:
				user = r.post(url, data={ "data":"getuser", "chatid":user }).json()[0]
				text += f"<a href='tg://user?id={user['chatid']}'>{user['name']}</a>\n"
		bot.send_message(message.chat.id, f"<b>ОТКРЫТА РЕГИСТРАЦИЯ! #{game['id']}</b>\nКоличество мест: {game['count']}\nОписание: {game['note']}\n\nВнимание! Регистрация закроется {game['end']}!\n\n{text}", reply_markup=key)


@bot.message_handler(content_types=['text'])
def text(message:Message):
	getuser(message)
	if message.text == "Создать" and message.chat.id in admins:
		create0(message)


def create0(message: Message):
	chatid = message.chat.id
	key = ReplyKeyboardMarkup(resize_keyboard=True)
	key.row("Отмена")
	bot.send_message(chatid, f"Введите описание:", reply_markup=key)
	bot.register_next_step_handler(message, create1)
# получаем описание
def create1(message: Message):
	chatid = message.chat.id
	text = message.text
	if text == "Отмена":
		START(message)
		bot.clear_step_handler(message)
	else:
		note = message.text
		key = ReplyKeyboardMarkup(resize_keyboard=True)
		key.row("Отмена")
		ex = dt.strftime(dt.now(), "%d.%m.%Y %H:%M")
		bot.send_message(chatid, f"Введите дату начала регистрации в формате:\n<code>{ex}</code>", reply_markup=key)
		bot.register_next_step_handler(message, create2, note)
# получаем дату старта и проверяем её
def create2(message: Message, note):
	chatid = message.chat.id
	text = message.text
	if text == "Отмена":
		START(message)
		bot.clear_step_handler(message)
	else:
		try:
			if dt.strptime(text, "%d.%m.%Y %H:%M"):
				if dt.strptime(text, "%d.%m.%Y %H:%M") > dt.now():
					key = ReplyKeyboardMarkup(resize_keyboard=True)
					key.row("Отмена")
					ex = dt.strftime(dt.now(), "%d.%m.%Y %H:%M")
					bot.send_message(chatid, f"Введите дату окончания регистрации в формате:\n<code>{ex}</code>")
					bot.register_next_step_handler(message, create3, note, start=text)

				else:
					key = ReplyKeyboardMarkup(resize_keyboard=True)
					key.row("Отмена")
					ex = dt.strftime(dt.now(), "%d.%m.%Y %H:%M")
					bot.send_message(chatid, f"Это время уже прошло, укажите верную дату.\nДату и время надо присылать в следующем формате:\n<code>{ex}</code>", reply_markup=key)
					bot.register_next_step_handler(message, create2, note)
		except:
			key = ReplyKeyboardMarkup(resize_keyboard=True)
			key.row("Отмена")
			ex = dt.strftime(dt.now(), "%d.%m.%Y %H:%M")
			bot.send_message(chatid, f"Некорректная дата.\nДату и время надо присылать в следующем формате:\n<code>{ex}</code>", reply_markup=key)
			bot.register_next_step_handler(message, create2, note)
# получаем дату окончания и проверяем её
def create3(message: Message, note, start):
	chatid = message.chat.id
	text = message.text
	if text == "Отмена":
		START(message)
		bot.clear_step_handler(message)
	else:
		try:
			if dt.strptime(text, "%d.%m.%Y %H:%M"):
				if dt.strptime(text, "%d.%m.%Y %H:%M") > dt.strptime(start, "%d.%m.%Y %H:%M"):
					key = ReplyKeyboardMarkup(resize_keyboard=True)
					key.row("Отмена")
					bot.send_message(chatid, "Введите количество победителей:", reply_markup=key)
					bot.register_next_step_handler(message, create4, note, start, end=text)

				else:
					key = ReplyKeyboardMarkup(resize_keyboard=True)
					key.row("Отмена")
					ex = dt.strftime(dt.now(), "%d.%m.%Y %H:%M")
					bot.send_message(chatid, f"Ошибка!\nУказанная дата раньше, чем дата старта.\nДату и время надо присылать в следующем формате:\n<code>{ex}</code>", reply_markup=key)
					bot.register_next_step_handler(message, create3, note, start)
		except:
			key = ReplyKeyboardMarkup(resize_keyboard=True)
			key.row("Отмена")
			ex = dt.strftime(dt.now(), "%d.%m.%Y %H:%M")
			bot.send_message(chatid, f"Некорректная дата.\nДату и время надо присылать в следующем формате:\n<code>{ex}</code>", reply_markup=key)
			bot.register_next_step_handler(message, create3, note, start)
# получаем кол-во игроков 
def create4(message: Message, note, start, end):
	chatid = message.chat.id
	text = message.text
	if text == "Отмена":
		START(message)
		bot.clear_step_handler(message)
	else:
		try:
			if int(text):
				count = text
				res = r.post(url, data={ "data":"addgame", "start":start, "end": end, "count": count, "note":note}).text
				main(message.chat.id)
				key = InlineKeyboardMarkup()
				but1 = InlineKeyboardButton(text="❌ Cancel", callback_data=f"delgame_{res}")
				but2 = InlineKeyboardButton(text="✅ Done", callback_data=f"run_{res}")
				key.add(but1, but2)
				bot.send_message(chatid, f"Игра #{res}\nНачало: {start}\nКонец: {end}\nМест: {count}\nОписание: {note}\n\n<b>Готово?</b>", reply_markup=key)

		except:
			key = ReplyKeyboardMarkup(resize_keyboard=True)
			key.row("Отмена")
			bot.send_message(chatid, "Ошибка!\nВведите количество играков-счастливчиков:", reply_markup=key)
			bot.register_next_step_handler(message, create4)



def run(game):
	game = r.post(url, data={ "data":"getgame", "game":game }).json()[0]
	while True:
		if dt.now()>= dt.strptime(game['start'], "%d.%m.%Y %H:%M"):
			r.post(url, data={ "data":"rungame", "game":game['id'] })
			allusers = r.post(url, data={ "data":"allusers" }).json()
			for user in allusers:
				try:
					key = InlineKeyboardMarkup()
					key.add( InlineKeyboardButton( text="Зарегистрироваться", callback_data=f"reg_{game['id']}" ) )
					bot.send_message(user['chatid'], f"<b>ОТКРЫТА РЕГИСТРАЦИЯ! #{game['id']}</b>\nКоличество мест: {game['count']}\nОписание: {game['note']}\n\nВнимание! Регистрация закроется {game['end']}!", reply_markup=key)
					time.sleep(0.25)
				except:
					pass
			break

def stop(game):
	game = r.post(url, data={ "data":"getgame", "game":game }).json()[0]
	while True:
		if dt.now()>= dt.strptime(game['end'], "%d.%m.%Y %H:%M"):
			r.post(url, data={ "data":"stopgame", "game":game['id'] })
			threading.Thread(target=results, args=(game['id'], )).start()
			for admin in admins:
				try:
					bot.send_message(admin, f"<b>Регистрация #{game['id']} закрыта!</b>")
				except:
					pass
			break

def results(game):
	game = r.post(url, data={ "data":"getgame", "game":game }).json()[0]
	for admin in admins:
		try:
			bot.send_message(admin, f"<i>Подсчёт #{game['id']}...</i>")
		except:
			pass

	count = int(game['count'])
	
	users = str(game['users']).split(" ")
	if "" in users:
		users.remove("")
	random.shuffle(users)
	
	luckers = str(game['luckers']).split(" ")
	if "" in luckers:
		luckers.remove("")
	random.shuffle(luckers)

	all = luckers+users
	winners = all[:count]
	losers = all[count:]

	print(winners)
	print(losers)
	text = f"<b>Результаты #{game['id']}</b>\n\n<u>Победители</u>:\n"
	for win in winners:
		user = r.post(url, data={ "data":"getuser", "chatid":win } ).json()[0]
		text += f"<a href='tg://user?id={win}'>{user['name']}</a>\n"
	text += "\n<u>Получили счастливый билет</u>:\n"
	for lose in losers:
		user = r.post(url, data={ "data":"getuser", "chatid":lose } ).json()[0]
		text += f"<a href='tg://user?id={lose}'>{user['name']}</a>\n"
		if user['luck'] == "0":
			date_luck = dt.strftime(dt.now(), "%d.%m.%Y %H:%M")
			r.post(url, data={ "data":"addluck", "chatid":lose , "date_luck": date_luck})
	for user in winners+losers:
		try:
			bot.send_message(user, text)
		except:
			for admin in admins:
				try:
					bot.send_message(admin, f"<i><a href='tg://user?id={user}'>Пользователь</a> остановил бота!</i>")
				except:
					pass
		time.sleep(0.25)
	
	r.post(url, data={ "data":"winners", "game":game['id'], "winners":winners  })



@bot.callback_query_handler(func=lambda call: True)
def inline(call: CallbackQuery):
	arr = call.data.split("_")
	message = call.message
	data = arr[0]

	if data == "ban":
		chatid = arr[1]
		r.post(url, data={ "data":"deluser", "chatid":chatid })
		key = InlineKeyboardMarkup()
		key.add(InlineKeyboardButton(text="❌ Отказано", callback_data="pass"))
		bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.id, reply_markup=key)
		try:
			bot.send_message(chatid, "<i>В доступе отказано!</i>")
		except:
			pass

	elif data == "allow":
		chatid = arr[1]
		r.post(url, data={ "data":"allowuser", "chatid":chatid })
		key = InlineKeyboardMarkup()
		key.add(InlineKeyboardButton(text="✅ Одобрено", callback_data="pass"))
		bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.id, reply_markup=key)
		try:
			bot.send_message(chatid, "<i>Доступ разрешен!</i>")
		except:
			pass
		main(chatid)

	elif data == "delgame":
		game = arr[1]
		r.post(url, data={ "data":"delgame", "game":game })
		key = InlineKeyboardMarkup()
		bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="<i>Очищено</i>", reply_markup=key)
		main(message.chat.id)

	elif data == "run":
		game = arr[1]
		res = r.post(url, data={ "data":"getgame", "game":game }).json()[0]
		start = res['start']

		threading.Thread(target=run, args=(game, )).start()
		threading.Thread(target=stop, args=(game, )).start()
		key = InlineKeyboardMarkup()
		bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.id, reply_markup=key)
		bot.send_message(message.chat.id, f"<i>Готово!\nРегистрация запустится {start}</i>")

	elif data == "reg":
		getuser(message)
		chatid = message.chat.id
		game = arr[1]
		game = r.post(url, data={ "data":"getgame", "game":game }).json()[0]
		if game['status'] == "stop":
			bot.answer_callback_query(call.id, f"Регистрация была завершена {game['end']}!", show_alert=True)
		else:
			users = str(game['users']).split(' ')
			users.remove("")
			if str(chatid) in users:
				bot.answer_callback_query(call.id, "Вы уже зарегистрированы!", show_alert=True)
			else:
				user = r.post(url, data={ "data":"getuser", "chatid":message.chat.id } ).json()[0]
				if int(user['luck']) > 0:
					end_lucky = dt.strptime(user['date_luck'], "%d.%m.%Y %H:%M") + tdl(weeks=3)
					if end_lucky < dt.now():
						r.post(url, data={ "data":"delluck", "chatid":chatid })
						users = f"{game['users']} {chatid}"
						r.post(url, data={ "data":"newusers", "game":game['id'], "users":users })
						bot.answer_callback_query(call.id, "Вы зарегистрировались!", show_alert=True)
					else:
						key = InlineKeyboardMarkup()
						but1 = InlineKeyboardButton(text="❌ Нет", callback_data=f"noluck_{game['id']}")
						but2 = InlineKeyboardButton(text="✅ Да", callback_data=f"yesluck_{game['id']}")
						key.add(but1, but2)
						end_lucky = dt.strftime(end_lucky, "%d.%m.%Y %H:%M")
						bot.send_message(chatid, f"У вас есть счастливый проездной, действующий до {end_lucky}!\n\nИспользовать его?", reply_markup=key)
				else:
					newusers = f"{game['users']} {chatid}"
					r.post(url, data={ "data":"newusers", "game":game['id'], "users":newusers })
					bot.answer_callback_query(call.id, "Вы зарегистрировались!", show_alert=True)

	elif data == "noluck":
		chatid = message.chat.id
		game = arr[1]
		game = r.post(url, data={ "data":"getgame", "game":game }).json()[0]
		users = f"{game['users']} {chatid}"
		r.post(url, data={ "data":"newusers", "game":game['id'], "users":users })
		bot.answer_callback_query(call.id, "Вы зарегистрировались!", show_alert=True)
		bot.delete_message(message_id=message.id, chat_id=message.chat.id)

	elif data == "yesluck":
		chatid = message.chat.id
		game = arr[1]
		game = r.post(url, data={ "data":"getgame", "game":game }).json()[0]
		luckers = f"{game['luckers']} {chatid}"
		r.post(url, data={ "data":"newluckers", "game":game['id'], "luckers":luckers })
		r.post(url, data={ "data":"delluck", "chatid":chatid })
		bot.answer_callback_query(call.id, "Вы зарегистрировались с приоритетом!", show_alert=True)
		bot.delete_message(message_id=message.id, chat_id=message.chat.id)



while True:
	try:
		bot.polling()
	except Exception as E:
		time.sleep(1)
