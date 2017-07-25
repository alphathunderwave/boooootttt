"""import functions to use"""

import tweepy, random
import markovgen
from time import sleep
import boooootttt as bot
import recurrent_keras
import os.path

"""creates a new instance of boooootttt"""

bot_ = bot.bot()

"""creates a new instance of Markov and uses database.txt as an infile."""
with open('database.txt','r') as infile:
	markov = markovgen.Markov(infile)


"""calls generate_markov_text and sends that to the bot to tweet out.
	then the loops sleeps for a random amout of time between one and three
	hours"""

randcount = random.randint(20,50)

recurrent_keras.recurrent(DATA_DIR = './data/beeeeennnn_.txt')
for follower in bot_.api.followers():
	screen_name = follower.screen_name
	print(screen_name)
	if os.path.exists('./data/' + screen_name + '.txt'):
		recurrent_keras.recurrent(DATA_DIR = './data/' + screen_name + '.txt', WEIGHTS = './saved/model.hdf5')
	else:
		print('no file for ' + screen_name)

'''while True:
	count = 0
	sleepnum = random.randint(3600,10800)
	text = markov.generate_markov_text()
	if count == randcount:
		if random.choice([True,False]):
			bot_.random_reply(text)
		else:
			bot_.random_retweet()
		count = 0
		randcount = random.randint(20,50)
	else:
		bot_.do_tweet(text)
		count = count + 1
	sleep(sleepnum)'''
