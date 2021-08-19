import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from paho.mqtt import publish
import time
import paho.mqtt.client as mqtt


def cria_audio(comando):
    
    tts = gTTS(comando, lang='pt-br')
    tts.save('./audios/comando.mp3')
    playsound('./audios/comando.mp3')
    
def on_message(client, userdata, message):
    
    time.sleep(1)
    print("received message =", str(message.payload.decode("utf-8")))
    
    
palavra_chave = 'rossi'
client = mqtt.Client()
client.connect('broker.mqttdashboard.com', 1883)
client.subscribe('rossi/temp', 2)
client.on_message = on_message
client.loop_start() #start loop to process received messages


def monitora_audio():
    
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        
        while True:
            
            print("ROSSI: Aguardando comandos...")
            audio = microfone.listen(source)
            
            trigger = microfone.recognize_google(audio, language='pt-BR')
            trigger = trigger.lower()
        
            if palavra_chave in trigger:
                
                print("COMANDO: " + trigger)
                playsound('./audios/javou.mp3')
                executa_comandos(trigger)
                break

    
def executa_comandos(trigger):
    
    if 'notícias' in trigger:
        ultimas_noticias()
    elif 'tempo' in trigger:
        previsao_tempo()
    elif 'ligar' in trigger or 'ligue' in trigger:
        client.publish('rossi/led', 'L')
    elif 'desativar' in trigger or 'desative' in trigger:
        client.publish('rossi/led', 'D')
    else:
        #playsound('./audios/')
        print('to afim nn')       
  
        
def ultimas_noticias():
    
    site = get('https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419')
    noticias = BeautifulSoup(site.text, 'html.parser')
    
    for item in noticias.findAll('item'):
        manchete = item.title.text
        cria_audio(manchete)
        break
 
def temperatura():
    pass
    # client.on_message = 
    # temp = client.subscribe('rossi/temp', 2)
    # print(temp)
   



def previsao_tempo():
    pass        

def cria_audio2(comando):
    
    tts = gTTS(comando, lang='pt-br')
    tts.save('./audios/javou.mp3')
    playsound('./audios/javou.mp3')
    
