import json
import re
from discord.ext import commands
from discord import app_commands
import discord
import datetime

import functions.buttons as buttons

class MMMCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print ('nft cog ready')

    @staticmethod
    def retrieve_features(path):
        with open(path, 'r') as features:
            data = json.load(features)
        return data
    
    async def create_progress_bar(self,value, max_value, bar_length=10):
        filled_length = int(bar_length * value / max_value)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"{value}/{max_value}\n[{bar}]"

    @app_commands.command()
    @app_commands.choices(collection = [
        app_commands.Choice(name="HM Millitia", value="data/mmm_features.json"),
        app_commands.Choice(name="HM Prio Prio Gang", value="data/prio_features.json"),
        app_commands.Choice(name="HM Proto Gang", value="data/mmm_features.json")
    ])
    @app_commands.describe(number="Asset number example: 10", hidden="choose True to hide results otherwise False",
                           collection="Choose a collection from the list")
    async def search(self, interaction: discord.Interaction, collection: app_commands.Choice[str], number: str, hidden: bool):
        """
        Query HM Assets. Input only asset number
        """
        await interaction.response.defer(ephemeral=hidden)
        try:
            nfts = self.retrieve_features(collection.value)
        except Exception as e:
            print(e.with_traceback)

        results = [d for d in nfts if d['name'].split()[-1] == f"#{number}"]

        if results:
                embed = discord.Embed(
                    title=f"<:olecram_sticker:1062718503997677630> order for.. {interaction.user.display_name}", 
                    description="<:teresa:1102540853626540053> your order has been served!",
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(name=f"Requested by {interaction.user.name}")
                for result in results:

                    embed.add_field(
                            name='Name:', 
                            value=f"**{result['name']}**\n",inline=False
                        )

                    stats_left = (
                    f"Defense:\t**{result['defense']}**\n"
                    f"Strength:\t**{result['strength']}**\n"
                    f"Dexterity:\t**{result['dexterity']}**\n"
                    f"Perception:\t**{result['perception']}**\n"
                )
                    stats_right = (
                        f"Constitution:\t**{result['constitution']}**\n"
                        f"Hit Points:\t**{result['hit_points']}**\n"
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
                    embed.add_field(
                            name='', 
                            value=f"{await self.create_progress_bar(value=result['total'],max_value=result['max'])}", inline=False
                        )
                    embed.set_thumbnail(url='https://hermonsters.com/core/views/96a589a588/assets/images/hm_logo.png')
                    embed.set_footer(text='type `-statsguide` for more')
                    view = buttons.Buttons()
                    view.add_item(
                        discord.ui.Button(
                            label=f"View on jpg.store",
                            style=discord.ButtonStyle.green,
                            url=f"https://www.jpg.store/asset/{result['id']}",
                            emoji="<:hmoji:1042497799658410037>",)
                        )
                await interaction.followup.send(embed=embed, ephemeral=hidden, view=view)
        else:
            await interaction.followup.send(f"No results found for HM asset: #{number}", ephemeral=hidden)


async def setup(bot):
    await bot.add_cog(MMMCog(bot))
