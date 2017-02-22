import praw
from praw_object_data import retry_if_broken_connection
from enum import Enum

client_id = "G_rle_KDBCc7kw"
secret="QjZR808fes7P8AFzUn8mb7WYC0w"
username='bloviator-bot'
password='COMP498N'
user_agent = 'reddit posting for bloviator, using praw tutorial'

#our subreddit
test_subreddit = 'bloviationzone'

post_list_file = 'post_list.txt'

@retry_if_broken_connection
def poster():
    r = praw.Reddit(client_id=client_id,
                    client_secret=secret,
                    username=username,
                    password=password,
                    user_agent=user_agent)

    return r

def get_threads_replied_to():
    threadfile = open(post_list_file, 'r')
    return threadfile.readlines()

def main():
    reddit = poster()

    posts = get_threads_replied_to()

    #NOTE: you can append subreddits by +'ing them together. This will be useful when interacting with many political subs
    subreddit = reddit.subreddit(test_subreddit)
    for submission in subreddit.stream.submissions():
        print('post found')
        #check to see if the bot hasn't already replied
        if submission.id not in posts:
            print('replying in thread')
            #if submission contains what we want, reply.
            submission.reply('YO THIS WAS AUTOMATED. CAN U BEELEEVE THAT?')

            threads = open(post_list_file, 'a')
            threads.write(submission.id)


if __name__ == '__main__':
    main()
