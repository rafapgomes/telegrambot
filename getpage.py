import requests

headers = { 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)'}
cookies = {'sessionid':'2113549053%3ABmcfoaxek5Sg7A%3A29'}

def request(url):  

    response = requests.get(url,headers=headers,cookies=cookies)
    return response.content

