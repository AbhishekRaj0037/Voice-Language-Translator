from googletrans import Translator
import speech_recognition as sr 
import sounddevice as sd
from gtts import gTTS
import wavio as wv
import pygame
import sys
import os

freq=44100
duration=5

translator = Translator()
r = sr.Recognizer()

recorded_audio_as_text=None

# A tuple containing all the language and 
# codes of the language will be detcted 
dic = ('afrikaans', 'af', 'albanian', 'sq',  
       'amharic', 'am', 'arabic', 'ar', 
       'armenian', 'hy', 'azerbaijani', 'az',  
       'basque', 'eu', 'belarusian', 'be', 
       'bengali', 'bn', 'bosnian', 'bs', 'bulgarian', 
       'bg', 'catalan', 'ca', 'cebuano', 
       'ceb', 'chichewa', 'ny', 'chinese (simplified)', 
       'zh-cn', 'chinese (traditional)', 
       'zh-tw', 'corsican', 'co', 'croatian', 'hr', 
       'czech', 'cs', 'danish', 'da', 'dutch', 
       'nl', 'english', 'en', 'esperanto', 'eo',  
       'estonian', 'et', 'filipino', 'tl', 'finnish', 
       'fi', 'french', 'fr', 'frisian', 'fy', 'galician', 
       'gl', 'georgian', 'ka', 'german', 
       'de', 'greek', 'el', 'gujarati', 'gu', 
       'haitian creole', 'ht', 'hausa', 'ha', 
       'hawaiian', 'haw', 'hebrew', 'he', 'hindi', 
       'hi', 'hmong', 'hmn', 'hungarian', 
       'hu', 'icelandic', 'is', 'igbo', 'ig', 'indonesian',  
       'id', 'irish', 'ga', 'italian', 
       'it', 'japanese', 'ja', 'javanese', 'jw', 
       'kannada', 'kn', 'kazakh', 'kk', 'khmer', 
       'km', 'korean', 'ko', 'kurdish (kurmanji)',  
       'ku', 'kyrgyz', 'ky', 'lao', 'lo', 
       'latin', 'la', 'latvian', 'lv', 'lithuanian', 
       'lt', 'luxembourgish', 'lb', 
       'macedonian', 'mk', 'malagasy', 'mg', 'malay', 
       'ms', 'malayalam', 'ml', 'maltese', 
       'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian', 
       'mn', 'myanmar (burmese)', 'my', 
       'nepali', 'ne', 'norwegian', 'no', 'odia', 'or', 
       'pashto', 'ps', 'persian', 'fa', 
       'polish', 'pl', 'portuguese', 'pt', 'punjabi',  
       'pa', 'romanian', 'ro', 'russian', 
       'ru', 'samoan', 'sm', 'scots gaelic', 'gd', 
       'serbian', 'sr', 'sesotho', 'st', 
       'shona', 'sn', 'sindhi', 'sd', 'sinhala', 'si', 
       'slovak', 'sk', 'slovenian', 'sl', 
       'somali', 'so', 'spanish', 'es', 'sundanese', 
       'su', 'swahili', 'sw', 'swedish', 
       'sv', 'tajik', 'tg', 'tamil', 'ta', 'telugu', 
       'te', 'thai', 'th', 'turkish', 
       'tr', 'ukrainian', 'uk', 'urdu', 'ur', 'uyghur', 
       'ug', 'uzbek',  'uz', 
       'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh', 
       'yiddish', 'yi', 'yoruba', 
       'yo', 'zulu', 'zu') 

def takecommand():
    try:
        recording = sd.rec(int(duration * freq), 
                        samplerate=freq, channels=2)
        print("Recording audio...")
        sd.wait()
        print("Saving recording...")
        wv.write("recorded_voice.wav",recording,freq,sampwidth=2)
        recorded_file=sr.AudioFile("recorded_voice.wav")
        with recorded_file as source:
            audio=r.record(source)
        recorded_audio_as_text=r.recognize_google(audio)
        return recorded_audio_as_text.lower()
    except:
        print("Some error occurred")
        sys.exit()


def destination_language(): 
    print("Please speak language in which you want to convert your voice to : Ex. Hindi , English , etc.") 
    print() 
    to_lang = takecommand() 
    while (to_lang == "None" or (to_lang not in dic)):
        to_lang = takecommand() 

    to_lang =  dic[dic.index(to_lang)+1]
    return to_lang 

def play_translated_audio(translated_text,to_lanuage):
    myobj = gTTS(text=translated_text, lang=to_lanuage, slow=False)
    myobj.save("Converted_audio.mp3")
    # Initialize the mixer module
    pygame.mixer.init()
    pygame.time.delay(100)

    # Load the mp3 file
    pygame.mixer.music.load("Converted_audio.mp3")

    # Play the loaded mp3 file
    print("Playing...")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # Check if audio is playing
        pygame.time.Clock().tick(10)  # Check every 100ms
    
if __name__=="__main__":
    print("Speak to translate into another language")
    recorded_audio_as_text=takecommand()
    to_lanuage=destination_language()
    translated = translator.translate(recorded_audio_as_text, dest=to_lanuage).text
    play_translated_audio(translated,to_lanuage)

