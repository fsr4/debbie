from discord import Client
from discord.utils import get


class Bot(Client):
    role_names = []
    topic_names = []
    roles = []
    log = None

    def __init__(self, **options):
        super().__init__(**options)
        role_file = open("roles.txt")
        self.role_names = role_file.read().splitlines()
        role_file.close()
        print(self.role_names)
        topic_file = open("topics.txt")
        self.topic_names = topic_file.read().splitlines()
        topic_file.close()
        print(self.topic_names)
        self.log = open("log.txt", "a")

    async def on_ready(self):
        print(f"Logged in as user {self.user}")

    async def on_message(self, message):
        if message.author == self.user or (message.channel.name != "rollen" and message.channel.name != "befehle"):
            return
        if len(self.roles) == 0 and message.content == "!initbot":
            self.setup(message.guild)
            return
        if len(self.roles) == 0:
            return
        if message.content.lower().startswith("!join "):
            await self.handle_role_joining(message.author, message.content[6:], message.channel)
            return
        if message.content.lower().startswith("!leave "):
            await self.handle_role_leaving(message.author, message.content[7:], message.channel)

    def setup(self, guild):
        for role in self.role_names:
            self.roles.append(get(guild.roles, name=role))
        for topic in self.topic_names:
            self.roles.append(get(guild.roles, name=topic))
        print(list(map(lambda r: r.name, self.roles)))

    async def handle_role_joining(self, user, role_name, channel):
        role = self.get_role_by_name(role_name)
        if role is None:
            return
        if role_name in self.topic_names:
            await self.handle_topic_joining(user, role, channel)
            return
        await self.remove_existing_roles(user)
        await user.add_roles(role)
        await channel.send(f"{user.mention} wurde zum Studiengang {role_name.upper()} hinzugefügt!\n")
        self.log.write(f"Added {user.name} to role {role.name}\n")
        self.log.flush()

    async def handle_role_leaving(self, user, role_name, channel):
        role = self.get_role_by_name(role_name)
        if role is None:
            return
        await user.remove_roles(role)
        await channel.send(f"{user.mention} wurde aus {role.name} entfernt!\n")
        self.log.write(f"Removed {user.name} from role {role.name}\n")
        self.log.flush()

    def get_role_by_name(self, role_name):
        role = next((r for r in self.roles if r.name.lower() == role_name.lower()), None)
        return role

    async def remove_existing_roles(self, user):
        for role in self.roles:
            if role in user.roles:
                await user.remove_roles(role)
                return

    async def handle_topic_joining(self, user, role, channel):
        await user.add_roles(role)
        await channel.send(f"{user.mention} wurde zu {role.name} hinzugefügt!\n")
        self.log.write(f"Added {user.name} to role {role.name}\n")
        self.log.flush()


with open('key.txt', 'r') as file:
    key = file.read().replace('\n', '')

Bot().run(key)
