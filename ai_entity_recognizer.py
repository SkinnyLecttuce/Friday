import spacy
import ai_system
import ai_sync_settings
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import os

class Recognizer():
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.system = ai_system.System()
        self.sync = ai_sync_settings.Syncer()

    def Extraction(self,keys,ids,intent,intent_model_build2,intent_model):
        print("INTENT:",intent)
        r = 0
        formats = True

        task_tree = {'Book_Flight':{'formats':[],'entity':{'GPE':'None','ORG':'None','DATE':'','WORK_OF_ART':'None','TIME':'None'},'action':'system.book.flight'},'Rate_Book':{'formats':'','entity':{'WORK_OF_ART':'None','CARDINAL':'None','NNP':'None'},'action':'system.rate.book'},'Play_Music':{'formats':[".mp3", ".wav", ".mp4","."],'entity':{'WORK_OF_ART':'None'},'action':'system.play'},'Book_Hotel':{'formats':[],'entity':{'ORG':'None','WORK_OF_ART':'None','NNP':'None','NNS':'None','NN':'None'},'action':'system.book.hotel'},'Launch_App':{'formats':['.exe','.wav','.mp3','.mp4','.','C:','.lnk','.'],'entity':{},'action':'system.open'},'What_If':{'formats':[],'entity':{},'action':'system.browser'}}

        text = self.sync.sync_read_input()

        for id in ids:
            for task_ents in task_tree[intent]['entity']:
                if(keys[id] == task_ents):
                    task_tree[intent]['entity'][task_ents] = id

        for id in ids:
            if(len(task_tree[intent]['formats']) == 0):
                print(task_tree[intent]['action'])
                r=self.system.Execute(task_tree[intent]['action'],task_tree[intent]['entity'],text,intent_model,intent_model_build2)
                self.sync.sync_output(r)
                return r
            else:
                for task_formats in task_tree[intent]['formats']:
                    print(task_formats,id)
                    formats = False
                    if(task_formats in id):
                        print("Task_found_format",id,task_formats)
                        id = id.split(task_formats)
                        print(task_tree[intent]['action'],id)
                        r=self.system.Execute(task_tree[intent]['action'], task_tree[intent]['entity'], id,intent_model,intent_model_build2)
                        self.sync.sync_output(r)
                        formats = True
                        break
            print(task_tree[intent], keys, ids)

        if(formats == True):
            return r
        else:
            print("No task formats")
            id = ['-']
            r = self.system.Execute(task_tree[intent]['action'], task_tree[intent]['entity'], id, intent_model, intent_model_build2)
            self.sync.sync_output(r)
            return r



    def Entities(self,text):
        res = {}
        self.sync.sync_input(text)
        words = text
        print(self.nlp(words))
        ent_rec = self.nlp(words).ents
        for ww in ent_rec:
            res[ww.text] = ww.label_

        w = word_tokenize(words)
        pos = pos_tag(w)
        res2 = {}
        words2 = []
        ig = 0
        breakable = False
        for p in pos:
            for things in res:
                if (p[0] in things):
                    res2[things] = res[things]
                    breakable = True
                    if(things in words2):
                        pass
                    else:
                        words2.append(things)
                    break

                else:
                    pass
            if (breakable == False):
                res2[p[0]] = p[1]
                if(p[0] in words2):
                    pass
                else:
                    words2.append(p[0])
            breakable = False

        return [res2,words2]

'''
e= Recognizer()
ee = e.Entities('What is the goood ?')
print("Entity:",ee[0],ee[1])
r=e.Extraction(ee[0],ee[1],"What_If")
print(r)
'''