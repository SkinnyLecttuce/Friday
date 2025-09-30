import ai_intent_recognizer

class Detector():
    def __init__(self):
        self.intent_model2 = ai_intent_recognizer.Recognizer()

    def Get_ready(self):
        intent_model_build2 = self.intent_model2.Model_exec('data/bot_social.txt', 'model_history/intent_detect2.h5')
        return intent_model_build2

    def Detect(self,intent_model_build2,inp):
        intent_str = self.intent_model2.Predict(intent_model_build2,inp)
        intent = self.intent_model2.Intent_to_str(intent_str,'Social')
        return [intent_str,intent]