"""
Rolesystem
~~~~~~~~~~
"""
from discord import HTTPException, NotFound, Object
import os


class Verify:
    # IDs of the support and commands Channel
    supportChannel = 820281018263142412

    # https://discordpy.readthedocs.io/en/latest/api.html#role
    # https://discordpy.readthedocs.io/en/latest/api.html#reaction

    def __init__(self, parent):
        print("[Roles] Starting component")
        self.logger = parent.logger
        self.parent = parent

        working_dir = os.getcwd()
        self.log = open(f"{working_dir}/log.txt", "a")

        # ID of message that can be reacted to to add role
        self.verify_message_id = 825745357589053470
        
        self.emoji_to_verify = {
            "✅": 825744195896868864
        }

        parent.register(self)
        print("[Roles] Component started")

    # Handle Discord events
    async def on_event(self, event, args):
        if event == "raw_reaction_add":
            await self.on_raw_reaction_add(args[0])
        if event == "raw_reaction_remove":
            await self.on_raw_reaction_remove(args[0])

    # https://discordpy.readthedocs.io/en/latest/api.html#discord.on_reaction_add
    # https://github.com/Rapptz/discord.py/blob/master/examples/reaction_roles.py

    """
    Reaktion hinzufuegen == akzeptiert Regeln
    """
    # add role on a specific user reaction
    async def on_raw_reaction_add(self, payload):
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.verify_message_id:
            return

        self.logger.info(f"[Roles] New reaction {payload.emoji.name}")
        """Gives a role based on a reaction emoji."""

        try:
            verify_id = self.emoji_to_verify[payload.emoji.name]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            self.logger.error(f"[Roles] Invalid role emoji")
            return

        self.logger.info(f"[Roles] Found role id: {verify_id}")

        guild = self.parent.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            return

        verify_role = guild.get_role(verify_id)
        if verify_role is None:
            # Make sure the role still exists and is valid.
            return

        try: # to add or remove the verified role
            if verify_role in payload.member.roles:
                await self.logger.error(f"{payload.member.mention} already accepted the rules.")
            
            # Finally add role
            else: 
                await self.logger.notify(f"{payload.member.mention} accepts the rules.", self.supportChannel)
                await payload.member.add_roles(verify_role)
            
        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass

    """
    Reaktion entfernen == Widerruf des Einverstaendnis 
    """
    async def on_raw_reaction_remove(self, payload):
        # Removes a role based on a reaction emoji.
        # Make sure that the message the user is reacting to is the one we care about
        if payload.message_id != self.verify_message_id:
            return
            
        # member = payload.member
        print(f"[Roles] reaction removed {payload.emoji.name}")

        try:
            verify_id = self.emoji_to_verify[payload.emoji.name]
        except KeyError:
            # If the emoji isn't the one we care about then exit as well.
            self.logger.error(f"[Roles] Could not find matching role!")
            return

        print(f"[Roles] Role found: {verify_id}")

        guild = self.parent.get_guild(payload.guild_id)
        if guild is None:
            # Check if we're still in the guild and it's cached.
            self.logger.error(f"[Roles] Guild is invalid")
            return

        verify_role = guild.get_role(verify_id)
        if verify_role is None:
            # Make sure the role still exists and is valid.
            self.logger.error(f"[Roles] Role is not valid")
            return

        member = guild.get_member(payload.user_id)
        if member is None:
            # Makes sure the member still exists and is valid 147117399391469568
            self.logger.error(f"[Roles] Member is not valid, {payload.user_id}")
            return

        try: # to remove the role
            # Remove role if member is part of
            if verify_role in member.roles:
                await self.logger.notify(f"{member.mention} revokes its consent.", self.supportChannel)
                await member.remove_roles(verify_role)
            
            # Finally add role
            else: 
                await self.logger.error(f"{member.mention} already revoked its consent.")
            
        except HTTPException:
            # If we want to do something in case of errors we'd do it here.
            pass
