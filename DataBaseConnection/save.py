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

    return r

def count(filename):
    file = open(filename, 'r')
    return len(file.readlines())



login_url = "http://127.0.0.1:8000/login/"
match_url = "http://127.0.0.1:8000/match-register/"
decision_url = "http://127.0.0.1:8000/decision-register/"

client = requests.session()

csrftoken = set_csrftoken(client)



#### Login
data = dict(username=sys.argv[1], password=sys.argv[2], csrfmiddlewaretoken=csrftoken, next='/')
r = client.post(login_url, data=data, headers=dict(Referer=login_url))

# I need to reset csrftoken because login redirects to home, ant csrftoken is cleared
csrftoken = set_csrftoken(client)



#### Saving Match

# Get match data
file = open("match.txt", "r")
content = file.readline()
file.close()

content = content.split(';')

# Getting the number of hits and mistakes
hits = count('hits.txt')
mistakes = count('mistakes.txt')

# Geting individual feedback
file = open('individual_feedback.txt', 'r')
feedback_lines = file.readlines()
file.close()

feedback = ''
for item in feedback_lines:
    feedback += item

feedback = feedback[:-1]

# Preparing data package
data = dict(
    role=content[1],
    hits=hits,
    mistakes=mistakes,
    individual_feedback=feedback,
    group=content[0],
    csrfmiddlewaretoken=csrftoken,
    next='/'
)

# Save match
r = save(client, data, match_url)

# Getting match id
match_id = r.json()['match_id']

# Preparing decision URL for saving the decisions
decision_url += match_id + "/"



#### Saving Decisions

# Open hits file
file = open('hits.txt', 'r')
content = file.readlines()
file.close()

for item in content:
    aux = item.split(';')

    data = dict(
        decision=aux[1].replace('\n', ''),
        scenery=aux[0],
        is_mistake=False,
        csrfmiddlewaretoken=csrftoken,
        next='/'
    )

    #print(data, end="\n\n")
    r = save(client, data, decision_url)

# Open mistakes file
file = open('mistakes.txt', 'r')
content = file.readlines()
file.close()

for item in content:
    aux = item.split(';')

    data = dict(
        decision=aux[1].replace('\n', ''),
        scenery=aux[0],
        is_mistake=True,
        csrfmiddlewaretoken=csrftoken,
        next='/'
    )

    #print(data, end="\n\n")
    r = save(client, data, decision_url)