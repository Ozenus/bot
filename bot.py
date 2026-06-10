import os
import discord
from discord import app_commands

TOKEN = os.getenv("DISCORD_TOKEN")

YOUR_ID = 1045262704543281242
TARGET_ID = 900057792751206453
VOICE_JOIN_CHANNEL_ID = 1513954926735392951
RAID_CHANNEL_ID = 1259222715479363645 # Замените на нужный ID

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.message_content = True  # Важно для некоторых версий


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
    if interaction.channel_id != RAID_CHANNEL_ID:
        await interaction.response.send_message(
            f"❌ Эту команду можно использовать только в канале <#{RAID_CHANNEL_ID}>",
            ephemeral=True
        )
        return
    
    # Получаем канал и проверяем права
    channel = client.get_channel(RAID_CHANNEL_ID)
    
    # Проверяем права бота в канале
    bot_member = channel.guild.get_member(client.user.id)
    
    if not bot_member.guild_permissions.mention_everyone:
        await interaction.response.send_message(
            "❌ У бота нет права `mention @everyone` на этом сервере!",
            ephemeral=True
        )
        return
    
    if not channel.permissions_for(bot_member).mention_everyone:
        await interaction.response.send_message(
            "❌ У бота нет права `mention @everyone` в этом канале!",
            ephemeral=True
        )
        return
    
    # Отправляем сообщение в канал и пинг
    try:
        await channel.send(
            "@everyone 🚨 RAID"
        )
        await interaction.response.send_message(
            "✅ Пинг отправлен!",
            ephemeral=True
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ Ошибка: у бота недостаточно прав для отправки @everyone!",
            ephemeral=True
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
        channel = client.get_channel(VOICE_JOIN_CHANNEL_ID)

        if channel:
            await channel.send(
                f"<@{TARGET_ID}> {member.display_name} зашёл в войс!"
            )


client.run(TOKEN)
