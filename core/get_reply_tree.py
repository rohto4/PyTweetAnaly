'''
Created on 2019/05/07

@author: Rohto
'''
from util.twitter_util import createTwitterSession, getTweetById #@UnresolvedImport
from util.twitter_util import getStatusIdByUrl, getAndShowTweet #@UnresolvedImport

def main():
    twitter = createTwitterSession()
    url = input()
    
    getAndShowTweet(twitter, url)
    
if __name__ == '__main__':
    main()