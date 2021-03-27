"""
Rolesystem
~~~~~~~~~~
"""
from discord import HTTPException
import os


class Roles:
    majors = []
    topics = []
    roles = []
    logger = None
    parent = None
    role_message_id = None
    emoji_to_role = None

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
        self.role_message_id = 820311782714769418
        
        self.emoji_to_role = {
            # IDs of role associated with partial emoji object from FACHSCHAFT4 
            # "ai": 701076932128931891,  
            # "fiw": 701079605389426698,
            # "ikg": 825381218942058547,
            # "imi": 701080074429923368,
            # "wi": 701078301200089170,
            # "wiko": 701079069340729345,
            # "wiw": 701078822878969969,
            # "wm": 701078451989381150,
            # "far": 701078591986860063,
            #"🍿": 706937054751096832, 
            #"🎮": 706936994386804857

            # IDs of role associated with partial emoji object from DEV-DISCORD
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
            "🎮": 820325903313535027
        }

        parent.register(self)
        
        print("[Roles] Component started")

    # Handle Discord events
    async def on_event(self, event, args):
        # if event == "ready":
        #     self.on_ready()
        # elif event == "message":
        #     self.on_message(a)
        if event == "raw_reaction_add":
            await self.on_raw_reaction_add(args[0])
        #elif event == "raw_reaction_remove":
            #await self.on_raw_reaction_remove(args[0])

    # https://discordpy.readthedocs.io/en/latest/api.html#discord.on_reaction_add
    # https://github.com/Rapptz/discord.py/blob/master/examples/reaction_roles.py

    # add role on a specific user reaction
    async def on_raw_reaction_add(self, payload):
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
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
            for majorRole in self.majors:
                if role in payload.member.roles:
                    await self.logger.notify(f"{payload.member.mention} left {role.name}")
                    await payload.member.remove_roles(role)
                    # TODO remove all user reactions instead of this single one
                    return
                elif self.get_role_by_name(majorRole, guild) != role and self.get_role_by_name(majorRole, guild) in payload.member.roles:
                    await self.logger.notify(f"{payload.member.mention} you need to leave {majorRole} before joining {role.name}")
                    # TODO remove all user reactions instead of this single one
                    return
                else:
                    await self.logger.notify(f"{payload.member.mention} joined {role.name}")
                    await payload.member.add_roles(role)
                    # TODO remove all user reactions instead of this single one
                    return

            """
            for topicRole in self.topics:                
                if self.get_role_by_name(topicRole, guild) in payload.member.roles:
                    await self.logger.notify(f"{member.mention} left {role.name}")
                    await payload.member.remove_roles(role)
                    # TODO remove all user reactions instead of this single one
                    return
                else:
                    await self.logger.notify(f"{member.mention} joined {role.name}")
                    await payload.member.add_roles(role)
                    # TODO remove all user reactions instead of this single one
                    return
            """

        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
    
    """        
    async def on_raw_reaction_remove(self, payload):
        # Removes a role based on a reaction emoji.
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return
            
        # member = payload.member
        print(f"[Roles] reaction entfernt {payload.emoji.name}")

        try:
            role_id = self.emoji_to_role[payload.emoji.name]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            self.logger.error(f"[Roles] Could not find matching role!")
            return

        print(f"[Roles] Role found: {role_id}")

        guild = self.parent.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            self.logger.error(f"[Roles] Guild is invalid")
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            self.logger.error(f"[Roles] Role is not valid")
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            # Makes sure the member still exists and is valid 147117399391469568
            self.logger.error(f"[Roles] Member is not valid, {payload.user_id}")
            return

        try:
            # Finally, remove the role
            self.logger.notify("{user.mention} left {role.name}")
            await member.remove_roles(role)
        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            self.logger.error("[Roles] HTTPException")
            pass
    """

    def get_role_by_name(self, role_name, guild):
        role_name = role_name.lower().replace(" ", "")
        role = next((r for r in guild.roles if r.name.lower().replace(" ", "") == role_name), None)
        self.logger.info(f"[Roles] {role}")
        return role

    project_dir = os.path.dirname(__file__)
    if len(project_dir) != 0:
        project_dir += "/"

    #await channel.send(f"{user.mention} wurde aus {role.name} entfernt!\n")
    #self.log.write(f"Removed {user.name} from role {role.name}\n")
    #self.log.flush()
