import aiohttp
import json
import discord
from datetime import datetime, timedelta
from urllib.parse import quote


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

async def randomimageapi(ctx, url: str):
    async with aiohttp.ClientSession(headers=header) as session:            
        async with session.get(url) as content:
            if content.status != 200:
                return await ctx.reply(":confused: Сервис не отвечает.")
            res = json.loads(await content.text())
            try:
                res['link']
            except:
                print(f"Error in:\n {content.text}\n\n")
                return await ctx.reply(":confused: Что-то пошло не так.")
            em = discord.Embed(color=0xa0cfe5)
            em.set_image(url=res['link'])
            await ctx.send("", embed=em)


async def nekoslifeapi(ctx, url: str, text=""):
    async with aiohttp.ClientSession() as session:            
        async with session.get(url) as content:
            if content.status != 200:
                return await ctx.reply(":confused: Сервис не отвечает.")
            res = json.loads(await content.text())
            try:
                res['url']
            except:
                print(f"Error in:\n {content.text}\n\n")
                return await ctx.reply(":confused: Что-то пошло не так.")
            em = discord.Embed(color=0xa0cfe5)
            em.set_image(url=res['url'])
            await ctx.send(f'{text}', embed=em)


async def freegames(ctx):
    now=datetime.now()
    async with aiohttp.ClientSession() as session:
        async with session.get('https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions') as resp:
            if resp.status !=200:
                await ctx.send(f'{ctx.message.author.mention}:confused: Cервис не отвечает.')
            else:
                result = json.loads(await resp.text())
                await ctx.send("Сейчас в раздаче следующие игры:")
                for item in result['data']['Catalog']['searchStore']['elements']:
                    if item['promotions']==None:
                        continue
                    elif item['promotions']['promotionalOffers'] == []:
                        continue
                    else:
                        startDate = datetime.strptime(item['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        endDate = datetime.strptime(item['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        if now > startDate and now < endDate:
                            em = discord.Embed(title=item['title'], url=f"https://www.epicgames.com/store/ru/product/{quote(item['productSlug'])}/home",  description=item['description'], color=0xa0cfe5)
                            em.set_image(url=quote(item['keyImages'][2]['url'], safe='http://'))

                            em.add_field(name="Начало:", value=startDate.strftime("%m/%d/%Y, %H:%M:%S"), inline=True)
                            em.add_field(name="Конец:", value=endDate.strftime("%m/%d/%Y, %H:%M:%S"), inline=True)

                            #em.description
                            await ctx.send("", embed=em)
                        else:
                            continue