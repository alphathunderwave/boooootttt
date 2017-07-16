"""import functions to use"""

import tweepy, random
import markovgen
from time import sleep
import boooootttt as bot

"""creates a new instance of boooootttt"""

bot_ = bot.bot()

"""creates a new instance of Markov and uses database.txt as an infile."""
with open('database.txt','r') as infile:
	markov = markovgen.Markov(infile)


"""calls generate_markov_text and sends that to the bot to tweet out.
	then the loops sleeps for a random amout of time between one and three
	hours"""

while True:
	text = markov.generate_markov_text()
	bot_.do_tweet(text)
	rando = random.randint(3600,10800)
	sleep(rando)
