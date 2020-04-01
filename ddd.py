import discord

client = discord.Client()

@client.event
async def on_ready():
    print(client.user.id)
    print("완료")
    game = discord.Game("연애")
    await client.change_presence(status=discord.Status.online, activity=game)






@client.event
async def on_message(message):
    if message.content.startswith("민지안녕"):
         await message.channel.send("안녕!")
    if message.content.startswith("민지강화실패"):
         await message.channel.send("나대지마~")
    if message.content.startswith("민지이쁘다"):
         await message.channel.send("고마워 내가쫌 ㅎ")
    if message.content.startswith("민지야"):
         await message.channel.send("네!")
    if message.content.startswith("민지뭐해"):
         await message.channel.send("좀비고하는중!")
    if message.content.startswith("민지바보"):
         await message.channel.send("뭐?")
    if message.content.startswith("민지애교해봐"):
         await message.channel.send("뀨우이이잉 > 3 < 삉삉")
    if message.content.startswith("민지귀여워"):
         await message.channel.send("기욤발사!!!!쀼쀼♥ 핫튜뿅뿅!!♥♥ 띠드버거 머꾸띠퍼ㅠ3ㅠ")


    if message.content == "!도움말":
        embed = discord.Embed(title="명령어", description="봇 명령어", color=0x62c1cc)
        embed.add_field(name="돼지민지", value="민지안녕, 민지강화실패, 민지이쁘다, 민지야, 민지뭐해, 민지바보, 민지애교해봐", inline=True)
        await message.channel.send('', embed=embed)






client.run("Njk0NTgyNTMyNDg1Njc3MTI5.XoNuig.dWoadsC05Irjs9rkWYd6gqT6WiA")