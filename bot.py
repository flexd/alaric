# This is an example script that we use for /r/wow
from alaric import Alaric

##] Some configurating
subreddits = ['wow', 'fluxflashor']
logger_subreddit = "wowcaretaker"

bad_urls = {
    'meme_urls': {
        'sites': ['qkme.me', 'quickmeme.com', 'memegenerator.net'],
        'reason': "Greetings {author_name},\n\nI have removed your post as it violates our subreddit policy towards memes.\n\n> No GM Jokes, memes, rage comics/faces.\n\nI suggest you try your submission over in /r/wowcomics instead. Have a great day =)"
    },
    'exploit_sites': {
        'sites': ['ownedcore.com', 'masterofwarcraft.net', 'd3scene.com', 'blizzhackers.cc', 'elitepvpers.com', 'hackforums.net', 'deathsoft.com'],
        'reason': "Greetings {author_name},\n\nThe website you have linked to has been known to distribute to hacks and exploits and because of our subreddit policy against them, I have gone ahead and removed your link. Relevant policy info:\n\n> Cheats, hacks, and exploits are not welcome in this subreddit.\n\nBetter safe than sorry! Heave a great day =)"
    },
    'emulation_sites': {
        'sites': ['trinitycore.info', 'arcemu.org', 'ac-web.org', 'getmangos.com', 'mmotop.org'],
        'reason': "Greetings {author_name},\n\nI have removed your post as it violates our subreddit policy towards WoW Emulation. This community does not endorse private servers and has no plans to. Why don't you try posting in /r/wowservers instead. Have a great day =)"
    },
}

##] Startup a new instance of Alaric
wowbot = Alaric(subreddits=subreddits, logger_subreddit=logger_subreddit)

##] Setup some /r/wow specific settings
wowbot.set_comment_footer("\n\n----\nThis comment was posted by a robot. If you believe it was an error, please contact [the moderation team](http://www.reddit.com/message/compose?to=%2Fr%2Fwow).")

##] Remove bad urls
for _, url in bad_urls.iteritems():
    wowbot.remove_posts_with_url(url['sites'], url['reason'])
