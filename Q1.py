# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 22:21:35 2016

@author: Rakshu
"""
import re

#path = 'C:/Users/Rakshu/Desktop/NLP/ferguson_train.txt'
path = input('Enter path: \n')
f = open(path)

'''
20 most frequent URLs
'''
urls_dict = {}
hashTags_dict = {}
userMentions_dict = {}
for line in f:
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
    hashTags = re.findall(r"#(\w+)", line)
    userTags = re.findall(r"@(\w+)", line)
    for url in urls:
        if url in urls_dict.keys():
            urls_dict[url] = urls_dict.get(url) + 1
        else:
		urls_dict[url] = 1
    for tag in hashTags:
        if tag in hashTags_dict.keys():
            hashTags_dict[tag] = hashTags_dict.get(tag) + 1
        else:
		hashTags_dict[tag] = 1
    for tag2 in userTags:
        if tag2 in userMentions_dict.keys():
            userMentions_dict[tag2] = userMentions_dict.get(tag2) + 1
        else:
		userMentions_dict[tag2] = 1
  
def top20(tag_dict):
    cnt =0
    for tag in sorted(tag_dict, key=tag_dict.get, reverse=True):
        if cnt<20:
            print tag, "", tag_dict[tag]
        else:
            break
        cnt = cnt+1
    
 
print "\n20 most frequent URLs:\n"
top20(urls_dict)
print "\n20 most frequent hashtags:\n"
top20(hashTags_dict)
print "\n20 most frequent user mentions:\n"
top20(userMentions_dict)


#cnt =0
#for url in sorted(urls_dict, key=urls_dict.get, reverse=True):
#    if cnt<20:
#        print url, "", urls_dict[url]
#    else:
#        break
#    cnt = cnt+1
#    
