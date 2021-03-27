from discord import Client
from discord.utils import get

class Logger:
    log_file = None
    parent = None

    def __init__(self, log_path, parent):
        self.log_file = open(log_path, "a", encoding="utf-8")
        self.parent = parent

    def log(self, label, message):
        #channel = #support of Fachschaft 4
        channel = Client.get_channel(self ,825376458276339713)
        message = f"[{label}] {message}"
        
        #send message to channel logfile and console
        await channel.send(f"{message}\n")
        self.log_file.write(f"{message}\n")
        self.log_file.flush()
        print(message)

    def info(self, message):
        self.log("Info", message)

    def error(self, message):
        self.log("Error", message)
