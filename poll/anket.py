#Более 15 баллов – очень высокий риск алкогольной зависимости
#Разбалловка 1-0,2-1,3-2,4-3,5-4
class Anket:
    def __init__(self, config):
        self.config = config
        self.answers = None
        self.scores = 0  
        self.length = len(config)

    def add_answers(self, answers: list):
        self.scores = 0
        self.answers = answers
        self._counter()
        return self.scores
    def get_question(self,k):
      return self.config[k].get('text')
    def _counter(self):
        for i in range(self.length):
            qtype = self.config[i].get('type')
            qoptions =  self.config[i].get('options')
            right_answer =  self.config[i].get('right_answer')
            qanswer = self.answers[i]
            if qtype == 'closed':
                self.scores += 1 if qanswer == 'часто' else + 0
            elif qtype == 'multiple_choice':
                self.scores += right_answer.get(qanswer, 0)
            elif qtype == 'numbers':
                self.scores += str(qanswer)              

