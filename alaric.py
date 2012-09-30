from time import gmtime, strftime
from praw import Reddit

class Alaric:

    def __init__(self, user_agent=None, subreddits=None, banned_urls=None, logger_subreddit=None):
        
        self.user_agent = self.set_defaults(user_agent, "Alaric - The /r/wow bot for menial tasks")
        self.subreddits = self.set_defaults(subreddits, list())
        self.banned_urls = self.set_defaults(banned_urls, list())
        self.logger_subreddit = self.set_defaults(logger_subreddit, None)

        ##] Robot commenting is awesome
        self.robot_comment_footer = "\n\n----\nThis comment was posted by a robot. If you believe this was in error, please contact its creator [here](http://www.reddit.com/message/compose/?to=fluxflashor)"
        self.banned_url_comment_reply = "Greetings {author_name},\n\nI have removed your post as it violates our subreddit policy towards memes.\n\n> No GM Jokes, memes, rage comics/faces.\n\nI suggest you try your submission over in /r/wowcomics instead. Have a great day =)"

        self.user = Reddit(user_agent=self.user_agent)
        self.user.login()

    def set_defaults(self, default_test, default_value):
        
        if default_test is not None:
            defaults = default_test
        else:
            defaults = default_value

        return defaults

    def remove_banned_urls(self, banned_urls=None):
        """ Grabs the 100 latest posts from the specified 
            subreddits and checks to see if the banned urls 
            matches any of them"""
        if banned_urls is not None:
            
            if len(self.subreddits) < 1:
                print "No subreddits provided."
            else:    
                for subreddit in self.subreddits:

                    sr = self.user.get_subreddit(subreddit)
                    post_id = 0
                    new_posts = sr.get_new(limit=100)

                    try:
                        posts_file = open(subreddit+".posts", 'r')
                    except IOError:
                        already_posted = ""
                    else: 
                        already_posted = posts_file.read()
                        posts_file.close()

                    for post in new_posts:
                        post_id += 1
                        #print post
                        for banned_url in banned_urls:
                            if banned_url in post.url:
                                print "Banned URL found.\n  " + post.url

                                if post.name in already_posted:
                                    print "Ignoring. Already replied and removed."
                                else:
                                    print "Post has not been removed or replied to"
                                    
                                    try:
                                        post.remove()
                                    except APIException:
                                        pass
                                    else:
                                        print "Post has been successfully removed."

                                        try:
                                            post.add_comment(self.banned_url_comment_reply.format(author_name=post.author) + self.robot_comment_footer)
                                        except APIException:
                                            pass
                                        else:
                                            print "Comment has been successfully posted."

                                            ##] Post a new thread to the logger reddit if specified
                                            if logger_subreddit is not None:

                                                submission_author = post.author
                                                submission_url = post.url
      
                                                submission_title = "Removed post with url [{banned_url}] submitted by /u/{submission_author}".format(banned_url=banned_url,submission_author=submission_author)
                                                submission_text = "**REPORT**  \n\nSubmission URL: {submission_url}  \nSubmitted by: {submission_author}"
                                                try:
                                                    self.user.submit(logger_subreddit, submission_title, submission_text)
                                                except APIException:
                                                    pass
                                                else:
                                                    print "Logged report to {subreddit}".format(subreddit=logger_subreddit)


        else:
            print "No banned urls provided."