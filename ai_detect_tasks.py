import ai_intent_recognizer

class Detector():
    def __init__(self):
        self.intent_model = ai_intent_recognizer.Recognizer()

    def Get_ready(self):
        intent_model_build = self.intent_model.Model_exec('data/bot_questions.txt', 'model_history/intent_detect.h5')
        return intent_model_build

    def Detect(self,intent_model_build,inp):
        intent_str = self.intent_model.Predict(intent_model_build, inp)
        intent = self.intent_model.Intent_to_str(intent_str, 'Task')
        return [intent_str,intent]

