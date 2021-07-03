import sys
import os
import requests

def set_csrftoken(client):
    client.get(login_url)  # sets cookie
    if 'csrftoken' in client.cookies:
        # Django 1.6 and up
        return client.cookies['csrftoken']
    else:
        # older versions
        return client.cookies['csrf']


def save(client, data, url):
    r = client.post(url, data=data, headers=dict(Referer=url))

    print(r.status_code)



login_url = "http://127.0.0.1:8000/login/"
match_url = "http://127.0.0.1:8000/match-register/"
decision_url = "http://127.0.0.1:8000/decision-register/"

client = requests.session()

csrftoken = set_csrftoken(client)

data = dict(username="andre.aragao", password="Dufwine#1003", csrfmiddlewaretoken=csrftoken, next='/')
r = client.post(login_url, data=data, headers=dict(Referer=login_url))

# I need to reset csrftoken because login redirects to home, ant csrftoken is cleared
csrftoken = set_csrftoken(client)

data = dict(
    role="Scrum Master",
    hits=6,
    mistakes=4,
    individual_feedback="Poucos erros.",
    group="Firma",
    csrfmiddlewaretoken=csrftoken,
    next='/')

r = client.post(match_url, data=data, headers=dict(Referer=match_url))

print(f'{r.status_code}')

match_id = r.json()['match_id']

decision_url += match_id + "/"


########### Save decision

data = dict(
    decision="Daily Scrum",
    scenery="Reunião de Equipe",
    is_mistake=False,
    csrfmiddlewaretoken=csrftoken,
    next='/'
)

save(client, data, decision_url)

data = dict(
    decision="Sprint Retrospective",
    scenery="Reunião de Equipe",
    is_mistake=True,
    csrfmiddlewaretoken=csrftoken,
    next='/'
)

save(client, data, decision_url)