import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
from requests import get
from bs4 import BeautifulSoup
from paho.mqtt import publish


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



def cria_audio(comando):
    
    tts = gTTS(comando, lang='pt-br')
    tts.save('./audios/comando.mp3')
    playsound('./audios/comando.mp3')
    
    
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


def publica_mqtt(topic, payload):
    publish.single(topic, payload=payload, qos=1, retain=True, hostname='vo ve ainda', port='numsei', client_id='rossi', auth={'username': '', 'password': ''})


def main():
    monitora_audio()    


main()