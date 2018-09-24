"""
Shows basic usage of the Gmail API.

Lists the user's Gmail labels.
"""
from apiclient import discovery
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import base64

import cfg
import socket
import re
import time
import multiprocessing


def chat(sock, msg):
    """
    Send a chat message to the server.
    Keyword arguments:
    sock -- the socket over which to send the message
    msg  -- the message to be sent
    """
    sock.send("PRIVMSG {} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))



s = socket.socket()
s.connect((cfg.HOST,cfg.PORT))
s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
s.send("JOIN {}\r\n".format(cfg.CHAN).encode("utf-8"))

CHAT_MSG=re.compile(r"^:\w+!\w+@\w+.tmi.twitch.tv PRIVMSG #\w+ :")



# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.modify' # we are using modify and not readonly, as we will be marking the messages Read
store = file.Storage('storage.json') 
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

user_id = 'me'
label_id_one = 'INBOX'
label_id_two = 'UNREAD'



#gets all of the unread messages from the inbox
def remail():
    t=0
    while True:
        ot=time.time()
        diff = ot - t
        
        unread_msgs = service.users().messages().list(userId='me',labelIds=[label_id_two]).execute()

    
        mess = unread_msgs['messages']
        final_list=[]
    
        #print ("Total messaged retrived: ", str(len(mess)))
        for msgs in mess:
            temp_dict = { }
            m_id = msgs['id']
            message = service.users().messages().get(userId=user_id, id=m_id).execute() #get message using api
            payId=message['payload']
            headr =payId['headers']
    
            for one in headr:
                if one['name'] == 'Subject':
                       msg_subject = one['value']
                       temp_dict['Subject']= msg_subject
                else:
                       pass
           
            for three in headr:
                    if three['name']=='From':
                       msg_from = three['value']
                       temp_dict['Sender']= msg_from
                    else:
                       pass
            
            #print(temp_dict['Sender']) #should always look like this for me natedamen <nate.damen@pb08.wixshoutout.com>
                
            if temp_dict['Subject'] == 'rnbw':
                chat(s,"!rainbowHeart")
                #print(temp_dict['Subject'])
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute() 

            elif temp_dict['Subject'] == 'gltchd':
                chat(s,"!flicker")
                #print(temp_dict['Subject'])
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute()

            elif temp_dict['Subject'] == 'fxdgltch':
                chat(s,"!flickerOff")
                #print(temp_dict['Subject'])
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute()

            elif temp_dict['Subject'] == 'hrt':
                chat(s,"!heartColor")
                #print(temp_dict['Subject'])
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute()

            elif temp_dict['Subject'] == 'bgclr':
                chat(s,"!backgroundColor")
                #print(temp_dict['Subject'])
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute()

            elif temp_dict['Subject'] == 'rst':
                chat(s,"!reset")
                #print(temp_dict['Subject'])
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute()

            elif temp_dict['Subject'] == 'ch1':
                chat(s,"<3")
                #print(temp_dict['Subject'])
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute()
            elif temp_dict['Subject'] == 'ch2':
                chat(s,"!mirrorMirror")
                #print(temp_dict['Subject'])
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute()
            elif temp_dict['Subject'] == 'frainbow':
                chat(s,"!fullRainbow")
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute()
            elif temp_dict['Subject'] == 'sparkles':
                chat(s,"!sparkles")
                service.users().messages().modify(userId=user_id, id=m_id, body={ 'removeLabelIds': ['UNREAD']}).execute()

            time.sleep(1 / cfg.RATE)
            
        if diff > 240:
            t=time.time()
            diff=0
            ot=time.time()
            chat(s,"Hey Chat! This is TvheadBot just letting you know a few commands: !rainbow     !ch1     !heart")
          
        #time.sleep(1 / cfg.RATE)     




def pingPong(): 
    while True:    
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            time.sleep(1 / cfg.RATE) 
            print('sent')
        print(response) 
        



if __name__ == '__main__' :
    p =  multiprocessing.Process(target=pingPong)
    m =  multiprocessing.Process(target=remail)
    m.start()
    print('Started Email Scanning')
    p.start()
    print('ping pong started')
    
