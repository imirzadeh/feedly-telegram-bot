import re
from .settings import CLICK_TRACKER_URL


def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext


def build_menu(buttons,
			   n_cols,
			   header_buttons=None,
			   footer_buttons=None):
	menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
	if header_buttons:
		menu.insert(0, header_buttons)
	if footer_buttons:
		menu.append(footer_buttons)
	return menu


def add_tracker_url(data):
	tracker_url = '{}/click?id={}'.format(CLICK_TRACKER_URL, data['_id'])
	return tracker_url
	

def make_html(data):
	data['url'] = add_tracker_url(data)
	summary = data.get("summary")
	if not summary:
		summary = data.get("content")
	
	if not summary:
		summary = "no description"
	summary = cleanhtml(summary)
	if not data.get("visual") or not summary or summary == "Comment":
		res =  """
		[ <a href="{}" >{}</a> ] <a href="{}"> {} </a>
		<b></b>
		{}
		""".format(data['url'], data['origin'], data['url'], cleanhtml(data['title']), summary)
	else:
		res =  """
		[ <a href="{}">{}</a> ]: <a href="{}"> {} </a>
		<b></b>
		{}
		""".format(data['visual'], data['origin'], data['url'], cleanhtml(data['title']), summary)
	return res
