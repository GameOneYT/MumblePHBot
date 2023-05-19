import re
from pornhub_api import PornhubApi
import pymumble_py3 as pymumble
from pymumble_py3.callbacks import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED as text_received
import requests
import base64
import time

api = PornhubApi() 
client = pymumble.Mumble("localhost", "PornHubBot", 64738)

client.start()

client.is_ready()

    
def message_received(message):
    raw_message = message.message.strip()
    if message.actor == 0:
        # Some server will send a welcome message to the bot once connected.
        # It doesn't have a valid "actor". Simply ignore it here.
        return
    
    if len(message.message) > 1 and message.message[:1] == "?":
        send_back(message, raw_message)
    
    
def send_back(message, raw_message):
    message.message = re.sub(r'<.*?>', '', raw_message[1:])

    
    user = client.users[message.actor]['name']
    
    
    print("From mumble("+user+"): "+message.message)
    print("all: "+str(message))
    # Echo the message back to the chat
    client.users[message.actor].send_text_message("Searching for: " + str(message.message))
    
    
    # Search Pornhub for videos based on the message
    try:
        data = api.search.search(
            message.message,
            ordering="mostrelevant"#,
            # period="weekly"
        )
    except:
        client.users[message.actor].send_text_message(str("Error to find video"))
        return

    # Send a list of video titles and links to the chat server
    msg_tg = ""
    videos = data.videos[:3] #3 is how many video send to the mumble
    for vid in videos:
        print(vid.title, " --- ", vid.url)
        
        
        
        
        # Download the thumbnail image for the video
        image_data = requests.get(vid.thumb).content

        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        msg_tg += str('<br /><a href="' + vid.url + '">')
        msg_tg += f'<img src="data:image/jpeg;base64,{image_b64}"/><span style="color:#39a5dd">'
        msg_tg += vid.title+"</span></a><br />"
        #client.channels.find_by_name(client.my_channel()["name"]).send_text_message(str(msg_tg))
        client.users[message.actor].send_text_message(str(msg_tg))
        # client.users[message.actor].send_text_message(str("ты лох я не шучу"))
        msg_tg = ""
    print("\n\n")
                    
        
while True:        
    client.callbacks.set_callback(text_received, message_received)
    time.sleep(10)
