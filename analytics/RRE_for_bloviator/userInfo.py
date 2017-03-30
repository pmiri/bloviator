#!/usr/bin/python

import praw
from pprint import pprint
import networkx as nx


# try:
#     import matplotlib.pyplot as plt
# except:
#     raise


def extractPosts(graph, redditObj, user, l=10):
    author = redditObj.redditor(user)

    print author

    print "Subreddits: "

    authorSubmissions = author.submissions.new(limit=500)
    subList = {}
    counter = 0

    for submission in authorSubmissions:
        counter += 1
        thisSubreddit = submission.subreddit.display_name

        if (not thisSubreddit in subList.keys()):
            subList[thisSubreddit] = 1
        else:
            subList[thisSubreddit] += 1

    sorted_subList = sorted(subList, key=subList.get)

    for subreddit in sorted_subList:
        print "\t", subreddit, subList[subreddit]

    print "Total Submissions: ", counter

    authorComments = author.comments.top(limit=1000)
    subList = {}

    print "Subreddit Comments:"

    commentCount = 0
    for comment in authorComments:
        if (comment.is_root):
            print "ROOT"
        commentCount += 1
        thisSubreddit = comment.subreddit.display_name

        if (not thisSubreddit in subList.keys()):
            subList[thisSubreddit] = 1
        else:
            subList[thisSubreddit] += 1

    sorted_subList = sorted(subList, key=subList.get)

    for subreddit in sorted_subList:
        print "\t", subreddit, subList[subreddit]

    print "Total Comments: ", commentCount

    print "Replies: "

    authorComments = author.comments.top(limit=1000)
    commentCount = 0
    for comment in authorComments:
        if (comment.is_root):
            submission = comment.parent()
            print "\t", submission.author
        else:
            parent = comment.parent()
            print "\t", parent.author
        commentCount += 1

    print "\tComment count:", commentCount


replyGraph = nx.DiGraph()

# password = raw_input('Password:')
#
# r = praw.Reddit(user_agent='edu.umd.cs.inst633o.cbuntain')
# r.login('proteius',password)

r = praw.Reddit(client_id='fJvsPpDJaUSIPQ',
                client_secret='jj-qI-SacUWH3csuV3kyMQiPmgQ',
                password='COMP498N',
                user_agent='/u/grandpasterflash trying the open-source Reddit Response Extractor',
                username='grandpasterflash')

userList = [
    "PM_ME_YOUR_NEUROSIS",
    "stopdropandrocknroll",
    "loveandlightning"
]

try:
    for user in userList:
        print "Checking on user: /u/", user

        extractPosts(replyGraph, r, user, 25)

except Exception, e:
    print "Failed during execution: ", e

finally:
    nx.write_gexf(replyGraph, 'cs_user_info.gexf')
