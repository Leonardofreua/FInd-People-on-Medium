#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import requests
import click
import csv
#from datatime import datatime, timedelta
#from time import sleep

MEDIUM_URL = 'https://medium.com'

#https://github.com/Radu-Raicea/Interesting-People-On-Medium/blob/master/finder.py

"""
    Remove the extra caracters that get returned with every JSON request on Medium endpoints
    Parameters:    
        - @response: str
            
"""
def clean_json_response(response):
    return json.loads(response.text.split('])}while(1);</x>')[1])

"""
    Returns the User ID of a Medium Username
    Parameters:
        - @username: str
"""
def get_user_id(username):
    print('Retrieving user ID...\n')
    
    url           = MEDIUM_URL + '/@' + username + '?format=json'
    response      = requests.get(url)
    response_dict = clean_json_response(response)
        
    return response_dict['payload']['user']['userId']

"""
    Returns the list of Username from a user's Followings list
    Parameters:
        - @user_id: str
"""
def get_list_of_followings(user_id):
    print('\nRetrieving uesrs from Followings...\n')
    
    next_id = False
    followings = []
    
    while True:
        
        if next_id:
            # If this is not the first page of the followings list
            url = MEDIUM_URL + '/_/api/users/' + user_id + '/following?limit=8&to=' + next_id
        else:
            # If this is the first page of the followings list
            url = MEDIUM_URL + '/_/api/users/' + user_id + '/following'
        
        response      = requests.get(url)
        response_dict = clean_json_response(response)
         
        for user in response_dict['payload']['value']:
            followings.append(user['username'])
        
        try:
            # If the "to" key is missing, we've reached the end of the list and an exception is thrown
            next_id = response_dict['payload']['paging']['next']['to']
        except:
            break
         
    return followings
 
"""
    Returns the list of IDs of the latest posts of a list of users
    Parameters:
        - @usernames: str
"""
def get_list_of_latest_posts_ids(usernames):
    print('\nRetrieving the latest posts...\n')
    
    post_ids = []
    
    for username in usernames:
        url            = MEDIUM_URL + '/@' + username + '/latest?format=json'
        response       = requests.get(url)
        response_dict  = clean_json_response(response)
        
        try:
            posts = response_dict['payload']['references']['Post']
        except:
            posts = []

        if posts:
            for key in posts.keys():
                post_ids.append(posts[key]['id'])
    
    return post_ids

if __name__ == '__main__':
    print(get_user_id('lfreua'))
    print(get_list_of_followings('da4389418289'))
    print(get_list_of_latest_posts_ids('lfreua'))