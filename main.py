import ai_detect_tasks
import ai_detect_social
import ai_detect_task_social
import ai_entity_recognizer
import ai_seq2seq
import ai_speaker
import ai_nlp
import ai_sync_settings

class Friday_ai():
    def __init__(self):
        self.sync = ai_sync_settings.Syncer()
        self.nlp = ai_nlp.NLP()
        self.task = ai_detect_tasks.Detector()
        self.social = ai_detect_social.Detector()
        self.task_social = ai_detect_task_social.Detector()
        self.entity_model = ai_entity_recognizer.Recognizer()
        self.responser = ai_speaker.Speaker('female')

    def Get_ready(self):
        response6 = ai_seq2seq.Seq2Seq()
        response6.define_data_path("data/bot_social_q.txt", "data/bot_social_a.txt")
        response6.train('model_history/response6_model.h5')
        response6.load_model('model_history/response6_model.h5')

        response7 = ai_seq2seq.Seq2Seq()
        response7.define_data_path("data/bot_romantic_q.txt", "data/bot_romantic_a.txt")
        response7.train('model_history/response7_model.h5')
        response7.load_model('model_history/response7_model.h5')

        response0 = ai_seq2seq.Seq2Seq()
        response0.define_data_path("data/bot_book_flight_q.txt", "data/bot_book_flight_a.txt")
        response0.train('model_history/response0_model.h5')
        response0.load_model('model_history/response0_model.h5')

        response1 = ai_seq2seq.Seq2Seq()
        response1.define_data_path("data/bot_rate_book_q.txt", "data/bot_rate_book_a.txt")
        response1.train('model_history/response1_model.h5')
        response1.load_model('model_history/response1_model.h5')

        response2 = ai_seq2seq.Seq2Seq()
        response2.define_data_path("data/bot_play_music_q.txt", "data/bot_play_music_a.txt")
        response2.train('model_history/response2_model.h5')
        response2.load_model('model_history/response2_model.h5')

        response3 = ai_seq2seq.Seq2Seq()
        response3.define_data_path("data/bot_book_hotel_q.txt", "data/bot_book_hotel_a.txt")
        response3.train('model_history/response3_model.h5')
        response3.load_model('model_history/response3_model.h5')

        response4 = ai_seq2seq.Seq2Seq()
        response4.define_data_path("data/bot_launch_app_q.txt", "data/bot_launch_app_a.txt")
        response4.train('model_history/response4_model.h5')
        response4.load_model('model_history/response4_model.h5')

        response5 = ai_seq2seq.Seq2Seq()
        response5.define_data_path("data/bot_search_q.txt", "data/bot_search_a.txt")
        response5.train('model_history/response5_model.h5')
        response5.load_model('model_history/response5_model.h5')


        intent_model_build3 = self.task_social.Get_ready()

        intent_model_build2 = self.social.Get_ready()

        intent_model_build = self.task.Get_ready()

        return [intent_model_build,[response0,response1,response2,response3,response4,response5],[response6,response7],intent_model_build2,intent_model_build3]

    def Execute(self,inp,intent_model_build,task_responser_build_model,social_responser_build_model,intent_model_build2,intent_model_build3):
        self.sync.sync_refresh()
        intent_str = 0
        intent_str_pos = 0
        response_plus_entity = ''
        print("Modal:",intent_model_build3)
        intent_task_or_social_str = self.task_social.Detect(intent_model_build3[0],inp)

        if(intent_task_or_social_str[0] == 1):
            print('Social')
            intent_d = self.social.Detect(intent_model_build2[0],inp)
            intent_str = intent_d[0]
            intent = intent_d[1]
            print(intent)
            intent_str_pos = intent_str-1

            response = social_responser_build_model[intent_str_pos].generate(inp)
            #self.responser.Speak(response)
            response_text = []
            wc = ''
            i = 0
            response_text = response.split(' ')
            print('split:', response_text)
            response_text.remove(response_text[0])
            print('reemo', response_text)

            for w in response_text:
                print('w', w)
                if (i == 0):
                    wc = wc + w.capitalize() + ' '
                else:
                    wc = wc + w + ' '
                i = i + 1
            response = wc
            print("Response_Text:", response, response_text, wc)

            response_plus_entity = response

        elif(intent_task_or_social_str[0] == 2):
            print('Task')
            intent_d = self.task.Detect(intent_model_build[0], inp)
            intent_str = intent_d[0]
            intent = intent_d[1]
            print(intent)
            intent_str_pos = intent_str-1

            entity = self.entity_model.Entities(inp)
            entity = self.entity_model.Extraction(entity[0],entity[1],intent,self.task,intent_model_build2[0])

            response = task_responser_build_model[intent_str_pos].generate(inp)

            response_text = []
            wc=''
            i = 0
            response_text=response.split(' ')
            print('split:',response_text)
            response_text.remove(response_text[0])
            print('reemo',response_text)

            for w in response_text:
                print('w',w)
                if(i == 0):
                    wc = wc+w.capitalize()+' '
                else:
                    wc=wc+w+' '
                i=i+1
            response=wc
            print("Response_Text:",response,response_text,wc)
            if('Error' in str(entity)):
                print(entity)

            else:
                pass
                #self.responser.Speak(entity)

            #self.responser.Speak(response)
            response_plus_entity = response+' :'+str(entity)

            response_plus_entity = response_plus_entity

        print("resdedd:",response_plus_entity,response_plus_entity)
        response_plus_entity = response_plus_entity
        '''
        print('Task')
        intent_str = self.intent_model.Predict(intent_model_build[0], inp)
        intent = self.intent_model.Intent_to_str(intent_str, 'Task')
        print(intent)
        intent_str_pos = intent_str - 1

        entity = self.entity_model.Entities(inp)
        entity = self.entity_model.Extraction(entity[0], entity[1], intent, self.intent_model2, intent_model_build2)

        response = task_responser_build_model[intent_str_pos].generate(inp)

        if ('Error' in str(entity)):
            print(entity)

        else:
            pass
            # self.responser.Speak(entity)

        # self.responser.Speak(response)
        response_plus_entity = str(response) + ' :' + str(entity)

        response_plus_entity = str(response_plus_entity)

        response_plus_entity = response_plus_entity.capitalize()
        '''
        return response_plus_entity


bot = Friday_ai()
nlps = ai_nlp.NLP()
#trained = bot.Get_ready()
def Start_hosting(inp):
    text = str(inp)
    #learn: text:hello text:i am good text:[1]

    if("learn:" in inp):
        i = 0
        data = {0:'',1:'',2:''}
        f1 = open('data/bot_social_q.txt','+a')
        f2 = open('data/bot_social_a.txt','+a')
        f3 = open('data/bot_task_social.txt','+a')
        inp.split("learn:")
        print(inp)
        for s in inp:
            extract = s[1].split("text:")
            for ext in extract:
                data[i] = ext
                i = i+1
        f1.writelines(data[0]+'\n')
        f2.writelines(data[1]+'\n')
        f3.writelines(data[0]+' +++$+++ '+data[2]+'\n')
        f1.close()
        f2.close()
        f3.close()
        return "Doe"

    while(True):
        bot_reply = bot.Execute(inp,trained[0],trained[1],trained[2],trained[3],trained[4])
        print("Friday Response <-",bot_reply)
        return bot_reply

'''

def Start_hosting_terminal():
    bot = Friday_ai()
    nlps = ai_nlp.NLP()
    trained = bot.Get_ready()
    while (True):
        inp = input('Send ->')
        bot_reply = bot.Execute(inp, trained[0], trained[1], trained[2], trained[3], trained[4])
        print("Friday Response <-", bot_reply)
Start_hosting_terminal()
'''
