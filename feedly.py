import requests
from .credentials import FEEDLY_TOKEN


class FeedlyAPI(object):
	def __init__(self):
		self.headers = {'Authorization': FEEDLY_TOKEN}
	
	def get_new_items(self, stream):
		url = "http://cloud.feedly.com/v3/streams/contents?streamId={}&unreadOnly=true&count=100".format(stream)
		response = requests.get(url, headers=self.headers)
		return response.json()
	
	def set_mark_status(self, items, status="read"):
		url = "http://cloud.feedly.com/v3/markers"
		action = "markAsRead" if status == "read" else "keepUnread"
		data = {
			"action": action,
			"type": "entries",
			"entryIds": items
		}
		res = requests.post(url, json=data, headers=self.headers)
