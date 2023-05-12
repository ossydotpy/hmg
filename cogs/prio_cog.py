import json
import re
from discord.ext import commands
from discord import app_commands
import discord
import datetime

class PRIOCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print ('nft cog ready')

    @staticmethod
    def retrieve_features():
        with open('data/prio_features.json', 'r') as features:
            data = json.load(features)
        return data

    @app_commands.command(name="prio")
    async def prio(self, interaction: discord.Interaction, keyword: str):
        await interaction.response.defer()
        nfts = self.retrieve_features()
        if keyword.startswith('#'):
            exact_match = re.match(r'^#(\d+)$', keyword)
            if exact_match:
                number = int(exact_match.group(1))
                results = [d for d in nfts if int(d['name'].split()[-1][1:]) == number]
            else:
                results = [d for d in nfts if keyword.lower() in d['name'].lower()]
            if results:
                    embed = discord.Embed(
                        title="NFT Search Results", 
                        description="Here are the search results for the requested NFT:",
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.set_author(name=f"Requested by {interaction.user.name}")
                    for result in results:
                        embed.add_field(
                                name='Name:', 
                                value=f"**{result['name']}**\n"
                            )

                        stats_left = (

                        f"Defense:\t\t**{result['defense']}**\n"
                        f"Strength:\t\t**{result['strength']}**\n"
                        f"Dexterity:\t\t**{result['dexterity']}**\n"
                        f"Perception:\t\t**{result['perception']}**\n"
                    )
                        stats_right = (
                            f"Constitution:\t\t**{result['constitution']}**\n"
                            f"Hit Points:\t\t**{result['hit_points']}**\n"
                            f"V. Handling:\t**{result['vehicle_handling']}**\n"
                        )

                        stats_combined = '\n'.join([f"{stats_left.splitlines()[i]}\t\t{stats_right.splitlines()[i]}" for i in range(3)])
                        embed.set_image(url=result['image'])

                        embed.add_field(
                            name='Monster Bio', 
                            value=f"Class: **{result['class']}**\n"
                            f"Birth State: **{result['birth_state']}**"
                        )

                        embed.add_field(
                            name='Monster Stats',
                            value=stats_combined,
                            inline=False  
                        )
                        
                        embed.add_field(
                                name='Summary', 
                                value=f"Total Points:\t\t **{result['total']}**\n"
                                f"Ratings:\t\t **{round((result['total_minus_hp']/result['max'])*100,2)}%**"
                            )
                        
                        embed.set_thumbnail(url='https://hermonsters.com/core/views/96a589a588/assets/images/hm_logo.png')
                        embed.set_footer(text='type `-statsguide` for more')
                    await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(f"No results found for query: {keyword}",ephemeral=True)
        else:
            await interaction.followup.send("Search query must start with '#'",ephemeral=True)



async def setup(bot):
    await bot.add_cog(PRIOCog(bot))

