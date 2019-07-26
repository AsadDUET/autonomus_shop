import os
import os.path
import sys
import datetime
import time
from pygame import mixer
import label_image
import atm
from gtts import gTTS
import json
import apiai
import random
import VoiceUsingChrome
import mySqlite
import label_image
data=[0,0,0]
CLIENT_ACCESS_TOKEN = 'f8dc0f9ac21a445e95eb0ed6af888198'#Shop
#~ CLIENT_ACCESS_TOKEN = '67d03b977e32456d89d1e4e84613cac5'#bangla
#CLIENT_ACCESS_TOKEN = 'dde3d7f999434732a56d9887b7c43d09'#robot
#CLIENT_ACCESS_TOKEN = '332da3ed83324895993de3f7f7ca5f91'#asad
#CLIENT_ACCESS_TOKEN ='1a62a0de8e1a42bdb544334977437567 '#joke

mixer.init()
response_json =''
shoping_chart={'chocolate':0,'chips':0,'biscuit':0}
prize_list={'chocolate':10,'chips':20,'biscuit':10}

def dialog(text):
    global response_json
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    request.session_id = "<shop1>"
    request.query = text
    response = request.getresponse()
    a=str(response.read(), 'utf-8')
    response_json =json.loads(a)
    print(response_json)
    print(response_json['result']['metadata']['intentName'])
    return (response_json["result"]["fulfillment"]["messages"][0]["speech"])#["textToSpeech"])


def save_and_load_speech(text):

    try: # Load local
        a = datetime.datetime.now()
        mixer.music.load("sound/"+ text +".mp3")
        b = datetime.datetime.now()
        print("local load time: ",b-a)
    except: # load from gtts
        a = datetime.datetime.now()
        tts = gTTS(text= text , lang='bn')
        b = datetime.datetime.now()
        print("TTS time: ",b-a)

        try: # save with variable name
            a = datetime.datetime.now()
            tts.save("sound/"+ text +".mp3")
            b = datetime.datetime.now()
            print("Saveing time: ",b-a)
            a = datetime.datetime.now()
            mixer.music.load("sound/"+text+".mp3")
            b = datetime.datetime.now()
            print("load time: ",b-a)
        except:
            try: # save using test name
                a = datetime.datetime.now()
                tts.save("test.mp3")
                b = datetime.datetime.now()
                print("Saveing time: ",b-a)
                a = datetime.datetime.now()
                mixer.music.load("test.mp3")
                b = datetime.datetime.now()
                print("load time: ",b-a)
            except:
                print("can't save")

def take_action(intent):
    global shoping_chart , prize_list
    local_response=''
    if intent=="add_to_list":
        for i in range(len(response_json["result"]['parameters']['product'])):
            product_name = response_json["result"]['parameters']['product'][i]
            try:
                product_quantity = int(response_json["result"]['parameters']['my_number'][i])
            except:
                product_quantity = 0
            shoping_chart[product_name] = product_quantity
        local_response = 'আর কি লাগবে'
    if intent=="remove_from_list":
        for product_name in response_json["result"]['parameters']['product']:
            shoping_chart[product_name] = 0
            local_response = 'আর কি লাগবে'
    if intent=='buying_end':
        print('taka')
        total_bill=0
        taka_get=0
        for product in shoping_chart:
            total_bill=total_bill+(shoping_chart[product]*prize_list[product])
        save_and_load_speech('আপনার বিল  '+str(total_bill)+' টাকা দয়া করে পরিশোধ করুন')
        mixer.music.play()
        while(mixer.music.get_busy()):
            time.sleep(.1)
        mixer.music.load("test2.mp3")
        while (total_bill-taka_get)!=0:
            atm.take_taka()
            new_taka=label_image.start_process()
            if taka_get+new_taka<=total_bill:
                taka_get=taka_get+new_taka
                if taka_get==total_bill:
                    atm.reset()
                    break
                save_and_load_speech('আরও '+ str(total_bill-taka_get) +'  টাকা পরিশোধ করুন')
                mixer.music.play()
                while(mixer.music.get_busy()):
                    time.sleep(.1)
                mixer.music.load("test2.mp3")
                atm.reset()
            elif taka_get+new_taka>total_bill:
                save_and_load_speech('ভাংতি হবে না, আরও '+ str(total_bill-taka_get) +'  টাকা পরিশোধ করুন')
                mixer.music.play()
                while(mixer.music.get_busy()):
                    time.sleep(.1)
                mixer.music.load("test2.mp3")
                atm.back_taka()
            if taka_get==total_bill:
                break
        save_and_load_speech('আপনার মালামাল গ্রহন করুন')
        mixer.music.play()
        atm.give_chips(shoping_chart['chips'])
        atm.give_chocolate(shoping_chart['chocolate'])
        atm.supply()
        while(mixer.music.get_busy()):
            time.sleep(.1)
        mixer.music.load("test2.mp3")
        for product in shoping_chart:
            shoping_chart[product]=0
        local_response = 'ধন্যবাদ, আবার আসবেন'
    if intent=='my_chart':
        for product in shoping_chart:
            if shoping_chart[product]>0:
                local_response=local_response + str(str(product) + ' '+ str(shoping_chart[product]) + 'টা ')
        local_response=local_response + ' আর কি লাগবে'
    if intent=='calculate':
        total=0
        for product in shoping_chart:
            total=total+shoping_chart[product]*prize_list[product]
        local_response=str('আপনার '+str(total)+' টাকা বিল হয়েছে, আর কি লাগবে')
    if intent=='prize':
        product_name = response_json["result"]['parameters']['product'][0]
        local_response= str(product_name) +' '+ str(prize_list[product_name]) + ' টাকা, নিবেন নাকি'
    if intent=='prize - yes':
        for context in response_json['result']['contexts']:
            if context['name']=='prize-followup':
                shoping_chart[context['parameters']['product'][0]]=context['parameters']['my_number'][0]
        local_response = 'আর কিছু কি লাগবে'
    print(shoping_chart)
    return local_response
def conversation():
    while True:
        user_said=None
        while(mixer.music.get_busy()):
            time.sleep(.1)
        mixer.music.load("test2.mp3")
        while (user_said==None):
            user_said=VoiceUsingChrome.chrome_detect()
        print('\n\n')
        print(user_said)
        time.sleep(.2)
        try:
            a = datetime.datetime.now()
            dialogflow_response=dialog(user_said)
            b = datetime.datetime.now()
            print("dialogflow time: ",b-a)
            intent=response_json['result']['metadata']['intentName']
            save_and_load_speech(dialogflow_response)

            mixer.music.play()
            if not response_json["result"]['actionIncomplete']:
                local_response=take_action(intent)
                while(mixer.music.get_busy()):
                    time.sleep(.1)
                mixer.music.load("test2.mp3")
                if local_response!='':
                    save_and_load_speech(local_response)
                    mixer.music.play()
                    while(mixer.music.get_busy()):
                        time.sleep(.1)
                    mixer.music.load("test2.mp3")

            while(mixer.music.get_busy()):
                time.sleep(.1)
            mixer.music.load("test2.mp3")



            print("end")
        except KeyboardInterrupt:
            raise
        except:
            pass

if __name__== '__main__':
    while True:
        conversation()
