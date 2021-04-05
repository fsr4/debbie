"""
HTW FSR4 Discord Bot
~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2021-present FSR4
:license: MIT, see LICENSE for more details.
"""
import os

from discord import Client, Intents

from components.roles import Roles
from components.invites import Invites
from components.verify import Verify
from logger import Logger


# Main instance of the Bots
# This class handles setting up all the components of the bot and notifies the components
# about events using a publisher-subscriber-structure
class Bot(Client):
    logger = None
    subscribers = set()

    def __init__(self, working_dir, **options):
        super().__init__(**options)
        print("[Main (Bot)] Starting")
        self.logger = Logger(f"{working_dir}log.txt", self)
        self.setup_components(working_dir)
        print("[Main (Bot)] Started successfully")

    # Setup subcomponents
    def setup_components(self, working_dir):
        print("[Main (Bot)] Setting up components")
        Roles(self)
        Invites(self, working_dir)
        Verify(self)
        print("[Main (Bot)] All components set up")

    # Publisher-Subscriber logic
    def register(self, who):
        print("[Main (Bot)] New component added ad subscriber")
        self.subscribers.add(who)

    def unregister(self, who):
        self.subscribers.discard(who)

    async def emit(self, message, *args):
        print("[Main (Bot)] Emmiting new event", message, "to all subscribers")
        for subscriber in self.subscribers:
            await subscriber.on_event(message, args)

    # Publish discord events to the publisher-subscriber-structure
    async def on_ready(self):
        await self.emit("ready")
    async def on_raw_reaction_add(self, payload):
        await self.emit("raw_reaction_add", payload)
    async def on_raw_reaction_remove(self, payload):
        await self.emit("raw_reaction_remove", payload)
    async def on_member_join(self, member):
        await self.emit("member_join", member)
    async def on_member_remove(self, member):
        await self.emit("member_remove", member)


project_dir = os.path.dirname(__file__)
if len(project_dir) != 0:
    project_dir += "/"

with open(f"{project_dir}config/key.txt", "r") as file:
    key = file.read().replace("\n", "")

# Bot, du darfst das!
intents = Intents.default()
intents.members = True
Bot(project_dir, intents=intents).run(key)
