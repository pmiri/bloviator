import language_model as lm
import pickle

datapath = '../data/v1/'
extension = '.txt'
modelpath = 'models/'
modelext = '.pickle'

subreddits = [
    'anarchism',
    'anarcho_capitalism',
    'aww',
    'conservative',
    'conspiracy',
    'democrats',
    'food',
    'libertarian',
    'news',
    'political_revolution',
    'politics',
    'progressive',
    'republican',
    'sandersforpresident',
    'showerthoughts',
    'socialism',
    'the_donald',
    'trees',
    'worldnews.1',
]

for subreddit in subreddits:
    print("Building model for ", subreddit)
    filename = datapath + subreddit + extension
    model12 = lm.train_char_lm(filename, order=12)
    modelfile = modelpath + subreddit + modelext
    pickle.dump(model12, open(modelfile, 'wb'))
