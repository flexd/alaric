# This is an example script that we use for /r/wow
from alaric import Alaric

##] Some configurating
banned_urls = ['qkme.me', 'quickmeme.com']
subreddits = ['wow']
logger_subreddit = "wowcaretaker"

##] Startup a new instance of Alaric
wowbot = Alaric(subreddits=subreddits, logger_subreddit=logger_subreddit)

wowbot.remove_banned_urls(banned_urls)