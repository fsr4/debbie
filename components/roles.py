"""
Rolesystem
~~~~~~~~~~
"""
from discord import HTTPException


class Roles:
    # role_names = []
    # topic_names = []
    # roles = []
    logger = None
    parent = None
    role_message_id = None
    emoji_to_role = None

    # https://discordpy.readthedocs.io/en/latest/api.html#role
    # https://discordpy.readthedocs.io/en/latest/api.html#reaction

    def __init__(self, parent):
        self.logger = parent.logger
        self.parent = parent

        # 820306041304514570 # ID of message that can be reacted to to add role
        self.role_message_id = 820311782714769418
        self.emoji_to_role = {
            # "ai": 701076932128931891,  # ID of role associated with partial emoji object 'partial_emoji_1'
            # "fiw": 701079605389426698,
            # "imi": 701080074429923368,
            # "wi": 701078301200089170,
            # "wiw": 701078822878969969,
            # "wiko": 701079069340729345,
            # "wm": 701078451989381150,
            "🍿": 820325939632275456,
            "🎮": 820325903313535027
        }

        parent.register(self)

    # Handle Discord events
    async def on_event(self, event, a, b, c):
        # if event == "ready":
        #     self.on_ready()
        # elif event == "message":
        #     self.on_message(a)
        if event == "raw_reaction_add":
            await self.on_raw_reaction_add(a)
        elif event == "raw_reaction_remove":
            await self.on_raw_reaction_remove(a)

    # https://discordpy.readthedocs.io/en/latest/api.html#discord.on_reaction_add
    # https://github.com/Rapptz/discord.py/blob/master/examples/reaction_roles.py

    # add role on a specific user reaction
    async def on_raw_reaction_add(self, payload):
        self.logger.info(f"Neue reaction {payload.emoji.name}")
        """Gives a role based on a reaction emoji."""

        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji.name]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            self.logger.error(f"Invalid role emoji")
            return

        self.logger.info(f"Found role id: {role_id}")

        guild = self.parent.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            return

        try:
            # Finally add the role
            await payload.member.add_roles(role)
        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    async def on_raw_reaction_remove(self, payload):
        # member = payload.member
        print(f"reaction entfernt {payload.emoji.name}")
        """Removes a role based on a reaction emoji."""
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.role_message_id:
            return

        try:
            role_id = self.emoji_to_role[payload.emoji.name]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            self.logger.error(f"Konnte keine passende Rolle finden")
            return

        print(f"Neue Rolle gefunden: {role_id}")

        guild = self.parent.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            self.logger.error(f"Guild is invalid")
            return

        role = guild.get_role(role_id)
        if role is None:
            # Make sure the role still exists and is valid.
            self.logger.error(f"Role is not valid")
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            # Makes sure the member still exists and is valid 147117399391469568
            self.logger.error(f"Member is not valid, {payload.user_id}")
            return

        try:
            # Finally, remove the role
            await member.remove_roles(role)
        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            self.logger.error("HTTPException")
            pass
