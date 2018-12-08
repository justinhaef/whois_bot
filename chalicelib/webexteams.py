import os
from os import environ as env
import json

from webexteamssdk import WebexTeamsAPI

# Grab the needed Token
teamsToken = env.get('WEBEX_TEAMS_ACCESS_TOKEN')

# Create the connection
api = WebexTeamsAPI(access_token=teamsToken)

# Pull in the list of who is the expert of what tech.
filename = os.path.join(
    os.path.dirname(__file__), 'whois.json')
with open(filename) as f:
    whois = json.load(f)

def lookup(tech):
    ''' Using the technology as the key, return the name associated
        with that technology from the static file. 
    '''
    name = whois[tech]
    return name

def sorry(roomId):
    ''' Return to the user that only Cisco Employees are allowed '''
    api.messages.create(roomId=roomId, text="Sorry but this bot is only for Cisco Employees!")

def ask(roomId, messageId):
    ''' Get the room to respond too, as well as the tech in question, 
        then reply to that room with the answer. 
    '''
    # Get the message info
    message = api.messages.get(messageId)

    # Create a List of the tech from the list
    techList = []
    # the make it into a list so it can be printed out
    for key in whois.keys():
        techList.append(key)
    
    # making the catagories a string
    keysString = ", ".join(techList)

    # main part of the bot's logic, first we'll catch if they are looking for the list
    if 'list' in message.text:
        api.messages.create(roomId=roomId, text="Here are all my technologies: {list}".format(list=keysString))
    
    # now we'll see if we can match the tech requested.
    elif message.text in techList:
        try:
            name = lookup(message.text)
            api.messages.create(roomId=roomId, text="{name} is responsible for {tech}".format(name=name, tech=message.text))
        except:
            api.messages.create(roomId=roomId, text="Sorry, I don't have {tech} in my list.".format(tech=message.text))
    else:
        api.messages.create(roomId=roomId, text="Sorry, I don't have {tech} in my list.".format(tech=message.text))