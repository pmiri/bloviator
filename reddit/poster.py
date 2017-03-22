import sys, getopt
import logging

import language_model as lm

import time
import subprocess

import praw
from praw_object_data import retry_if_broken_connection
import json

client_id = "G_rle_KDBCc7kw"
secret="QjZR808fes7P8AFzUn8mb7WYC0w"
user_agent = 'reddit posting for bloviator, using praw tutorial'

bot_list = ["left", "right", "apol"]
#our json file
json_bot_file = "bots.json"

post_list_file = 'post_list.txt'

# Logging configuration
log_file = 'log.txt'
logging.basicConfig(filename=log_file, level=logging.DEBUG)

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
def get_threads_replied_to(bot_type):
    threadfile = open(bot_type + "_" + post_list_file, 'r+')
    return threadfile.readlines()

def boot_loop():
    logger = logging.getLogger('bot_log')
    #loop
    while(True):
        for bot_type in bot_list:
            bot = loadbot(bot_type)
            reddit = poster(bot)

            logger.info('using bot: ' + bot_type + '\n')

            #this may be irrelevant givent the nature of the submission stream
            #posts = get_threads_replied_to(bot_type)
            for sub in bot["subreddits"]:
                #NOTE: you can append subreddits by +'ing them together. This will be useful when interacting with many political subs
                print('entering ' + sub + '...')
                subreddit = reddit.subreddit(sub)
                t = time.time()
                for submission in subreddit.stream.submissions.hot.comments(limit=25):
                    print('post(s) found')
                    #check to see if the bot hasn't already replied
                    if True #time.time() - t > 60*10: #TODO: figure out appropriate conditions to NOT post submission.id not in posts:
                        t = time.time()
                        print('replying in thread' + submission)

                        #if submission contains what we want, reply.
                        comment = subprocess.check_output(['python3', '/home/bloviator/lm/language_model.py', sub])
                        submission.reply(comment)
                        logger.info('r/' + sub + ':\"' + comment + '\"\n')

                        threads = open(bot_type + '_' + post_list_file, 'a+')
                        botlog = open(bot_type + '_comments', 'a+')
                        threads.write(submission.id)
                        botlog.write(submission.id + ': ' + 'TODO: comment go here')
                        logger.info("SUBMISSION ID:" + submission.id)
                        break
                        
                    sleepytime = 60*10 - (time.time() - t)
                    print('sleeping for %d', sleepytime)
                    sleep(sleepytime)


def main():
    while(True):
        print("bloviating...")
        boot_loop()

if __name__ == '__main__':
    main()
