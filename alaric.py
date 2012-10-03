from time import gmtime, strftime
from praw import Reddit, errors

class Alaric:

    def __init__(self, user_agent=None, subreddits=None, logger_subreddit=None):
        
        self.user_agent = self.set_defaults(user_agent, "Alaric - The /r/wow bot for menial tasks")
        self.subreddits = self.set_defaults(subreddits, list())
        self.logger_subreddit = self.set_defaults(logger_subreddit, None)

        ##] Default robot stuff
        self.comment_footer = "\n\n----\nThis comment was posted by a robot."
        self.console_output = False

        self.user = Reddit(user_agent=self.user_agent)
        self.user.login()

    def set_defaults(self, default_test, default_value):
        
        if default_test is not None:
            defaults = default_test
        else:
            defaults = default_value

        return defaults


    def set_comment_footer(self, markdown):
        """ Accepts a plaintext string or string of
            markdown text. Currently there is no
            checks in place to make sure the user
            submits text that will work with reddit.
            """
        self.comment_footer = markdown


    def write_to_file(self, file_path, text):
        fhandler = open(file_path, 'a+')
        fhandler.write(text)
        fhandler.close()


    def set_console_output(self, output_enabled=True):
        """ Accepts boolean parameter that allows
            a user to enable console output from
            Alaric if the bot is being run in a console.
            
            If a boolean is not passed to the function,
            it will default to True.
            """
            if type(output_enabled) in (bool):
                self.console_output = output_enabled
            else:
                self.console_output = True


    def output_to_console(self, message):
        """ Outputs a message to the console if the
            user has told Alaric it is allowed to do
            so.
            """
        if self.console_output:
            print message


    def remove_posts_with_url(self, urls=None, reason=None):
        """ Grabs the 100 latest posts from the specified 
            subreddits and checks to see if they match any
            of the urls to be removed

            urls = list
            reason = string

            reason has some magic to it and allows the
            following text replacements:
              {author_name} ->  Outputs name of the submitter

            if the reason is not provided, a comment will not
            be posted to let the user know the thread was
            removed.
            """
        if urls is not None:
            
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
                        for url in urls:
                            if url in post.url:
                                print "URL Match Found.\n  " + post.url

                                if post.name in already_posted:
                                    print "Ignoring. Already replied and removed."
                                else:
                                    print "Post has not been removed or replied to"
                                    
                                    try:
                                        post.remove()
                                    except errors.APIException as e:
                                        write_to_file('error.log', e)
                                    else:
                                        print "Post has been successfully removed."

                                        try:
                                            if reason is not None:
                                                post.add_comment(reason.format(author_name=post.author) + self.comment_footer)
                                        except errors.APIException as e:
                                            write_to_file('error.log', e)
                                        else:
                                            print "Comment has been successfully posted."

                                            ##] Post a new thread to the logger reddit if specified
                                            if self.logger_subreddit is not None:

                                                submission_author = post.author
                                                submission_url = post.url
      
                                                submission_title = "Removed post with url [{url}] submitted by /u/{submission_author}".format(url=url, submission_author=submission_author)
                                                submission_text = "**REPORT**  \n\nSubmission URL: {submission_url}  \nSubmitted by: {submission_author}".format(submission_url=submission_url, submission_author=submission_author)
                                                try:
                                                    self.user.submit(self.logger_subreddit, submission_title, submission_text)
                                                except errors.APIException as e:
                                                    write_to_file('error.log', e)
                                                else:
                                                    print "Logged report to {subreddit}".format(subreddit=self.logger_subreddit)


        else:
            print "No urls provided."