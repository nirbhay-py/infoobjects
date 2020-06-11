
def preprocess(tweet_tokens, stop_words = ()):
	#this method cleans the tweet tokens by removing noise such as stop-words and using lemmatization which is using the stem of a word for better analysis
    cleaned_tokens = []
    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lem = WordNetLemmatizer()
        token = lem.lemmatize(token, pos)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token
			#yield produces a series of values over time

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

def main():
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')

	#loading dataset

    text = twitter_samples.strings('tweets.20150430-223406.json')

    tweet_tokens = twitter_samples.tokenized('positive_tweets.json')[0]
	#tokenizer returns special characters such as @ and _.

    stop_words = stopwords.words('english')
	#stop_words are a list of common words that represent 'noise'

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

	#getting tokenized values for pos,neg sets

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []
	#empty arrays for cleaned vals

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(preprocess(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(preprocess(tokens, stop_words))


    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]
    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:8000]
    test_data = dataset[8000:]
    print("Training model")
    st = time.time()
    classifier = NaiveBayesClassifier.train(train_data)
    print("Model trained with time = {}s".format(time.time()-st))
    custom_tweet = str(input("Enter a string and the model will analyse its sentiment:"))
    custom_tokens = preprocess(word_tokenize(custom_tweet))
    print(custom_tweet, " is ", classifier.classify(dict([token, True] for token in custom_tokens)))

def get_imports():
	from nltk.stem.wordnet import WordNetlem
	from nltk.corpus import twitter_samples, stopwords
	from nltk.tag import pos_tag
	from nltk.tokenize import word_tokenize
	from nltk import FreqDist, classify, NaiveBayesClassifier
	import time
	import re, string, random

get_imports()
main()
