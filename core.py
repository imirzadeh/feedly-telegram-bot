from .feedly import FeedlyAPI
from .db import DBManager, Item


STREAMS = [
	"user/80e083cf-ebdf-4510-a368-00083cf1fd95/category/hackernews",
	"user/80e083cf-ebdf-4510-a368-00083cf1fd95/category/TechCrunch",
]


class Core(object):
	def __init__(self):
		self.db = DBManager()
		self.feedly = FeedlyAPI()

	def make_item(self, data):
		item = Item()
		item.id = data.get("id")
		item.title = data.get("title", "--")
		item.origin = data.get("origin", {}).get("title", "--")
		item.url = data.get("originId", "http://google.com")
		item.summary = data.get("summary", {}).get("content")
		item.visual = data.get("visual", {}).get("url", None)
		item.content = data.get("content", {}).get("content")
		item.engagement = data.get("engagement", 0)
		item.raw_feedly_json = data
		return item

	def add_new_items(self, items):
		return self.db.insert_items(items)

	def fetch_new_items(self):
		new_items = []
		for s in STREAMS:
			data = self.feedly.get_new_items(s)
			items = data.get("items")
			if not data or not items:
				continue
			for i in items:
				new_item = self.make_item(i)
				new_items.append(new_item.to_dict())
		return self.add_new_items(new_items)

	def push(self, items):
		self.db.update_push_status(items)

	def update_item(self, item_id, status):
		print("updaing {} to {}".format(item_id, status))
		self.db.update_items_read_status([item_id], status)

	def get_by_obj_ids(self, ids):
		return self.db.get_by_obj_ids(ids)

	def update_feedly(self):
		unupdated_items = list(filter(lambda x: x['id'], self.db.get_unupdated_feedly()))
		print("NUM >>> ", str(len(unupdated_items)))
		if len(unupdated_items) == 0:
			return
		unupdated_items = [i['id'] for i in unupdated_items]
		self.feedly.set_mark_status(unupdated_items)
		self.db.update_feedly_status(unupdated_items)
		# for i in range(int(len(unupdated_items) / 10)):
		# 	print("YO, {}".format(i))
		# 	curitems = unupdated_items[50*i: 50*i+50]
		# 	self.feedly.set_mark_status(curitems)
		# 	self.db.update_feedly_status(curitems)

if __name__ == "__main__":
	core = Core()
	core.update_feedly()
# 	core.fetch_new_items()
