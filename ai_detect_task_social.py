import ai_intent_recognizer

class Detector():
    def __init__(self):
        self.intent_model3 = ai_intent_recognizer.Recognizer()

    def Get_ready(self):
        intent_model_build3 = self.intent_model3.Model_exec('data/bot_task_social.txt','model_history/intent_detect3.h5')
        return intent_model_build3

    def Detect(self,intent_model_build3,inp):
        intent_task_or_social_str = self.intent_model3.Predict(intent_model_build3, inp)
        intent = self.intent_model3.Intent_to_str(intent_task_or_social_str, 'Task_Social')
        return [intent_task_or_social_str,intent]