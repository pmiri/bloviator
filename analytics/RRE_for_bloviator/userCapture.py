#!/usr/bin/python

import praw
from pprint import pprint
import networkx as nx

# try:
#     import matplotlib.pyplot as plt
# except:
#     raise

def recCommentGrab(graph, comment, parent, level, sub):

	if ( isinstance(comment, praw.objects.MoreComments) ):
		return

	if ( comment.author == None ):
		return

	print "\t"*level, parent, "<- replies to -", comment.author

	graph.add_node(comment.author, seen=sub)

	if ( parent in graph.successors(comment.author) ):
		graph[comment.author][parent]['weight'] = graph[comment.author][parent]['weight'] + 1
	else:
		graph.add_edge(comment.author, parent, weight=1)

	if ( len(comment.replies) > 0 ):
		for rep in comment.replies:
			recCommentGrab(graph, rep, comment.author, level+1, sub)

def extractPosts(graph, redditObj, sub, l=10):

	submissions = r.subreddit(sub).top('month', limit=2)

	for post in submissions:

		if ( post.author == None ):
			continue

		author = post.author
		authorComments = author.comments.top(limit=10)

		print post.author

		commentCount = 0
		for comment in authorComments:
			if ( comment.is_root ):
				submission = comment.submission
				print "\t", submission.author
			else:
				parent = comment.parent()
				print "\t", parent.author
			commentCount+=1

		print "\tComment count:", commentCount

		replyGraph.add_node(post.author, seen=sub)

		# post.replace_more_comments(limit=10, threshold=0)

		# print "\tComment count: ", len(post.comments)

		# commentList = post.comments[:]

		# for comment in commentList:
		# 	if ( not isinstance(comment, praw.objects.MoreComments) ):
		# 		recCommentGrab(replyGraph, comment, post.author, 1, sub)
		# 	# else:
		# 	# 	moreComs = comment.comments()

		# 	# 	if ( moreComs != None ):
		# 	# 		commentList.extend(moreComs)

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

subList = [
	"sandersforpresident",
    # "political_revolution",
    # "progressive",
    # "socialism",
    # "anarchism",
    # "politics",
    # "democrats",
    # "news",
    # "worldnews",
    # "aww",
    # "trees",
    # "food",
    # "showerthoughts",
    # "the_donald",
    # "conservative",
    # "republican",
    # "libertarian",
    # "anarcho_capitalism",
    # "conspiracy"
]

try:
	for sub in subList:
		print "Checking on subreddit: /r/", sub

		extractPosts(replyGraph, r, sub, 25)

except Exception, e:
	print "Failed during execution: ", e

finally:
	nx.write_gexf(replyGraph, 'cs_user_capture.gexf')







