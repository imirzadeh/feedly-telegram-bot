import logging
import json

from .helpers import build_menu, make_html, add_tracker_url
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler

from .core import Core
from .pocket import add_to_pocket
from .settings import FEED_REFERESH_RATE_HOURS
from .credentials import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

core = Core()


def get_menu(id):
	button_list = [
		InlineKeyboardButton("read", callback_data="{}_read".format(id)),
		InlineKeyboardButton("save pocket", callback_data="{}_pocket".format(id))
	]
	return button_list


def push_data(bot, items):
	pushed_items = []
	for item in items:
		try:
			reply_markup = InlineKeyboardMarkup(build_menu(get_menu(item['_id']), n_cols=2))
			txt = make_html(item)
			bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=txt, parse_mode='HTML', reply_markup=reply_markup)
			pushed_items.append(item['_id'])
		except Exception as e:
			raise e
	core.push(pushed_items)
	core.update_feedly()


def callback_query(bot, update):
	cq = update.callback_query
	data = cq.data
	item_id = data.split("_")[0]
	item_status = data.split("_")[1]
	pocket = False
	if item_status == "read":
		core.update_item(item_id, item_status)
	elif item_status == "pocket":
		data = core.get_by_obj_ids([item_id])[0]
		url = data.get("url")
		if url:
			pocket = True
	
	bot.delete_message(TELEGRAM_CHAT_ID, cq.message.message_id)
	if pocket:
		bot.answer_callback_query(cq.id, text="saved to pocket")
	else:
		bot.answer_callback_query(cq.id, text="set read status")


def texts(_, update):
	bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="Hello, This is Iman's feedly bot")


def attach_handlers():
	start_handler = CommandHandler("hello", texts)
	dispatcher.add_handler(start_handler)
	callback_handler = CallbackQueryHandler(callback_query)
	dispatcher.add_handler(callback_handler)


def callback_half_minute(bot, job):
	items = core.fetch_new_items()
	items = core.get_by_obj_ids(items)
	logger.info("new_items")
	for i in items:
		logger.info(i['_id'])
	push_data(bot, items)
	

if __name__ == "__main__":
	updater = Updater(TELEGRAM_BOT_TOKEN)
	dispatcher = updater.dispatcher
	bot = updater.bot
	attach_handlers()
	j = updater.job_queue
	job_minute = j.run_repeating(callback_half_minute, interval=int(FEED_REFERESH_RATE_HOURS*3600), first=0)
	updater.start_polling()
