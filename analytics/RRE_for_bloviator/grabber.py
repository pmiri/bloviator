#!/usr/bin/python

import networkx as nx
import praw
import praw.models


# try:
#     import matplotlib.pyplot as plt
# except:
#     raise

def recCommentGrab(graph, comment, parent, level, sub):
    if (isinstance(comment, praw.models.MoreComments)):
        return

    if (comment.author is None):
        return

    author = comment.author.name

    print "\t"*level, parent, "<- replies to -", comment.author

    graph.add_node(author, seen=sub)

    if (parent in graph.successors(author)):
        graph[author][parent]['weight'] = graph[author][parent]['weight'] + 1
    else:
        graph.add_edge(author, parent, weight=1)

    if (len(comment.replies) > 0):
        for rep in comment.replies:
            recCommentGrab(graph, rep, author, level + 1, sub)


def extractPosts(graph, redditObj, sub, l=10):
    submissions = r.subreddit(sub).top('month', limit=10)

    for post in submissions:

        print post.author, post

        if (post.author == None):
            continue

        replyGraph.add_node(post.author.name, seen=sub)

        post.comments.replace_more(limit=5, threshold=0)

        print "\tComment count: ", len(post.comments)

        commentList = post.comments[:]

        for comment in commentList:
            if (not isinstance(comment, praw.models.MoreComments)):
                recCommentGrab(replyGraph, comment, post.author.name, 1, sub)
            else:
            	moreComs = comment.comments()

            	if ( moreComs != None ):
            		commentList.extend(moreComs)


# password = raw_input('Password:')

# r = praw.Reddit(user_agent='edu.umd.cs.inst633o.cbuntain')
# r.login('proteius',password)

r = praw.Reddit(client_id='fJvsPpDJaUSIPQ',
                client_secret='jj-qI-SacUWH3csuV3kyMQiPmgQ',
                password='COMP498N',
                user_agent='/u/grandpasterflash trying the open-source Reddit Response Extractor',
                username='grandpasterflash')

subList = [
    "sandersforpresident",
    "political_revolution",
    "progressive",
    "socialism",
    "anarchism",
    "politics",
    "democrats",
    "news",
    "worldnews",
    "aww",
    "trees",
    "food",
    "showerthoughts",
    "the_donald",
    "conservative",
    "republican",
    "libertarian",
    "anarcho_capitalism",
    "conspiracy"
]

for sub in subList:

    replyGraph = nx.DiGraph()

    try:
        print "Checking on subreddit: /r/", sub

        extractPosts(replyGraph, r, sub, 100)

    except Exception, e:
        print "Failed during execution: ", e

    finally:
        nx.write_gexf(replyGraph, ('%s.gexf' % sub))
