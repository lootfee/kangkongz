import os
import random

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	POSTS_PER_PAGE = 20