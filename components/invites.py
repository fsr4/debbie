"""
Rolesystem über Invite-Links
~~~~~~~~~~
"""
from discord import HTTPException

class Invites:
    logger = None
    parent = None
    invites = {}
    invites_to_roles = {}
    

    #DEV-DISCORD Roles
    studentRole = 820346720793395201
    lecturerRole = 822851116266029057
    buddyRole = 822851121319378966
    guestRole = 822851122590253086
    alumniRole = 825456973406666752
    """
    #FS4-DISCORD Roles
    studenRole = 820346720793395201
    lecturerRole = 822851116266029057
    buddyRole = 822851121319378966
    guestRole = 822851122590253086
    alumniRole = 825456973406666752
    """

    # https://discordpy.readthedocs.io/en/latest/api.html#role
    # https://discordpy.readthedocs.io/en/latest/api.html#reaction

    def __init__(self, parent, project_dir):
        print("[Invites] Starting component")
        self.logger = parent.logger
        self.parent = parent

        #invite codes are ignored by .gitignore
        with open(f"{project_dir}invites/student.txt", "r") as file:
          studentKey = file.read().replace("\n", "")
        with open(f"{project_dir}invites/lecturer.txt", "r") as file:
          lecturerKey = file.read().replace("\n", "")
        with open(f"{project_dir}invites/alumni.txt", "r") as file:
          alumniKey = file.read().replace("\n", "")
        with open(f"{project_dir}invites/buddy.txt", "r") as file:
          buddyKey = file.read().replace("\n", "")
        with open(f"{project_dir}invites/guest.txt", "r") as file:
          guestKey = file.read().replace("\n", "")
        
        self.invites_to_roles = {}
        self.invites_to_roles[studentKey] = self.studentRole
        self.invites_to_roles[lecturerKey] = self.lecturerRole
        self.invites_to_roles[alumniKey] = self.alumniRole
        self.invites_to_roles[buddyKey] = self.buddyRole
        self.invites_to_roles[guestKey] = self.guestRole

        parent.register(self)
        print("[Invites] Component started")

    # Handle Discord events
    async def on_event(self, event, args):
        if event == "ready":
            await self.on_ready()
        elif event == "member_join":
            await self.on_member_join(args[0])
        elif event == "member_remove":
            await self.on_member_remove(args[0])

    async def on_ready(self): 
        # Getting all the guilds the bot is in
        for guild in self.parent.guilds:
            # Adding each guild's invites to the dict
            self.invites[guild.id] = await guild.invites()
            print("[Invites] Got invites:", self.invites)
    
    def find_invite_by_code(self, invite_list, code):
        # Simply looping through each invite in an
        # invite list which we will get using guild.invites()
        for inv in invite_list:
            # Check if the invite code in this element
            # of the list is the one we're looking for
            if inv.code == code:
                # If it is, we return it.
                return inv

    async def on_member_join(self, member):
        print("[Invites] New member joined")
        # Getting the invites before the user joining
        # from our cache for this specific guild
        invites_before_join = self.invites[member.guild.id]
        # Getting the invites after the user joining
        # so we can compare it with the first one, and
        # see which invite uses number increased
        invites_after_join = await member.guild.invites()
        # Loops for each invite we have for the guild
        # the user joined.
        for invite in invites_before_join:
            # Now, we're using the function we created just
            # before to check which invite count is bigger
            # than it was before the user joined.
            if invite.uses < self.find_invite_by_code(invites_after_join, invite.code).uses:
                # Now that we found which link was used,
                # we will print a couple things in our console:
                # the name, invite code used the the person
                # who created the invite code, or the inviter.
                print(f"[Invites] Member {member.name} Joined")
                print(f"[Invites] Invite Code: {invite.code}")
                print(f"[Invites] Inviter: {invite.inviter}")
                
                # Find the role for the new member
                try:
                    role_id = self.invites_to_roles[invite.code]
                except KeyError:
                    self.logger.error(f"[Invites] Invalid invite code, using guest")
                    # Use Guest role
                    role_id = self.guestRole

                self.logger.info(f"[Invites] Found role id: {role_id}")

                guild = self.parent.get_guild(member.guild.id)
                if guild is None:
                    # Check if we're still in the guild and it's cached.
                    self.logger.error(f"[Invites] Error: No guild - Abort!")
                    return

                role = guild.get_role(role_id)

                if role is None:
                    # Make sure the role still exists and is valid.
                    self.logger.error(f"[Invites] Error: No role found in guild - Abort!")
                    return

                try:
                    # Finally add the role
                    await member.add_roles(role)   
                except HTTPException:
                    # If we want to do something in case of errors we'd do it here.
                    pass
                
                self.logger.info(f"[Invites] Given role to new user")

                # We will now update our cache so it's ready
                # for the next user that joins the guild
                self.invites[member.guild.id] = invites_after_join
                # We return here since we already found which 
                # one was used and there is no point in
                # looping when we already got what we wanted
                return
    
    async def on_member_remove(self, member):
      # Updates the cache when a user leaves to make sure
      # everything is up to date
      print("[Invites] Member removed or exited")
      self.invites[member.guild.id] = await member.guild.invites()
