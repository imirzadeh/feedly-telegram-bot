import os
from flask import Flask, request, redirect

app = Flask(__name__)

def add_http_to_url(url):
	if url.find("http://") != 0 and url.find("https://") != 0:
		url = "http://" + url
	return url

@app.route('/click', methods=["GET"])
def feedly_click():
	post_id = request.args.get('id')
	return redirect()

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
