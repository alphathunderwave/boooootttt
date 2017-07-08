import tweepy, random
import markovgen
from time import sleep
import boooootttt as bot
#creates a new instance of boooootttt
bot_ = bot.bot()
with open('database.txt','r') as infile:
	#creates a new instance of Markov and inputs database.txt
	markov = markovgen.Markov(infile)
while True:
	#every 1-3 hours the bot will call the markov and tweet the text that is returned
    text = markov.generate_markov_text()
    bot_.do_tweet(text)
    rando = random.randint(3600,10800)
    sleep(rando)
