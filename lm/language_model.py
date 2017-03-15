from collections import *
from random import random, shuffle
from tqdm import tqdm
from nltk.tokenize import sent_tokenize
import pickle

BLOVIATION_MAX = 50
MODEL_PATH = "/home/bloviator/models/"
MODEL_EXT = ".10mb.8.padded.pickle"
MODEL_ORDER = 8
SUBREDDITS = [
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
    'worldnews',
]

# Trains a Markov-chain-based language model on a file fname.
def train_char_lm(fname, order=10):
    data = open(fname, 'r').read()
    lm = defaultdict(Counter)
    pad = "~" * order
    data = pad + data
    for i in tqdm(range(len(data)-order)):
        history, char = data[i:i+order], data[i+order]
        lm[history][char]+=1
    def normalize(counter):
        s = float(sum(counter.values()))
        return [(c,cnt/s) for c,cnt in counter.items()]
    outlm = {hist:normalize(chars) for hist, chars in lm.items()}
    return outlm

# Generates a single letter from a given language model and history
def generate_letter(lm, history, order):
        history = history[-order:]
        dist = lm[history]
        x = random()
        for c,v in dist:
            x = x - v
            if x <= 0: return c

# Generates nletters characters of random text given a model and model order.
def generate_text(lm, order, nletters=1000, seed=None):
    history = "~" * order
    if seed is not None:
        history = ((order - len(seed)) * "~") + seed;
        if history not in lm:
            history = "~" * order
    out = []
    print("Generating text...")
    for x in tqdm(range(0, nletters)):
        c = generate_letter(lm, history, order)
        history = history[-order:] + c
        out.append(c)
    return "".join(out)

# Bloviates a single comment. A comment will be composed of only complete
# sentences and a maximum of BLOVIATION_MAX characters in total (though it can
# be of any length under 140 and over 0 characters).
#
# Throws ValueError when a subreddit not in the above SUBREDDITS list is passed
# as a parameter.
def bloviate(subreddit, seed=None):
    if subreddit not in SUBREDDITS:
        raise ValueError('Subreddit not recognized')
    file_path = MODEL_PATH + subreddit + MODEL_EXT
    print("Loading model...")
    lm = pickle.load(open(file_path, 'rb'))
    bloviation = ""
    while bloviation == "":
        bloviations = generate_text(lm, MODEL_ORDER)
        # Strip away padding characters
        bloviations = "".join(c for c in bloviations if c!="~");
        sentences = sent_tokenize(bloviations)
        # Shuffle the sentences, for fun and to increase randomness
        shuffle(sentences)
        for sentence in sentences:
            if len(sentence) < BLOVIATION_MAX \
                and len(bloviation) < BLOVIATION_MAX:
                bloviation += " " + sentence
    return bloviation
