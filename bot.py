import os
import discord
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

YOUR_ID = 1045262704543281242
TARGET_ID = 900057792751206453
VOICE_JOIN_CHANNEL_ID = 1259222715479363645  # Канал для пингов при заходе в войс
RAID_CHANNEL_ID = 1513954926735392951  # Канал для команды /raid (замените на нужный ID)

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True


class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        synced = await self.tree.sync()
        print(f"Загружено {len(synced)} команд")


client = MyClient()


@client.event
async def on_ready():
    print(f"Бот запущен как {client.user}")


@client.tree.command(
    name="raid",
    description="Пингнуть всех о рейде"
)
async def raid(interaction: discord.Interaction):
    # Проверяем, что команда вызвана в нужном канале
    if interaction.channel_id != RAID_CHANNEL_ID:
        await interaction.response.send_message(
            f"❌ Эту команду можно использовать только в канале <#{RAID_CHANNEL_ID}>",
            ephemeral=True
        )
        return
    
    await interaction.response.send_message(
        "@everyone 🚨 РЕЙД!"
    )


@client.tree.command(
    name="online",
    description="Проверить что бот работает"
)
async def online(interaction: discord.Interaction):
    await interaction.response.send_message(
        "🟢 Бот онлайн!"
    )


@client.event
async def on_voice_state_update(member, before, after):

    if member.id != YOUR_ID:
        return

    if before.channel is None and after.channel is not None:

        # Используем отдельный канал для пингов при заходе в войс
        channel = client.get_channel(VOICE_JOIN_CHANNEL_ID)

        if channel:
            await channel.send(
                f"<@{TARGET_ID}> {member.display_name} зашёл в войс!"
            )


client.run(TOKEN)1
