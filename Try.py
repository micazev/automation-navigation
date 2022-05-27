import time
from Log import Log

class Try():

    def __init__(self):
        pass


    @staticmethod
    def catch(item, mensagem = ""):
        for p in range(0,5):
            try:
                Log.add(mensagem)
                {item}
            except:
                time.sleep(2)
                Log.add('erro ao achar o elemento')
            break