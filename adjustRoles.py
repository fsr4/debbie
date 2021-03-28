"""
ACHTUNG: Dieses Skript soll zum Rollensystemwechsel einmalig ausgeführt werden, um die (M) Rollen
         zu entfernen und die entsprechenden User in (B) Rollen zu integrieren!
~~~~~~~~~~
"""

from discord import Client, Intents, Object
from discord import HTTPException
import os

class AdjustRoles(Client):
    oldRoles = []
    newRoles = []
    logger = None

    def __init__(self, working_dir, **options):
        super().__init__(**options)
        print("[Main (Bot)] Starting")
        with open(f"{working_dir}rollAdjustment/oldRoles.txt") as oldRoles_file:
            self.oldRoles = oldRoles_file.read().splitlines()
        with open(f"{working_dir}rollAdjustment/newRoles.txt") as newRoles_file:
            self.newRoles = newRoles_file.read().splitlines()
        self.logger = open(f"{working_dir}/log.txt", "a")
        print("[Main (Bot)] Started successfully")

    async def on_ready(self):
        print(f"[Main (Bot)] Logged in as user {self.user}")
        self.adjust_existing_roles(self.guilds[0])

    async def adjust_existing_roles(self, guild):
        for user in guild.members:
            for roleIdx in range(0, self.oldRoles.count):
                if self.oldRoles[roleIdx] in user.roles:
                    # remove old roles to new roles
                    await user.remove_roles(self.oldRoles[roleIdx])
                    await user.add_roles(self.newRoles[roleIdx], Object(820346720793395201))
                    return

project_dir = os.path.dirname(__file__)
if len(project_dir) != 0:
    project_dir += "/"

with open(f"{project_dir}/config/key.txt", "r") as file:
    key = file.read().replace("\n", "")

intents = Intents.default()
intents.members = True
AdjustRoles(project_dir, intents=intents).run(key)
