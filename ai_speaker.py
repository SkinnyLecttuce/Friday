import pyttsx3

class Speaker():
    def __init__(self,voice_type):
        self.engine = pyttsx3.init()
        male = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_MARK_11.0"
        female = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        if(voice_type == 'male'):
            self.engine.setProperty('voice',male)
        if(voice_type == 'female'):
            self.engine.setProperty('voice', female)

        self.engine.setProperty('volume', 5)
        self.engine.setProperty('rate',160)


    def Speak(self,text):
        self.engine.say(text)
        self.engine.runAndWait()