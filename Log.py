from datetime import datetime

class Log():

    def __init__(self):
        pass


    @staticmethod
    def add(mensagem):
        name = datetime.now().strftime("%d-%m-%Y")
        hour = datetime.now().strftime("%H:%M:%S")
        filename = f"logs\log - {name}.txt"

        with open(f"{filename}", 'a', encoding="utf-8") as f:
            f.writelines(f"{hour} - {mensagem}\n")
    