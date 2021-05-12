import sys
import os
import requests


login_url = "http://127.0.0.1:8000/login/"
test_url = "http://127.0.0.1:8000/teste/"

client = requests.session()

# Retrieve the CSRF token first
client.get(login_url)  # sets cookie
if 'csrftoken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrftoken']
else:
    # older versions
    csrftoken = client.cookies['csrf']

data = dict(username="andre.aragao", password="Dufwine#1003", csrfmiddlewaretoken=csrftoken, next='/')
r = client.post(login_url, data=data, headers=dict(Referer=login_url))

client.get(login_url)  # sets cookie
if 'csrftoken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrftoken']
else:
    # older versions
    csrftoken = client.cookies['csrf']

data = dict(
    role="Scrum Master",
    hits=10,
    mistakes=4,
    individual_feedback="Errou demais",
    decision="Daily Scrum",
    concept="Reunião de Equipe",
    is_mistake=False,
    csrfmiddlewaretoken=csrftoken,
    next='/')

r = client.post(test_url, data=data, headers=dict(Referer=test_url))

print(f'{r.status_code}')
# path = os.getcwd()
# os.chdir('Assets/Data/')
# path = os.getcwd()

# file = open("score.txt", "w")  
# if r.status_code == 200:
#     r = client.get(data_url)
#     string = '{\"hits\": ' + str(r.json()['hits']) + ', \"mistakes\": ' + str(r.json()['mistakes']) + '}'
#     r = client.get(logout_url)

# else:
#     string = 'Credenciais incorretas'

# file.write(string)
# file.close()