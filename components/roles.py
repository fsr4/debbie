"""
Rolesystem
~~~~~~~~~~
"""
from discord import HTTPException, NotFound, Object
import os


class Roles:
    majors = []
    topics = []
    roles = []
    logger = None
    parent = None
    role_message_id = None
    emoji_to_role = None

    # IDs of the support and commands Channel
    supportChannel = 828645631609536552 #DEV-DISCORD
    #supportChannel = 825376458276339713 #FB4-DISCORD 

    # The User reactions are locked - currently Ayndread#4242
    lockedUser =  147117399391469568 

    # https://discordpy.readthedocs.io/en/latest/api.html#role
    # https://discordpy.readthedocs.io/en/latest/api.html#reaction

    def __init__(self, parent):
        print("[Roles] Starting component")
        self.logger = parent.logger
        self.parent = parent

        working_dir = os.getcwd()

        with open(f"{working_dir}/config/roles.txt") as role_file:
            self.roles = role_file.read().splitlines()
        with open(f"{working_dir}/config/majors.txt") as major_file:
            self.majors = major_file.read().splitlines()
        with open(f"{working_dir}/config/topics.txt") as topic_file:
            self.topics = topic_file.read().splitlines()
        
        self.log = open(f"{working_dir}/log.txt", "a")

        # ID of message that can be reacted to to add role
        self.role_message_id = [820311782714769418, 827890777102483457, 828654368508608602] #DEV-DISCORD
        #self.role_message_id = [825411896676450371, 826061339105034320, 826060157049896961, 825412786477727785, 822844083629326336] #FB4-DISCORD

        self.emoji_to_role = {
            #FB4-DISCORD
            #"ai": 701076932128931891,  
            #"fiw": 701079605389426698,
            #"ikg": 825381218942058547,
            #"imi": 701080074429923368,
            #"wi": 701078301200089170,
            #"wiko": 701079069340729345,
            #"wiw": 701078822878969969,
            #"wm": 701078451989381150,
            #"far": 701078591986860063,
            #"🍿": 706937054751096832, 
            #"🎮": 706936994386804857,

            #DEV-DISCORD 
            "ai": 825444462834090004,
            "fiw": 825455839325192212,
            "ikg": 825456114350948402,
            "imi": 822895053009715202,
            "wi": 825456172487278653,
            "wiko": 825456214572925009,
            "wiw": 825456242205917184,
            "wm": 825368307301220372,
            "far": 825456457116942368,
            "🍿": 820325939632275456,
            "🎮": 820325903313535027,
        }
        parent.register(self)
                
        print("[Roles] Component started")

    # Handle Discord events
    async def on_event(self, event, args):
        if event == "raw_reaction_add":
            await self.on_raw_reaction_add(args[0])
        #if event == "raw_reaction_remove":
         #   await self.on_raw_reaction_remove(args[0])
            
    # https://discordpy.readthedocs.io/en/latest/api.html#discord.on_reaction_add
    # https://github.com/Rapptz/discord.py/blob/master/examples/reaction_roles.py

    # add role on a specific user reaction
    async def on_raw_reaction_add(self, payload):
        # Make sure that the message the user is reacting to is the one we care about
        if not payload.message_id in self.role_message_id:
            return

        self.logger.info(f"[Roles] New reaction {payload.emoji.name}")
        """Gives a role based on a reaction emoji."""

        try:
            role_id = self.emoji_to_role[payload.emoji.name]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            self.logger.error(f"[Roles] Invalid role emoji")
            return

        self.logger.info(f"[Roles] Found role id: {role_id}")

        guild = self.parent.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try: #to add or remove the role
            # Remove role if member is part of
            if role in payload.member.roles:
                await self.logger.notify(f"{payload.member.mention} left {role.name}", self.supportChannel)
                await payload.member.remove_roles(role)
            
            # Notify user when trying to add multiple roles
            elif role.name in self.majors and any(self.get_role_by_name(majorRole, guild) in payload.member.roles for majorRole in self.majors):
                currentRole = next((r for r in payload.member.roles for majorRole in self.majors if r.name.lower().replace(" ", "") == majorRole.lower().replace(" ", "")), None)
                await self.logger.notify(f"{payload.member.mention} you need to leave {currentRole} before joining {role.name}", self.supportChannel)
            
            # Finally add role
            else: 
                await self.logger.notify(f"{payload.member.mention} is now {role.name}", self.supportChannel)
                await payload.member.add_roles(role)
            
            # Remove all user reactions except for the locked one
            # if payload.emoji.name != "✅":
            reactionMsg = await guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
            members = list(map(lambda member: Object(member.id), list(filter(lambda member: member.id != self.lockedUser, guild.members))))
            # https://discordpy.readthedocs.io/en/latest/api.html?highlight=remove%20reaction#discord.Message.remove_reaction
            [await reactionMsg.remove_reaction(payload.emoji, member) for member in members]

        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    def get_role_by_name(self, role_name, guild):
        role_name = role_name.lower().replace(" ", "")
        role = next((r for r in guild.roles if r.name.lower().replace(" ", "") == role_name), None)
        self.logger.info(f"[Roles] {role}")
        return role

    project_dir = os.path.dirname(__file__)
    if len(project_dir) != 0:
        project_dir += "/"
