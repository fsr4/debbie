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
        message = f"[{label}] {message}"
        
        #send message to channel logfile and console
        self.log_file.write(f"{message}\n")
        self.log_file.flush()
        print(message)

    def info(self, message):
        self.log("Info", message)

    def error(self, message):
        self.log("Error", message)

    async def notify(self, message):
        channel = self.parent.get_channel(820281018263142412)
        await channel.send(f"{message}\n")
