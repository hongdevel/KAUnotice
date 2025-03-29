import scraper as sc
import discord
from discord import app_commands
from discord.ext import tasks
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()  # 기본적인 intents만 활성화

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.latest_notice = [0, 0]

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        if not detect_new_notice.is_running():
            detect_new_notice.start()

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@tasks.loop(minutes=1)
async def detect_new_notice():
    html = sc.target_html("https://kau.ac.kr/kaulife/notice.php")
    last_data = sc.get_last_notice_num(html)

    if client.latest_notice == [0, 0]:
        message = "KAUnotice의 호스팅이 시작되었습니다!"
        client.latest_notice = last_data
    elif client.latest_notice != last_data:
        client.latest_notice = last_data
        message = sc.extract_title()
    else:
        message = "변경사항 없음"

    for guild in client.guilds:
        system_channel = guild.system_channel
        if system_channel:
            await system_channel.send(message)

#command

client.run(DISCORD_TOKEN)