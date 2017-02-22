import praw
from praw_object_data import retry_if_broken_connection
import json

client_id = "G_rle_KDBCc7kw"
secret="QjZR808fes7P8AFzUn8mb7WYC0w"
user_agent = 'reddit posting for bloviator, using praw tutorial'

#our json file
json_bot_file = "bots.json"

post_list_file = 'post_list.txt'

def loadbot( str ):
    json_data=open(json_bot_file).read()
    data = json.loads(json_data)[str]
    return data

@retry_if_broken_connection
def poster( bot ):
    r = praw.Reddit(client_id=client_id,
                    client_secret=secret,
                    username=bot["username"],
                    password=bot["password"],
                    user_agent=user_agent)

    return r

#TODO: change so that it queries and populates bot specific file, instead of this default
def get_threads_replied_to():
    threadfile = open(post_list_file, 'r')
    return threadfile.readlines()

def main():
    bot = loadbot("test")
    reddit = poster(bot)

    posts = get_threads_replied_to()

    #NOTE: you can append subreddits by +'ing them together. This will be useful when interacting with many political subs
    subreddit = reddit.subreddit('+'.join(bot["subreddits"]))
    for submission in subreddit.stream.submissions():
        print('post(s) found')
        #check to see if the bot hasn't already replied
        if submission.id not in posts:
            print('replying in thread')
            #if submission contains what we want, reply.
            submission.reply('YO THIS WAS AUTOMATED. CAN U BEELEEVE THAT?')

            threads = open(post_list_file, 'a')
            threads.write(submission.id)


if __name__ == '__main__':
    main()
