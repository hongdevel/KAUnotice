import scraper as sc
import discord
from discord import app_commands
from discord.ext import tasks
from discord.ui import View, Button
import random
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()  # 기본적인 intents만 활성화

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
        self.scraping_data = [
            {"name":"일반", "url":'https://kau.ac.kr/kaulife/notice.php', "last_data":None},
            {"name":"학사", "url":'https://kau.ac.kr/kaulife/acdnoti.php', "last_data":None},
            {"name":"장학및대출", "url":'https://kau.ac.kr/kaulife/scholnoti.php', "last_data":None},
            {"name":"행사", "url":'https://kau.ac.kr/kaulife/event.php', "last_data":None},
            {"name":"모집및채용", "url":'https://kau.ac.kr/kaulife/recruitment.php', "last_data":None},
            {"name":"입찰", "url":'https://kau.ac.kr/kaulife/bid.php', "last_data":None},
            {"name":"전염병관리", "url":'https://kau.ac.kr/kaulife/covidnoti.php', "last_data":None},
            {"name":"IT", "url":'https://kau.ac.kr/kaulife/itnoti.php', "last_data":None},
            {"name":"산학및연구", "url":'https://kau.ac.kr/kaulife/iunoti.php', "last_data":None},
            {"name":"교내식단표", "url":'https://kau.ac.kr/kaulife/foodmenu.php', "last_data":None},
        ]

    async def on_ready(self):
        print(f"Logged in as {self.user}")
        if not detect_new_notice.is_running():
            detect_new_notice.start()

    async def setup_hook(self):
        await self.tree.sync()

class UrlButton(View):
    def __init__(self, label:str, url:str):
        super().__init__(timeout=None)
        self.add_item(Button(label=label, url=url))

client = MyClient()

@tasks.loop(hours=1)
async def detect_new_notice():
    embed = None
    
    for page in client.scraping_data:
        html = sc.target_html(page["url"])
        new_data = sc.get_new_notice_num(html)

        if page["last_data"] == None:
            print(f"{page["name"]}공지 페이지의 변화 감지를 시작합니다.")
            page["last_data"] = new_data
        elif page["last_data"] != new_data:
            page["last_data"] = new_data
            titles = sc.extract_title(html)
            embed = discord.Embed(title=f"{page["name"]}공지에 새로운 공지가 게시되었습니다.", color=0xff7424)
            print(f"{page["name"]}공지에 새로운 공지가 감지되었습니다. 임베드를 전송합니다.")
            for title in titles:
                embed.add_field(name=title, value='', inline=False)
        else:
            print(f"{page["name"]}공지에 새로운 공지가 감지되지 않았습니다.")

        if embed != None:
            for guild in client.guilds:
                system_channel = guild.system_channel
                if system_channel:
                    await system_channel.send(embed=embed, view=UrlButton(label=f"{page["name"]}공지 바로가기", url=page["url"]))
            embed = None
        
        delay = random.uniform(3, 7)
        print(f"{page["name"]}공지 페이지의 스크래핑을 완료하였습니다. 다음 요청까지 걸리는 시간 : {delay:.2f}")
        await asyncio.sleep(delay)

@client.tree.command(name="공지확인", description="선택한 종류의 최근 공지를 확인합니다.")
async def view_notice(interaction: discord.Interaction, sort: sc.NoticeUrls):
    html = sc.target_html(sort.value)
    titles = sc.extract_title(html)
    embed = discord.Embed(title=f"{sort.name}공지", color=0x7da7fa)
    for title in titles:
        embed.add_field(name=title, value='', inline=False)
    
    await interaction.response.send_message(embed=embed, view=UrlButton(label=f"{sort.name}공지 바로가기", url=sort.value))

client.run(DISCORD_TOKEN)