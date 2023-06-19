import json
import re
from typing import Optional
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
    
    async def create_progress_bar(self,value, max_value, bar_length=15):
        filled_length = int(bar_length * value / max_value)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        return f"[{bar}]"
    
    def cooldown_for_everyone_but_me(
        interaction: discord.Interaction,
    ) -> Optional[app_commands.Cooldown]:
        if interaction.user.id == 638340154125189149:
            return None
        return app_commands.Cooldown(1, 180.0)

    @app_commands.checks.dynamic_cooldown(cooldown_for_everyone_but_me)
    @app_commands.command()
    @app_commands.choices(collection = [
        app_commands.Choice(name="HM Millitia", value="data/mmm_features.json"),
        app_commands.Choice(name="HM Prio Gang", value="data/prio_features.json"),
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
                    title=f"order for... {interaction.user.display_name}", 
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
                    f"Defense: **{result['defense']}**\n"
                    f"Strength: **{result['strength']} **\n"
                    f"Dexterity: **{result['dexterity']}**\n"
                    f"Perception: **{result['perception']} **\n"
                )
                    stats_right = (
                        f"Constitution: **{result['constitution']}**\n"
                        f"Hit Points: **{result['hit_points']}**\n"
                        f"V. Handling: **{result['vehicle_handling']}**\n"
                    )

                    stats_combined = '\n'.join([f"{stats_left.splitlines()[i]}\u2003{stats_right.splitlines()[i]}" for i in range(3)])
                    embed.set_image(url=result['image'])

                    embed.add_field(
                        name=':bookmark_tabs: Monster Bio\n', 
                        value=f"Class:\u2000**{result['class']}**\n"
                        f"Birth State:\u2000**{result['birth_state']}**"
                    )

                    embed.add_field(
                        name=':bar_chart: Monster Stats',
                        value=stats_combined,
                        inline=False  
                    )
                    
                    embed.add_field(
                            name=':abacus: Summary', 
                            value=f"Total Points:\u2000 **{result['total']}**\n"
                            f"Ratings:\u2000 **{round((result['total_minus_hp']/result['max'])*100,2)}% {await self.create_progress_bar(value=result['total_minus_hp'],max_value=result['max'])}**"
                        )
                    embed.set_thumbnail(url='https://hermonsters.com/core/views/96a589a588/assets/images/hm_logo.png')
                    embed.set_footer(text="made with ❤️ By chainsmith")
                    view = buttons.Buttons()
                    view.add_item(
                        discord.ui.Button(
                            label=f"View on jpg.store",
                            style=discord.ButtonStyle.green,
                            url=f"https://www.jpg.store/asset/{result['id']}",
                            emoji="<:hmoji:1042497799658410037>",)
                        )
                    view.add_item(
                        discord.ui.Button(
                            label=f"get custom bot",row=1,
                            style=discord.ButtonStyle.green,
                            url="https://discord.gg/2sUZ3YShm6",
                            emoji="<:transparentlogo:1114079453258203187>",)
                        )
                await interaction.followup.send(embed=embed, ephemeral=hidden, view=view)
        else:
            await interaction.followup.send(f"No results found for HM asset: #{number}", ephemeral=hidden)


async def setup(bot):
    await bot.add_cog(MMMCog(bot))
