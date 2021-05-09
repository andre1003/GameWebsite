import sys
import os
import requests


login_url = "http://127.0.0.1:8000/login/"
data_url = "http://127.0.0.1:8000/data/"
logout_url = "http://127.0.0.1:8000/logout/"

client = requests.session()

# Retrieve the CSRF token first
client.get(login_url)  # sets cookie
if 'csrftoken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrftoken']
else:
    # older versions
    csrftoken = client.cookies['csrf']

data = dict(username=str(sys.argv[1]), password=sys.argv[2], csrfmiddlewaretoken=csrftoken, next='/')
r = client.post(login_url, data=data, headers=dict(Referer=login_url))

path = os.getcwd()
os.chdir('Assets/Data/')
path = os.getcwd()

file = open("score.txt", "w")  
if r.status_code == 200:
    r = client.get(data_url)
    string = '{\"hits\": ' + str(r.json()['hits']) + ', \"mistakes\": ' + str(r.json()['mistakes']) + '}'
    r = client.get(logout_url)

else:
    string = 'Credenciais incorretas'

file.write(string)
file.close()