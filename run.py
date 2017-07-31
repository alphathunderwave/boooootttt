"""import functions to use"""

import tweepy, random
import markovgen
from time import sleep
import boooootttt as bot
import os
import recrrent_keras


"""creates a new instance of boooootttt"""

bot_ = bot.bot()

"""creates a new instance of Markov and uses database.txt as an infile."""
with open('database.txt','r') as infile:
	markov = markovgen.Markov(infile)


"""calls generate_markov_text and sends that to the bot to tweet out.
	then the loops sleeps for a random amout of time between one and three
	hours"""

randcount = random.randint(20,50)




bot_.dump()

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
