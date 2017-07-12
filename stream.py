"""import functions to use"""

import tweepy, random
import markovgen
from time import sleep
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import boooootttt as bot

"""creates a new instance of bot, an incremental count and a list of developers
	(beeeeennnn_ is default)"""

bot_ = bot.bot()
count = 0
dev = ['beeeeennnn_']

"""StdOutListener is a class that listens for replies to the bot. the on status
	function runs any time the listener 'hears' a status aimed at the bot"""

class StdOutListener(StreamListener):
	def on_status(self, status):

		"""this counter only lets the bot run 15 times, then it waits for
			15 minutes to protect overusing twitter"""

		global count
		count = count + 1
		if count == 15:
			sleep(900)
			count =0

		"""the bot wont respond to itself"""

		if status.user.screen_name == 'boooootttt_':
			pass
		for user in bot_.blacklist:
			if status.user.screen_name == user:
				pass
		else:
			if status.user.screen_name in dev:

				"""these are developer options.
					add_dev: adds a dev to the list of developers.
					remove_dev: removes a dev from the list.
					dump: runs tweetdumper.
					tweet: will make the bot tweet.
					at: will make the bot tweet at an intended user"""

				if 'add_dev' in status.text:
					text = status.text.split(' ')
					if text[2] not in dev:
						dev.append(text[2])
				elif 'remove_dev' in status.text:
					if status.text[2] in dev:
						dev.pop(status.text[2])

				elif 'dump' in status.text:
					dump = bot_.dump()
					bot_.reply(status,str(dump))

				elif 'tweet' in status.text:
					response = markov.generate_markov_text()
					bot_.do_tweet(response)

				elif 'at' in status.text:
					text = status.text.split(' ')
					response = '@' + text[2] + ' ' + markov.generate_markov_text()
					bot_.do_tweet(response)

			else:

				"""this is the general reply for anyone who tagged the bot"""

				response = markov.generate_markov_text()
				bot_.reply(status,str(response))

		return True

	"""on_error prints the error status and stops the stream. this should not
		happen. if it does something is broken and needs to be fixed"""

	def on_error(self, status):
		print(status)
		return False

"""new instance of StdOutListener and markov using database.txt as an infile.
	then a stream is set up using config from the bot_. _with = 'user' lets the
	stream know we are only looking for ourself being mentioned"""

l = StdOutListener()
with open('database.txt','r') as infile:
	markov = markovgen.Markov(infile)

print('Listening')
stream = Stream(bot_.auth, l)
stream.userstream(_with='user')
