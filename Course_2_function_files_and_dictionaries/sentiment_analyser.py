
punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
# lists of words to use
positive_words = []
with open("positive_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())


negative_words = []
with open("negative_words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())
            
            
            
# string punctuation stripping
def strip_punctuation(string):
    clean_string = string
    for char in punctuation_chars:
        if char in clean_string:
            clean_string = clean_string.replace(char, "")
            
            
    return clean_string


# count negative words
def get_neg(sentence):
    word_list = strip_punctuation(sentence).lower().split(" ")
    neg_count = 0
    for word in word_list:
        if word in negative_words:
            neg_count += 1
                        
    return neg_count



# count positive words
def get_pos(sentence):
    word_list = strip_punctuation(sentence).lower().split(" ")
    pos_count = 0
    for word in word_list:
        if word in positive_words:
            pos_count += 1
                        
    return pos_count


# create a dictionary with each tweet as a key whose value is a dict containing its data.
# 
with open("project_twitter_data.csv") as tweets_file:
    d_tweets = {} # a dict with each tweet as a key
    for index, line in enumerate(tweets_file):
        if index != 0: #skip the heading (tweet_text,retweet_count,reply_count)
            #remove white space from the line and split into a 3-element list.
            tweet_data = line.strip().split(",")
            # access the value of the first element
            tweet_txt = tweet_data[0]
            # count the pos words in the text
            pos_count = get_pos(tweet_txt)
            # count the neg words in the text
            neg_count = get_neg(tweet_txt)
            # calculate net score
            net_score = pos_count - neg_count
            # assign it to the dictionary with 
            # the tweet text as the key and assign the value to be its data.
            d_tweets[tweet_txt] = d_tweets.get(tweet_txt, 
                                                   dict(retweet_count = tweet_data[1], 
                                                        reply_count = tweet_data[2], 
                                                        pos_score = pos_count, 
                                                        neg_score = neg_count, 
                                                        net_score = net_score))
            
            
            
    #print(d_tweets)

# write a csv with the dict contents
with open("resulting_data.csv", "w") as res_file:
    # write a header
    #tweet_txt = 'tweet_txt'
    retweet_count = 'Number of Retweets'
    reply_count = 'Number of Replies'
    pos_score = 'Positive Score'
    neg_score = 'Negative Score'
    net_score = 'Net Score'
    header = "{retweet_count}, {reply_count}, {pos_score}, {neg_score}, {net_score}".format(retweet_count=retweet_count, 
                                                                                              reply_count=reply_count, 
                                                                                              pos_score=pos_score, 
                                                                                              neg_score=neg_score, 
                                                                                              net_score=net_score)
    res_file.write("{header}\n".format(header=header))
    #iterate through the d_tweets
    for tweet in d_tweets:
        #create an empty list that will contain the csv col values
        csv_cols = []
        # acces the value(dict) associated with the tweet and assign it to tweet scores
        tweet_scores = d_tweets[tweet]
        # iterate through tweet_scores and append its values to a list.
        for tweet_score in tweet_scores:
            csv_cols.append(tweet_scores[tweet_score])
        
        #create a string containing the csv format and assign it to the variable line    
        #tweet_txt = 'tweet_txt'
        retweet_count = csv_cols[0]
        reply_count = csv_cols[1]
        pos_score = csv_cols[2]
        neg_score = csv_cols[3]
        net_score = csv_cols[4]

        line = "{retweet_count}, {reply_count}, {pos_score}, {neg_score}, {net_score}".format(retweet_count=retweet_count, 
                                                                                                  reply_count=reply_count, 
                                                                                                  pos_score=pos_score, 
                                                                                                  neg_score=neg_score, 
                                                                                                  net_score=net_score)
        #write the line into the file
        res_file.write("{line}\n".format(line=line))

