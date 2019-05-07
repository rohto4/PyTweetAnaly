'''
Created on 2019/05/07

@author: Rohto
'''
from util.twitter_util import createTwitterSession, getTweetById #@UnresolvedImport

def main():
    twitter = createTwitterSession()
    res_text = getTweetById(twitter, '1125655406108217344')

if __name__ == '__main__':
    main()