"""
HTW FSR4 Discord Bot
~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2021-present FSR4
:license: MIT, see LICENSE for more details.
"""
import os

from discord import Client, Intents
from discord.utils import get

from components.roles import Roles
from logger import Logger

# Main instance of the Bots
# This class handles setting up all the components of the bot and notifies the components
# about events using a publisher-subscriber-structure
class Bot(Client):
    logger = None
    subscribers = set()
    
    def __init__(self, working_dir, **options):
        super().__init__(**options)
        self.logger = Logger(f"{working_dir}log.txt")
        self.setup_components()

    # Setup subcomponents
    def setup_components(self):
        Roles(self)

    # Publisher-Subscriber logic
    def register(self, who):
        self.subscribers.add(who)
    def unregister(self, who):
        self.subscribers.discard(who)
    async def emit(self, message, a = 0, b = 0, c = 0):
        for subscriber in self.subscribers:
            await subscriber.on_event(message, a, b, c)

    # Publish discord events to the publisher-subscriber-structure
    # async def on_ready(self):
    #     await self.emit("ready")
    # async def on_message(self, message):
    #     await self.emit("message", message)
    # async def on_reaction_add(self, reaction, user):
    #     await self.emit("reaction_add", reaction, user)
    async def on_raw_reaction_add(self, payload):
        await self.emit("raw_reaction_add", payload)
    async def on_raw_reaction_remove(self, payload):
        await self.emit("raw_reaction_remove", payload)

project_dir = os.path.dirname(__file__)
if len(project_dir) != 0:
    project_dir += "/"

with open(f"{project_dir}config/key.txt", "r") as file:
    key = file.read().replace("\n", "")

#Du darfst das!
intents = Intents.default()
intents.members = True
Bot(project_dir, intents=intents).run(key)
