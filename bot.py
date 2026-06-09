import os
import discord
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

YOUR_ID = 1045262704543281242

TARGET_ID = 900057792751206453

TEXT_CHANNEL_ID = 1513954926735392951
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
client = discord.Client(intents=intents)
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        await self.tree.sync()
client = MyClient()
@client.event
async def on_ready():
    print(f"Запущен как {client.user}")
@client.tree.command(name="raid", description="Пингнуть всех")
async def raid(interaction: discord.Interaction):
    await interaction.response.send_message("@everyone :rotating_light: RAID!")
@client.event
async def on_ready():
    print(f"Бот запущен как {client.user}")
@client.event
async def on_voice_state_update(member, before, after):
    # Проверяем, что это именно ты
    if member.id != YOUR_ID:
        return
    # Если ты вошёл в голосовой канал
    if before.channel is None and after.channel is not None:
        channel = client.get_channel(TEXT_CHANNEL_ID)
        if channel:
            await channel.send(
                f"<@{TARGET_ID}> {member.display_name} зашёл в войс!"
            )
client.run(TOKEN)
