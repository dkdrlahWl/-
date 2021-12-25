import discord, time, random, asyncio, requests, os
from discord.ext.commands import bot
client = discord.Client()
prefix = "."
idA, moneyA, timeA, levelA = [], [], [], []

try:
    f = open("UserData.txt", "r")
except:
    f = open("UserData.txt", "w")
    f.close()
    f = open("UserData.txt", "r")
while True:
    line = f.readline()
    if not line:
        break
    line = line.split(",")
    idA.append(line[0])
    moneyA.append(int(line[1]))
    timeA.append(int(line[2]))
    levelA.append(int(line[3]))
f.close()

TOKEN = os.environ.get('BOT_TOKEN')

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")
    game = discord.Game("베타.ver")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    cmd = message.content.split(" ")[0]
    args = message.content.split(" ")[1:]
    ID = str(message.author.id)


    if cmd == prefix + "도움말":
        embed = discord.Embed(title="명령어", description="봇 명령어", color=0x62C1CC)
        embed.add_field(name="도박", value="돈, 돈받기, 도박 <금액>, 올인, 랭킹, 레벨랭킹, 송금 <금액> <@대상>, 상점, 예시 : .레벨업팩1 할시 바로 구매 후 사용", inline=True)
        await message.channel.send("", embed=embed)
        
        


    if cmd == prefix + "돈받기" or cmd == prefix + "ㄷㅂㄱ":
        TIME = int(time.time())
        if ID in idA:
            if TIME - timeA[idA.index(ID)] < 60:  # 시간이 아직 안 지났을 때
                embed = discord.Embed(title="", description="1분 마다 받을 수 있습니다.", color=0x00FFFF)
                await message.channel.send(embed=embed)
                return
            elif TIME - timeA[idA.index(ID)] >= 60:
                timeA[idA.index(ID)] = int(time.time())
        give = random.randrange(1, 3) * random.randrange(1000, 10000)
        if ID in idA:  # ID가 있으면 돈을 더함
            moneyA[idA.index(ID)] += give
        elif not ID in idA:  # ID가 없으면 배열에 새로 추가
            idA.append(ID)
            moneyA.append(give)
            timeA.append(int(time.time()))
            levelA.append(0)
        embed = discord.Embed(title="", description=format(give, ",d")+ "원 만큼 받았습니다 현재 돈: "+ format(moneyA[idA.index(ID)], ",d")+ "원",color=0x500ff,)
        await message.channel.send(embed=embed)
        
        
    if cmd == prefix + "상점" or cmd == prefix + "ㅅㅈ":
        embed = discord.Embed(title="상점", description="", color=0x62C1CC)
        embed.add_field(name="list", value="레벨업팩 1급 : 5만 | 1 ~ 2업 \n\n 레벨업팩 2급 : 20만 | 1 ~ 10업\n\n 레벨업팩 3급 : 100만 | 1 ~ 50업\n\n 레벨업팩 4급 : 300만 | 1 ~ 150업\n\n 레벨업팩 5급 : 900만 | 1 ~ 450업\n\n 레벨업팩 6급 : 5000만 | 1 ~ 5000업\n\n 레벨업팩 7급 : 5억 | 1 ~ 50000업\n\n 레벨업팩 8급 : 55억 | 1 ~ 450000업\n", inline=True)
        await message.channel.send("", embed=embed)
    

    if cmd == prefix + "돈" or cmd == prefix + "ㄷ":
        if ID in idA:  # ID가 있을 때
            embed = discord.Embed(title="",description=format(moneyA[idA.index(ID)], ",d") + " 원",color=0xFF00FF,)
            await message.channel.send(embed=embed)
        elif not ID in idA:  # ID가 없을 때
            embed = discord.Embed(title="", description="0 원", color=0xFF00FF)
            await message.channel.send(embed=embed)


    if cmd == prefix + "내정보" or cmd == prefix + "ㄴㅈㅂ" or cmd == prefix + "ㅈㅂ" or cmd == prefix + "정보":
        if ID in idA:  # ID가 있을 때
            embed = discord.Embed(title="유저 정보", description="", color=0x62c1cc)
            embed.add_field(name="보유자금", value=format(moneyA[idA.index(ID)]), inline=True)
            embed.add_field(name="레벨", value=format(levelA[idA.index(ID)]), inline=True)
            await message.channel.send(embed=embed)
        elif not ID in idA:  # ID가 없을 때
            embed = discord.Embed(title="", description="0 원", color=0xFF00FF)
            await message.channel.send(embed=embed)
        


    if cmd == prefix + "올인" or cmd == prefix + "ㅇㅇ":
        if not ID in idA or moneyA[idA.index(ID)] <= 0:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다.", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        givee = random.randrange(2, 12)
        give = random.randrange(2, 3)  # 성공확률 : 4/9
        count = await message.channel.send("배수 정하는 중 ...")
        await asyncio.sleep(0)
        await count.edit(content="만약 성공하면 건 돈의 " + str(give) + "배 를 얻어요")
        await asyncio.sleep(0)
        if givee % 2 == 0:
            moneyA[idA.index(ID)] *= give
            await count.edit(
                content="올인 성공! 현재 돈: " + format(moneyA[idA.index(ID)], ",d") + "원"
            )
        elif givee % 2 != 0:
            moneyA[idA.index(ID)] = 0
            await count.edit(
                content="올인 실패... 현재 돈: " + format(moneyA[idA.index(ID)], ",d") + "원"
            )

    if cmd == prefix + "도박" or cmd == prefix + "ㄷㅂ":
        if len(args) != 1:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: .도박 돈", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if args[0].isdecimal() == False:  # 숫자가 입력되지 않았을 때
            embed = discord.Embed(title="", description="숫자만 입력해 주세요!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        args[0] = int(args[0])
        if not ID in idA or moneyA[idA.index(ID)] - args[0] < 0:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= args[0]
        givee = random.randrange(3, 10)
        give = random.randrange(2, 3)  # 성공확률 4/9
        count = await message.channel.send("배수 정하는 중 ...")
        await asyncio.sleep(0)
        await count.edit(content="만약 성공하면 건 돈의 " + str(give) + "배 를 얻어요")
        await asyncio.sleep(0)
        if givee % 2 == 0:
            moneyA[idA.index(ID)] += give * args[0]
            await count.edit(
                content="도박 성공! 현재 돈: " + format(moneyA[idA.index(ID)], ",d") + "원"
            )
        elif givee % 2 != 0:
            await count.edit(
                content="도박 실패... 현재 돈: " + format(moneyA[idA.index(ID)], ",d") + "원"
            )
            
            
    if cmd == prefix + "랭킹" or cmd == prefix + "ㄹㅋ":
        rank, rankA = "", []  # 모든 id와 돈을 담아 정렬할 2차원 배열 rankA
        for i in range(0, len(idA)):
            rankA.append([idA[i], moneyA[i]],)
        rankA = sorted(rankA, reverse=True, key=lambda x: x[1])
        for i in range(0, 10):
            try:
                rank += (str(i + 1)+ "위 <@"+ rankA[i][0]+ "> : "+ format(rankA[i][1], ",d")+ "\n")
            except:
                break
        embed = discord.Embed(title="봇1시즌 돈 랭킹", description=rank, color=0xD8AA2D)
        await message.channel.send(embed=embed)
        return
    if cmd == prefix + "레벨랭킹" or cmd == prefix + "ㄹㅂㄹㅋ":
        rank, rankA = "", []  # 모든 id와 돈을 담아 정렬할 2차원 배열 rankA
        for i in range(0, len(idA)):
            rankA.append([idA[i], levelA[i]],)
        rankA = sorted(rankA, reverse=True, key=lambda x: x[1])
        for i in range(0, 10):
            try:
                rank += (str(i + 1)+ "위 <@"+ rankA[i][0]+ "> : "+ format(rankA[i][1], ",d")+ "\n")
            except:
                break
        embed = discord.Embed(title="봇1시즌 레벨 랭킹", description=rank, color=0xD8AA2D)
        await message.channel.send(embed=embed)
        return


    if cmd == prefix + "송금" or cmd == prefix + "ㅅㄱ":
        if len(args) != 2 or args[0][3:-1] in idA:  # 만약 인자 수가 잘못됬거나 순서가 바뀌었을 때
            embed = discord.Embed(title="오류", description="사용법: .송금 돈 @유저이름", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not args[1][3:-1] in idA:  # 송금대상의 ID가 없을 때
            give = 0
            ID = args[1]
            idA.append(ID)
            moneyA.append(give)
            timeA.append(int(time.time()))
            embed = discord.Embed(title="오류", description="송금대상이 등록된 ID가 아닙니다", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA:  # 송금자의 ID가 없을 때
            embed = discord.Embed(title="오류", description="잔액이 부족합니다", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if args[0].isdecimal() == False:  # 숫자가 입력되지 않았을 때
            embed = discord.Embed(title="오류", description="숫자를 입력해주세요", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if moneyA[idA.index(ID)] < int(args[0]):  # 잔액이 부족할 때
            embed = discord.Embed(title="오류", description="잔액이 부족합니다", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        else:  # 모든 이상이 없을 때
            moneyA[idA.index(ID)] -= int(args[0])
            moneyA[idA.index(str(args[1][3:-1]))] += int(args[0])
            embed = discord.Embed(title="", description="송금을 성공하였습니다", color=0x118811)
            await message.channel.send(embed=embed)


    if cmd == prefix + "돈추가":
        if len(args) != 1:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: 돈추가 돈", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if args[0].isdecimal() == False:  # 숫자가 입력되지 않았을 때
            embed = discord.Embed(title="", description="숫자만 입력해 주세요!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        args[0] = int(args[0])
        if not ID in idA or moneyA[idA.index(ID)] - args[0] < 0:# 돈이 부족할 때
            moneyA[idA.index(ID)] += args[0]
            embed = discord.Embed(title="경고!", description="돈이 추가되었습니다", color=0x118811)
            await message.channel.send(embed=embed)
        if not ID in idA or moneyA[idA.index(ID)] - args[0] >= 0:# 돈이 부족할 때
            moneyA[idA.index(ID)] += args[0]
            embed = discord.Embed(title="경고!", description="돈이 추가되었습니다", color=0x118811)
            await message.channel.send(embed=embed)
            return


    if cmd == prefix + "레벨지급":
        if len(args) != 2 or args[0][3:-1] in idA:  # 만약 인자 수가 잘못됬거나 순서가 바뀌었을 때
            embed = discord.Embed(title="오류", description="사용법: 지급 레벨 @유저이름", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not args[1][3:-1] in idA:  # 송금대상의 ID가 없을 때
            give = 0
            ID = args[1]
            idA.append(ID)
            moneyA.append(give)
            timeA.append(int(time.time()))
            embed = discord.Embed(title="오류", description="송금대상이 등록된 ID가 아닙니다", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA:  # 송금자의 ID가 없을 때
            embed = discord.Embed(title="오류", description="잔액이 부족합니다", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if args[0].isdecimal() == False:  # 숫자가 입력되지 않았을 때
            embed = discord.Embed(title="오류", description="숫자를 입력해주세요", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if moneyA[idA.index(ID)] < int(args[0]):  # 잔액이 부족할 때
            embed = discord.Embed(title="오류", description="잔액이 부족합니다", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        else:  # 모든 이상이 없을 때
            levelA[idA.index(str(args[1][3:-1]))] += int(args[0])
            embed = discord.Embed(title="", description="지급을 성공하였습니다", color=0x118811)
            await message.channel.send(embed=embed)


    if cmd == prefix + "레벨업팩1":
        if len(args) != 0:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: 레벨업(번호)", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA or moneyA[idA.index(ID)] < 50000:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= 50000
        level = random.randrange(1, 2)  #1~3
        if ID in idA:
            levelA[idA.index(ID)] += level
            await message.channel.send(format(level) +" " + "level up 하셨습니다"+ "\n" +"현재 level : "+format(levelA[idA.index(ID)]))
            
    if cmd == prefix + "레벨업팩2":
        if len(args) != 0:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: 레벨업팩(번호)", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA or moneyA[idA.index(ID)] < 200000:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= 200000
        level = random.randrange(1, 11)  #4~11
        if ID in idA:
            levelA[idA.index(ID)] += level
            await message.channel.send(format(level) +" " + "level up 하셨습니다"+ "\n" +"현재 level : "+format(levelA[idA.index(ID)]))

    if cmd == prefix + "레벨업팩3":
        if len(args) != 0:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: 레벨업팩(번호)", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA or moneyA[idA.index(ID)] < 1000000:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= 1000000
        level = random.randrange(1, 51)  #4~14
        if ID in idA:
            levelA[idA.index(ID)] += level
            await message.channel.send(format(level) +" " + "level up 하셨습니다"+ "\n" +"현재 level : "+format(levelA[idA.index(ID)]))

    if cmd == prefix + "레벨업팩4":
        if len(args) != 0:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: 레벨업팩(번호)", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA or moneyA[idA.index(ID)] < 3000000:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= 3000000
        level = random.randrange(1, 151)  #4~14
        if ID in idA:
            levelA[idA.index(ID)] += level
            await message.channel.send(format(level) +" " + "level up 하셨습니다"+ "\n" +"현재 level : "+format(levelA[idA.index(ID)]))


    if cmd == prefix + "레벨업팩5":
        if len(args) != 0:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: 레벨업팩(번호)", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA or moneyA[idA.index(ID)] < 9000000:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= 9000000
        level = random.randrange(1, 451)  #4~14
        if ID in idA:
            levelA[idA.index(ID)] += level
            await message.channel.send(format(level) +" " + "level up 하셨습니다"+ "\n" +"현재 level : "+format(levelA[idA.index(ID)]))


    if cmd == prefix + "레벨업팩6":
        if len(args) != 0:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: 레벨업팩(번호)", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA or moneyA[idA.index(ID)] < 50000000:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= 50000000
        level = random.randrange(1, 5001)  #4~14
        if ID in idA:
            levelA[idA.index(ID)] += level
            await message.channel.send(format(level) +" " + "level up 하셨습니다"+ "\n" +"현재 level : "+format(levelA[idA.index(ID)]))


    if cmd == prefix + "레벨업팩7":
        if len(args) != 0:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: 레벨업팩(번호)", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA or moneyA[idA.index(ID)] < 500000000:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= 500000000
        level = random.randrange(1, 50001)
        if ID in idA:
            levelA[idA.index(ID)] += level
            await message.channel.send(format(level) + " " + "level up 하셨습니다" + "\n" + "현재 level : " + format(levelA[idA.index(ID)]))

    if cmd == prefix + "레벨업팩8":
        if len(args) != 0:  # 인자 수가 잘못됬을 때
            embed = discord.Embed(title="오류", description="사용법: 레벨업팩(번호)", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        if not ID in idA or moneyA[idA.index(ID)] < 5500000000:  # 돈이 부족할 때
            embed = discord.Embed(title="", description="돈이 부족합니다!", color=0xFF0000)
            await message.channel.send(embed=embed)
            return
        moneyA[idA.index(ID)] -= 5500000000
        level = random.randrange(1, 450000)
        if ID in idA:
            levelA[idA.index(ID)] += level
            await message.channel.send(format(level) + " " + "level up 하셨습니다" + "\n" + "현재 level : " + format(levelA[idA.index(ID)]))



    f = open("UserData.txt", "w")  # 바뀐 데이터 저장
    for i in range(0, len(idA), 1):
        f.write(str(idA[i]) + "," + str(moneyA[i]) + "," + str(timeA[i]) + "," + str(levelA[i]) + "\n")
    f.close()
    print(ID, cmd,)


client.run(TOKEN)
