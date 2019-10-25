from flask import render_template, abort, request
from app import app
import praw
import random
import requests
import requests.auth


CLIENT_ID = "zD0r60sBmdmmKA"
CLIENT_SECRET = "V45Fd29iUO6QaQwoLMfqL9_VmhE"
REDIRECT_URI = "http://localhost:5000"


@app.route('/')
@app.route('/index')
def index():
	# Generate a random string for the state parameter
	# Save it for use later to prevent xsrf attacks
	from uuid import uuid4
	state = str(uuid4())
	save_created_state(state)
	params = {"client_id": CLIENT_ID,
			  "response_type": "code",
			  "state": state,
			  "redirect_uri": REDIRECT_URI,
			  "duration": "permanent",
			  "scope": "identity",
			  "user_agent": "web_app:zD0r60sBmdmmKA:v1.0(by /u/sempre_paraos)"}
	import urllib
	sign_in_url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)
	#return render_template('index.html', title='Home', sign_in_url=sign_in_url, subreddit=subreddit)
	#reddit = praw.Reddit(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, response_type="code", duration="permanent", scope="identity")
	error = request.args.get('error', '')
	if error:
		return "Error: " + error
	state = request.args.get('state', '')
	if not is_valid_state(state):
		# Uh-oh, this request wasn't started by us!
		abort(403)
	code = request.args.get('code')
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	post_data = {"grant_type": "authorization_code",
				 "code": code,
				 "redirect_uri": REDIRECT_URI}
	response = requests.post("https://www.reddit.com/api/v1/access_token",
							 auth=client_auth,
							 data=post_data)
	token_json = response.json()
	access_token = token_json["access_token"]
	#access_token = get_token(code)
	username = get_username(access_token)
	#refresh_token = reddit.auth.authorize(code)
	#current_user = reddit.user.me()
	#subreddit =  reddit.subreddit('all').hot(limit=25)
	return render_template('index.html', title='Home', sign_in_url=sign_in_url, username=username)


# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
	pass
def is_valid_state(state):
	return True
	
'''@app.route('/reddit_callback')
def reddit_callback():
	error = request.args.get('error', '')
	if error:
		return "Error: " + error
	state = request.args.get('state', '')
	if not is_valid_state(state):
		# Uh-oh, this request wasn't started by us!
		abort(403)
	code = request.args.get('code')
	# We'll change this next line in just a moment
	access_token = get_token(code)
	return "Your reddit username is: %s" % get_username(access_token)'''
	
'''def get_token(code):
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	post_data = {"grant_type": "authorization_code",
				 "code": code,
				 "redirect_uri": REDIRECT_URI}
	response = requests.post("https://www.reddit.com/api/v1/access_token",
							 auth=client_auth,
							 data=post_data)
	token_json = response.json()
	
	return print(token_json) #token_json["access_token"]'''
	
def get_username(access_token):
    headers = {"Authorization": "bearer " + access_token}
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    return me_json['name']