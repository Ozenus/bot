import os
import discord

TOKEN = os.getenv("DISCORD_TOKEN")

YOUR_ID = 1045262704543281242

TARGET_ID = 900057792751206453

TEXT_CHANNEL_ID = 111111111111111111
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
client = discord.Client(intents=intents)
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
