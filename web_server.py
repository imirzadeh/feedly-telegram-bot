import os
from flask import Flask, request, redirect
from .db import DBManager, Item

app = Flask(__name__)
mongo_db = DBManager()


def create_redirect_url(url):
	if url.find("http://") != 0 and url.find("https://") != 0:
		url = "http://" + url
	return url


@app.route('/feedly/click', methods=["GET"])
def feedly_click():
	post_id = request.args.get('id')
	post = mongo_db.set_clicked(post_id)
	return redirect(create_redirect_url(post['url']))


if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
