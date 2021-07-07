import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from paho.mqtt import publish
import paho.mqtt.client as mqtt

def cria_audio(comando):
    
    tts = gTTS(comando, lang='pt-br')
    tts.save('./audios/comando.mp3')
    playsound('./audios/comando.mp3')
    
palavra_chave = 'rossi'

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
 

def previsao_tempo():
    pass        


def publica_mqtt():
    mqttc = mqtt.Client()
    mqttc.connect("iot.eclipse.org", 1883)
    mqttc.publish("rossi/status", '1')
    mqttc.loop(2)
    
    # publish.single(topic, payload=payload, qos=1, retain=True, hostname='85dd1517ad9c4248a66685c3f8fe2b51.s1.eu.hivemq.cloud', 
    #                port=8883, client_id='rossi', auth={'username': 'rossi', 'password': 'Rossi123'})