import json
from pymongo import MongoClient
from bson.objectid import ObjectId


class Item(object):
	def __init__(self, id=None, title=None, origin=False, url=None, summary=None, visual=None) :
		self.id = None
		self.title = title
		self.pushed = False
		self.read = False
		self.origin = False
		self.url = url
		self.summary = None
		self.visual = None
		self.feedly_updated = False
		self.status = "unread"
		self.content = None
		self.clicked = False
		self.engagement = None
		self.raw_feedly_json = None
	
	def to_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'pushed': self.pushed,
			'read': self.read,
			'origin': self.origin,
			'url': self.url,
			'summary': self.summary,
			'visual': self.visual,
			'feedly_updated': self.feedly_updated,
			'content': self.content,
			'clicked': self.clicked,
			'engagement': self.engagement,
			'raw_feedly_json': self.raw_feedly_json
		}
		
	def to_json(self):
		return json.dumps(self.to_dict())


class DBManager(object):
	def __init__(self):
		self.client = MongoClient('mongodb://localhost:27017/')
		self.db = self.client['feedly']
		self.items = self.db['items']
		
	def __create__indexes(self):
		self.items.create_index('id', unique=True)
		self.items.create_index('read')
		self.items.create_index('pushed')
		self.items.create_index('origin')
		self.items.create_index('url')
		self.items.create_index('clicked')
		self.items.create_index('feedly_updated')
	
	def insert_items(self, items):
		new_items = []
		for i in items:
			if self.items.find({'id': i['id']}).count() == 0:
				res = self.items.insert_one(i)
				new_items.append(str(res.inserted_id))
		return new_items
	
	def update_click_status(self, items):
		items = list(map(lambda x: ObjectId(x), items))
		self.items.update_many({'_id': {'$in': items}}, {'$set': {'clicked': True}})
		
		
	def update_items_read_status(self, items, status="read"):
		items = list(map(lambda x: ObjectId(x), items))
		if status == "read":
			self.items.update_many({'_id': {'$in': items}}, {'$set': {'read': True}})
		else:
			self.items.update_many({'_id': {'$in': items}}, {'$set': {'read': False}})
	
	def update_push_status(self, items):
		items = list(map(lambda x: ObjectId(x), items))
		self.items.update_many({'_id': {'$in': items}}, {'$set': {'pushed': True}})
		
	def update_feedly_status(self, items):
		print("setting feedly status true for items", items)
		res = self.items.update_many({'id': {'$in': items}}, {'$set': {'feedly_updated': True}})
	
	def get_unupdated_feedly(self):
		return list(self.items.find({'feedly_updated': False, 'read': True}))
		
	def get_unpushed_items(self):
		return list(self.items.find({'pushed': False}))
	
	def set_clicked(self, id):
		id = ObjectId(id)
		item = self.items.find_one_and_update({'_id': id}, {'$set': {'clicked': True}})
		return item
		
	def get_by_obj_ids(self, ids):
		ids = list(map(lambda x: ObjectId(x), ids))
		res = list(self.items.find({'_id': {'$in': ids}}))
		for r in res:
			r["_id"] = str(r["_id"])
		return res
