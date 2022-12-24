from pornhub_api import PornhubApi
import pymumble_py3 as pymumble
from pymumble_py3.callbacks import PYMUMBLE_CLBK_TEXTMESSAGERECEIVED as text_received
import requests
import base64

api = PornhubApi() 
client = pymumble.Mumble("localhost", "PornHubBot", 64738)

client.start()

client.is_ready()

    
    
def testt(message):
    # Echo the message back to the chat
    client.channels.find_by_name(client.my_channel()["name"]).send_text_message(str(message.message))
    print("From mumble:")
    print(message.message)
    
    # Search Pornhub for videos based on the message
    data = api.search.search(
        message.message,
        ordering="mostviewed",
        period="weekly"
    )

    # Send a list of video titles and links to the chat server
    msg_tg = ""
    videos = data.videos[:3] #3 is how many video send to the mumble
    for vid in videos:
        print(vid.title, vid.url)
        
        
        
        # Download the thumbnail image for the video
        image_data = requests.get(vid.thumb).content

        image_b64 = base64.b64encode(image_data).decode('utf-8')
        
        msg_tg += str('<br /><a href="' + vid.url + '">')
        msg_tg += f'<img src="data:image/jpeg;base64,{image_b64}"/><span style="color:#39a5dd">'
        msg_tg += vid.title+"</span></a><br />"
        client.channels.find_by_name(client.my_channel()["name"]).send_text_message(str(msg_tg))
        msg_tg = ""
    

                    
        
while True:        
    client.callbacks.set_callback(text_received, testt)
