import json

from chalice import Chalice

from chalicelib import webexteams

app = Chalice(app_name='whois_bot')


bot_email = 'whois_bot@webex.bot'

@app.route('/')
def hello():
    return "Hi, this is working"

@app.route('/browsertest/{tech}')
def browser(tech):
    name = webexteams.lookup(tech)
    return "{name} is responsible for {tech}".format(name=name, tech=tech)

@app.route('/test', methods=['POST'])
def index():
    # Get the POST data sent from Webex Teams
    json_data = app.current_request.json_body

    # Get the room details
    roomId = json_data['data']['roomId']
    # Get the message details
    messageId = json_data['data']['id']
    
    # make sure it isn't yourself, dumb bot!
    if json_data['data']['personEmail'] != bot_email:
        if 'cisco.com' in json_data['data']['personEmail']:
            webexteams.ask(roomId, messageId)
        else:
            webexteams.sorry(roomId)
