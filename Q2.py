
import re
import string
from nltk.corpus import stopwords
from nltk import bigrams, trigrams
import collections
import numpy as np

def bigramsReturn(arr):
    bigrams_arr = []
    for s in arr:
        bigrams_arr.extend(list(bigrams(s.split())))
    return bigrams_arr
    
def trigramsReturn(arr):
    trigrams_arr = []
    for s in arr:
        dummy = list(trigrams(s.split()))
        trigrams_arr.extend(dummy)
    return trigrams_arr

#path = 'C:/Users/Rakshu/Desktop/NLP/ferguson_train.txt'
path = input('Enter path: \n')
f = open(path)
text = f.read()
tweets = re.findall(r'(?<={)[^}]*',text)

#Preprocessing to remove stop word, punctuations and converting to lower case
for j in range(0,2500):
    #remove punctuations and convert to lower case
    tweets[j] = ''.join([i.lower() for i in tweets[j] if i not in string.punctuation])
    #remove non-ascii characters 
    tweets[j] = ''.join(i for i in tweets[j] if ord(i)<128)
    #remove stopwords
    tweets[j] = ' '.join([word for word in tweets[j].split() if word not in (stopwords.words('english'))])
  
bigrams_arr = bigramsReturn(tweets)
trigrams_arr = trigramsReturn(tweets)

# Frequencies
print "\n 20 most frequent bigrams: \n"
bigrams_cnt = dict(collections.Counter(bigrams_arr))
print collections.Counter(bigrams_arr).most_common(20)

print "\n 20 most frequent trigrams: \n"
trigrams_cnt = dict(collections.Counter(trigrams_arr))
print collections.Counter(trigrams_arr).most_common(20)

processed_tweets = ' '.join(i for i in tweets)
words_cnt = dict(collections.Counter(processed_tweets.split()))

# T-Score
def t_score(Bigram): # t_test 
    n_bigrams = len(bigrams_arr)
    w1, w2 = Bigram[0], Bigram[1]
    p_w1 = float(words_cnt[w1]) / n_bigrams
    p_w2 = float(words_cnt[w2]) / n_bigrams
    prob_bigram = float(bigrams_cnt[Bigram]) / n_bigrams
    var = prob_bigram
    t_statistic = (prob_bigram - (p_w1 * p_w2)) / (np.sqrt(var/n_bigrams)) 
    
    return t_statistic

def MI_score(Bigram):
    n_bigrams = len(bigrams_arr)
    w1, w2 = Bigram[0], Bigram[1]

    p_w1 = float(words_cnt[w1]) / n_bigrams
    p_w2 = float(words_cnt[w2]) / n_bigrams

    prob_bigram = float(bigrams_cnt[Bigram]) / n_bigrams
    return np.log2(prob_bigram/(p_w1 * p_w2))
    
def chi_score(Bigram):
    n_bigrams = len(bigrams_arr)
    w1, w2 = Bigram[0], Bigram[1]
    o11 = float(bigrams_cnt[Bigram]) # w1 and w2
    o12 = np.where(np.array(bigrams_arr)[:,1] == w2)[0].shape[0] - o11 # not w1 and w2 
    o21 = np.where(np.array(bigrams_arr)[:,0] == w1)[0].shape[0] - o11
    o22 = n_bigrams - o11 - o12 - o21
    chi_square = float(n_bigrams * (o11*o22 - o12*o21)**2) / ((o11+o12) * (o11+o21) * (o12+o22) * (o21+o22))
    
    return chi_square

def top20(tag_dict):
    cnt =0
    for tag in sorted(tag_dict, key=tag_dict.get, reverse=True):
        if cnt<20:
            print tag, "", tag_dict[tag]
        else:
            break
        cnt = cnt+1
        
# t, chi-squared and PMI scores
bigram_Tscore_dict = {}  
bigram_MIscore_dict = {}
bigram_chi_score_dict = {}    
for Bigram in set(bigrams_arr):
    bigram_Tscore_dict[Bigram] = t_score(Bigram)
    bigram_MIscore_dict[Bigram] = MI_score(Bigram)
    bigram_chi_score_dict[Bigram] = chi_score(Bigram)
print "\n 20 most collocating bigrams t-score: \n"
top20(bigram_Tscore_dict)
print "\n 20 most collocating bigrams MI-score \n"
top20(bigram_MIscore_dict)
print "\n 20 most collocating bigrams chi-score \n"
top20(bigram_chi_score_dict)


    
    
  