import requests
from .credentials import POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN

json_header = {'Content-type': 'application/json'}


def add_to_pocket(url):
	pocket_data = {
		"consumer_key": POCKET_CONSUMER_KEY,
		"access_token": POCKET_ACCESS_TOKEN,
		"url": url
	}
	pocket_api = "https://getpocket.com/v3/add"
	return requests.post(url=pocket_api, json=pocket_data, headers=json_header)