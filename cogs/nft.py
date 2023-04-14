import json
import re
from discord.ext import commands
import discord

class NFTCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print ('nft cog ready')

    @staticmethod
    def retrieve_features():
        with open('features.json', 'r') as features:
            data = json.load(features)
        return data

    @commands.command()
    async def search(self, ctx, keyword: str):
        nfts = self.retrieve_features()
        if keyword.startswith('#'):
            exact_match = re.match(r'^#(\d+)$', keyword)
            if exact_match:
                number = int(exact_match.group(1))
                results = [d for d in nfts if int(d['name'].split()[-1][1:]) == number]
            else:
                results = [d for d in nfts if keyword.lower() in d['name'].lower()]
            if results:
                    embed = discord.Embed(title="NFT Search Results", color=0x00ff00)
                    for result in results:
                        embed.add_field(name=result['name'],
                                        value=f"Defense: {result['defense']} \t Strength: {result['strength']}\n "
                                              f"Dexterity: {result['dexterity']} \t Hit Points: {result['hit_points']}\n "
                                              f"Perception: {result['perception']} \t Constitution: {result['constitution']}\n "
                                              f"Vehicle Handling: {result['vehicle_handling']}", inline=False,)
                    await ctx.send(embed=embed)
            else:
                await ctx.send(f"No results found for query: {keyword}")
        else:
            await ctx.send("Search query must start with '#'")


async def setup(bot):
    await bot.add_cog(NFTCog(bot))

