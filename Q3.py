# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 23:50:23 2016

@author: Rakshu
"""
import pandas as pd
import string
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from nltk import bigrams


path = input('Enter path: \n')
f = open(path)
text = f.read()
tweets = re.findall(r'(?<={)[^}]*',text)
labels = re.findall(r'}, (\w+)', text)

re.findall(r'(?<={)[^,]*','The video makes for a wonderful watch and will definitely bring a smile to your face. Take a look below: ,0.836')

#Preprocessing to reemove stop word, punctuations and converting to lower case
for j in range(0,2500):
    #remove punctuations and convert to lower case
    tweets[j] = ''.join([i.lower() for i in tweets[j] if i not in string.punctuation])
    #remove non-ascii characters 
    tweets[j] = ''.join(i for i in tweets[j] if ord(i)<128)
    #remove stopwords
    tweets[j] = ' '.join([word for word in tweets[j].split() if word not in (stopwords.words('english'))])
    
df = pd.DataFrame({'tweetText':tweets,
                   'Labels':labels})
                   
# Most frequent words    
all_words = set([word for line in tweets for word in word_tokenize(line)])
all_words_sorted = list(nltk.FreqDist(w for w in all_words))[:3000]


unigram_featureset = [({word: (word in set(line)) for word in all_words_sorted}, label) for index, (label,line) in df.iterrows()]
train, test = unigram_featureset[200:], unigram_featureset[:200]
classifier = nltk.NaiveBayesClassifier.train(train)

print 'Naive bayes classifier accuracy for Unigrams is: '
print(nltk.classify.accuracy(classifier, test))                 






