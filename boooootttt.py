"""import funtions to use"""

import tweepy, sys, random, pathlib
import markovgen
import tweetdumper
from time import sleep
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import config

class bot():

	"""__init__ initiates the bot, sets up consumer and access keys and secrets
	and logs into twitter.  it also creates a list for followers. config.py is
	needed to complete the login"""

	def __init__(self):
		self.CONSUMER_KEY = config.CONSUMER_KEY
		self.CONSUMER_SECRET = config.CONSUMER_SECRET
		self.ACCESS_KEY = config.ACCESS_KEY
		self.ACCESS_SECRET = config.ACCESS_SECRET
		self.auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
		self.auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
		self.api = tweepy.API(self.auth, wait_on_rate_limit = True)
		self.following = self.api.friends_ids('boooootttt_')
		self.blacklist = []
		self.developers =['beeeeennnn_']

	"""do_tweet takes in a string and submits it to twitter. the text is trimmed
	 to make sure that the tweet does not go over twitters limit of 140
	 characters"""

	def do_tweet(self,text):
		try:
			self.api.update_status(text[0:140])
			self.log('tweet sent' )
			self.write_tweet(text)
		except tweepy.TweepError as e:
			self.log(e)


	"""reply takes in a twitter status and a string and submits the string as a
	reply to the status. like the do_tweet function, the tweet is limited to 140
	 characters"""

	def reply(self,status,text):
		words = status.text.split(' ')
		command = words[1]
		user = '@' + status.user.screen_name
		id = status.id

		if status.user.screen_name == 'boooootttt_':
			pass

		elif status.user.screen_name in self.blacklist:
			pass

		elif status.user.screen_name in self.developers:
			if '-' in command:
				self.log('dev: ')
				if command == '-dump':
					text = self.dump()

				elif command == '-check_followers':
					text = self.check_followers()

				elif command == '-blacklist_add':
					try:
						text = self.blacklist_add(words[2])

					except tweepy.TweepError as e:
						self.log(e)

				elif command == '-blacklist_remove':
					try:
						text = self.blacklist_remove(words[2])

					except tweepy.TweepError as e:
						self.log(e)

				elif command == '-ls_blacklist':
					text = self.ls_blacklist()

				elif command == '-dev_add':
					try:
						text = self.dev_add(words[2])
					except tweepy.TweepError as e:
						self.log(e)
				elif command == '-dev_remove':
					try:
						text = self.dev_remove(words[2])
					except tweepy.TweepError as e:
						self.log(e)
				elif command == '-ls_dev':
					text = self.ls_dev()
				else:
					text = 'unknown command'

		try:
			self.api.update_status((user +' ' + str(text))[0:140],id)
			self.log("tweet sent to: " + user)
			self.write_tweet(str(text))

		except tweepy.TweepError as e:
			self.log(e)

	"""random_reply replies to a random tweet from someone it is following"""

	def random_reply(self,text):
		randuser = self.api.get_user(random.choice(self.following))
		self.log(randuser.screen_name)
		timeline = self.api.user_timeline(randuser.screen_name)
		for tweet in timeline:
			if 'RT' in tweet.text:
				timeline.remove(tweet)

		self.log('random reply to: ')
		self.reply(timeline[0],text)

	"""random_retweet retweets a random tweet from someone it is following"""

	def random_retweet(self):
		randuser = random.choice(self.following)
		timeline = self.api.user_timeline(randuser)
		for tweet in timeline:
			if 'RT' in tweet.text:
				timeline.remove(tweet)

		self.log('random retweet to: ')
		try:
			self.api.retweet(timeline[0])
		except tweepy.TweepError as e:
			self.log(e)

	"""wrtite_tweet writes a sent tweet to a file for saving"""

	def write_tweet(self,text):
		with open('tweetlist.txt','a') as outfile:
			outfile.write(text)

	"""dump uses tweetdumper to make a list of all the tweets for each follower.
		these tweets are written to a file named database.txt"""

	def dump(self):
		bad_followers = []
		with open('database.txt','w') as outfile:
			outfile.write('')
		for follower in self.api.followers():
			self.log(follower.screen_name)
			try:
				tweetdumper.get_all_tweets(follower.screen_name)

			except tweepy.TweepError as e:
				self.log(e)
				bad_followers.append(follower.screen_name)

		return bad_followers


	"""check_followers is a function that follows any new followers that the bot
	 is not already following"""

	def check_followers(self):
		self.log('checking for new followers')
		f = self.api.friends_ids('boooootttt_')
		friends =[]
		bad_friends=[]
		for friend in f:
			friends.append(self.api.get_user(friend).screen_name)

		for follower in self.api.followers():
			if follower.screen_name not in friends:
				try:
					self.api.create_friendship(follower.screen_name)
					self.log('now following: ' + follower.screen_name)

				except tweepy.TweepError as e :
					self.log(e)
					bad_friends.append(follower.screen_name)

		return bad_friends

	"""blacklist_add and blacklist_remove add and remove members to the
	blacklist. ls_blacklist returns the blacklist"""

	def blacklist_add(self,name):
		if name not in self.blacklist:
			self.blacklist.append(name)
			return name + ' added to blacklist'

	def blacklist_remove(self,name):
		if name in self.blacklist:
			self.blacklist.pop(name)
			return name + ' removed from blacklist'

	def ls_blacklist(self):
		return str(self.blacklist)

	"""dev_add and dev_remove and and remove members to the developers list.
	ls_dev returns the dev list"""

	def dev_add(self,name):
		if name not in self.developers:
			self.developers.append(name)
			return name + ' added to developers'

	def dev_remove(self,name):
		if name == 'beeeeennnn_':
			return 'cannot remove beeeeennnn_ from dev list'
		elif name in self.developers:
			self.developers.pop(name)
			return name + ' removed from developers'

	def ls_dev(self):
		return str(self.developers)

"""log keeps track of all error or success messages the bot creates"""

	def log(self,text):
		with open('log.txt','a') as outfile:
			outfile.write(text + '\n')
		print(text)
