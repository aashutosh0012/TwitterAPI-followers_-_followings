'''
#--------------------------------------------------------------------------------------------------------------------------------------------
twitter_Followers.py
Script to Fetch Twitter users Followers & Followings
Save output file "username_TwitterFollowers.xlsx" to directory from where script executed.


#----------------------------------------------------
'''

import requests,json,os,pandas as pd
#bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = 'AAAAAAAAAAAAAAAAAAAAANEJHQEAAAAAPaq8LhjeM%2F45PEEWJ7zXeXPtVuQ%3DEZ9WksWUryqwPAQKxqhWWeyLqIEn8IHEpSWUYKyXUBOGAhD2oa'
headers = {
     'Authorization': 'Bearer {}'.format(bearer_token)    
}

#----------------------------------------------------------------------------------------------------------------------------------------------   
def get_user_id(user_name):
    '''
    Fucntion Get User_id from user_name
    '''
    global user, user_id
    params = {
        "usernames": user_name,
        "user.fields": 'id,username,name,created_at,description',
    }
    get_user_id_url='https://api.twitter.com/2/users/by'
    response = requests.request(
        "GET",
        get_user_id_url,
        headers=headers,
        params=params
        )
    response.text
    result = json.loads(response.text)
    user = result['data'][0]
    #user_id = user['data'][0]['id']
    return user

get_user_id('aashutosh0012')
 
#----------------------------------------------------------------------------------------------------------------------------------------------
def get_following_list(user_name):
    '''
    Function to return list of accounts followed by the User.
    '''    
    #Fetch user details 
    user = get_user_id(user_name)
    user_id = user['id']
    global following
    following = []
    get_following_url = f'https://api.twitter.com/2/users/{user_id}/following'
    params = {
        'max_results': 1000,
    }    
    #loop through paginated result of "following" accounts list
    while True:
        response = requests.request(
            "GET",
            get_following_url,
            headers=headers,
            params = params
            )
        data = json.loads(response.text)
        following += data['data']
        try:
            next_token = data['meta']['next_token']
        except:
            next_token = 'Empty'
        
        if next_token == 'Empty':
            #break of loop when reached end of data.
            break
        else:
            #else, fetch next_token of paginated result and conutinue loop to fetch more results
            params = {
                'max_results': 1000,
                'pagination_token':next_token,
            }
    following = pd.DataFrame(following)
    print(f"\n\t\t{user['name']}(@{user['username']}) follows below ({len(following)}) Accounts")
    print("\t\t===========================================================")   
    print(following)
    #for friend in following:
    #    print('\t'+friend['name']+'(@'+friend['username']+')')
    #Save output to excel File
    with pd.ExcelWriter(file, engine='openpyxl', if_sheet_exists='replace', mode='a') as writer:
        following.to_excel(writer, sheet_name='Followings', index=False)



#----------------------------------------------------------------------------------------------------------------------------------------------
def get_followers_list(user_name):
    '''
    returns list of followers the User.
    '''    
    #Fetch user details 
    user = get_user_id(user_name)
    user_id = user['id']
    global followers
    followers = []
    get_followersList_url = f'https://api.twitter.com/2/users/{user_id}/followers'
    params = {
        'max_results': 1000,
    }    
    #loop through paginated result of "following" accounts list
    while True:
        response = requests.request(
            "GET",
            get_followersList_url,
            headers=headers,
            params = params
            )
        data = json.loads(response.text)
        followers += data['data']
        try:
            next_token = data['meta']['next_token']
        except:
            next_token = 'Empty'   
        if next_token == 'Empty':
            break
        else:
            params = {
                'max_results': 1000,
                'pagination_token':next_token,
            }
    followers = pd.DataFrame(followers)
    print(f"\n\t\t{user['name']}(@{user['username']}) is followed by below ({len(followers)}) Accounts")
    print("\t\t===========================================================")    
    print(followers)
    #for follower in followers:
    #    print('\t'+follower['name']+'(@'+follower['username']+')')    
    #Save output to excel File
    with pd.ExcelWriter(file, engine='openpyxl', if_sheet_exists='replace', mode='a') as writer:
        followers.to_excel(writer, sheet_name='Followers', index=False)

#----------------------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    username = input("\nEnter username to search:\t").strip('@')
    #username = 'aashutosh0012'
    file = f'{username}_TwitterFollowers.xlsx'
    get_followers_list(username)
    get_following_list(username)
    print(f'Output saved to "{file}"')
    input()