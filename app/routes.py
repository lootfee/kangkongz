from flask import render_template, abort, request, redirect, url_for
from app import app
import praw
import random
import requests
import requests.auth
import json
from uuid import uuid4
import urllib
import datetime

#visitor_clientid = str(random.randint(512, 1024))
#visitor_secret_key = str(random.randint(512, 1024))

CLIENT_ID = "zD0r60sBmdmmKA"
CLIENT_SECRET = "V45Fd29iUO6QaQwoLMfqL9_VmhE"
REDIRECT_URI = "http://localhost:5000"
#USER_AGENT = '"web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)"'

reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent="web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)")

					 
@app.route('/')
@app.route('/index')
def index():
	'''reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent="web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)")
	reddit.read_only = True'''
	reddit = ''
	code = request.args.get('code')
	access_token = ''
	username = ''
	#page = request.args.get('page', 1, type=int)
	if access_token:
		reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     refresh_token=access_token,
                     user_agent="web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)")
		print(reddit.auth.scopes())
	elif code:
		reddit = praw.Reddit(client_id=CLIENT_ID,
					 client_secret=CLIENT_SECRET,
					 redirect_uri=REDIRECT_URI,
					 user_agent="web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)")
		access_token = reddit.auth.authorize(code)
		print(access_token)
		username = reddit.user.me()#get_username(access_token)
		#subreddit = get_subreddit(access_token)
		#print(access_token)
	else:
		reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent="web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)")
		reddit.read_only = True
	phgonewild = reddit.subreddit('phgonewild').new(limit=10)
	return render_template('index.html', title='Home', username=username, phgonewild=phgonewild)

@app.route('/login')
def login():
	state = str(random.randint(0, 65000))
	'''params = {"client_id": CLIENT_ID,
			  "response_type": "code",
			  "state": state,
			  "redirect_uri": REDIRECT_URI,
			  "duration": "permanent",
			  "scope": "identity, read, save, submit",
			  "user_agent": "web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)"}
	sign_in_url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params)'''
	reddit = praw.Reddit(client_id='zD0r60sBmdmmKA',
                     client_secret='V45Fd29iUO6QaQwoLMfqL9_VmhE',
                     redirect_uri='http://localhost:5000',
                     user_agent='web_app:zD0r60sBmdmmKA:v1.0(by /u/sempre_paraos)')
	return redirect(reddit.auth.url(['identity, read, save, submit'], state, "permanent"))#redirect("https://ssl.reddit.com/api/v1/authorize?" + urllib.parse.urlencode(params))
	
@app.route('/phr4r')
def phr4r():
	reddit.read_only = True
	username = ''
	phr4r = reddit.subreddit('phr4r').new(limit=10)
	return render_template('index.html', title='Home', username=username, phr4r=phr4r)
	
@app.route('/phgonewildcouples')
def phgonewildcouples():
	reddit.read_only = True
	username = ''
	phgonewildcouples = reddit.subreddit('phgonewildcouples').new(limit=10)
	return render_template('index.html', title='Home', username=username, phgonewildcouples=phgonewildcouples)
	
@app.route('/gonewild')
def gonewild():
	reddit.read_only = True
	username = ''
	gonewild = reddit.subreddit('gonewild').new(limit=10)
	return render_template('index.html', title='Home', username=username, gonewild=gonewild)
	
	
@app.route('/gonewildtube')
def gonewildtube():
	reddit.read_only = True
	username = ''
	gonewildtube = reddit.subreddit('gonewildtube').new(limit=10)
	return render_template('index.html', title='Home', username=username, gonewildtube=gonewildtube)
	
@app.route('/asiansgonewild')
def asiansgonewild():
	reddit.read_only = True
	username = ''
	asiansgonewild = reddit.subreddit('asiansgonewild').new(limit=10)
	return render_template('index.html', title='Home', username=username, asiansgonewild=asiansgonewild)


@app.route('/couplesgonewild')
def couplesgonewild():
	reddit.read_only = True
	username = ''
	couplesgonewild = reddit.subreddit('couplesgonewild').new(limit=10)
	return render_template('index.html', title='Home', username=username, couplesgonewild=couplesgonewild)



# Left as an exercise to the reader.
# You may want to store valid states in a database or memcache,
# or perhaps cryptographically sign them and verify upon retrieval.
def save_created_state(state):
	pass
def is_valid_state(state):
	return True
	
@app.route('/reddit_callback')
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
	return "Your reddit username is: %s" % get_username(access_token)
	
def get_token(code):
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	post_data = {"grant_type": "authorization_code",
				 "code": code,
				 "redirect_uri": REDIRECT_URI}
	headers = {"User-Agent":"web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)"}
	response = requests.post("https://www.reddit.com/api/v1/access_token",
							 auth=client_auth,
							 data=post_data,
							 headers=headers)
	token_json = response.json()
	refresh_token = token_json["refresh_token"]
	refresh_post_data = {"grant_type": "refresh_token",
				 "refresh_token": refresh_token}
	refresh_response = requests.post("https://www.reddit.com/api/v1/access_token",
							 auth=client_auth,
							 data=refresh_post_data,
							 headers=headers)
	refresh_token_json = refresh_response.json()
	return refresh_token_json["access_token"]
	
'''def get_refresh_token(refresh_token):
	client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
	post_data = {"grant_type": "refresh_token",
				 "refresh_token": refresh_token}
	headers = {"User-Agent":"web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)"}
	response = requests.post("https://ssl.reddit.com/api/v1/access_token",
							 auth=client_auth,
							 data=post_data,
							 headers=headers)
	token_json = response.json()
	return token_json["refresh_token"]'''
	
def get_username(access_token):
	headers = {"Authorization": "bearer " + access_token, "User-Agent":"web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)"}
	response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
	me_json = response.json()
	return me_json['name']
	
def get_subreddit(access_token):
	headers = {"Authorization": "bearer " + access_token, "User-Agent":"web_app:k3rn1tz1123:v1.0(by /u/sempre_paraos)"}
	payload = {'show': 'all'}
	response = requests.get("https://oauth.reddit.com/api/v1/subreddits/default", headers=headers)
	me_json = response.json()
	print(me_json)
	#return me_json['name']