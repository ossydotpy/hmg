import discord
from discord import app_commands
from discord.ext import commands
from functions.custom_functions import send_api_request
from functions.buttons import Buttons
from datetime import datetime
import math


class HolderStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @app_commands.command(name="distribution")
    @app_commands.choices(collection=[
        app_commands.Choice(name="HM Millitia", value="fec7dfa59902eb40f65a62812662769962d5662f2a6bc2804b829881"),
        app_commands.Choice(name="HM Prio + Prototypes", value="5cf33cfea1b37c289060f55fa09c1fb3b9cb6972e40d9ed2f94a5ada"),
        app_commands.Choice(name="HM Apartments", value="40f9007b2fadb91a1c1aa69d651e3177547d123713b755eebbe09f54")
        ])
    async def distribution(self, interaction: discord.Interaction, collection: app_commands.Choice[str]):
        """check holder distribution of listed collections"""
        await interaction.response.defer()

        distro_url = f"https://server.jpgstoreapis.com/analytics/holders-distribution/{collection.value}"

        try:
            supply_url =f"https://server.jpgstoreapis.com/collection/{collection.value}/supply"
            supply, statcode = await send_api_request(apiurl=supply_url)
            
            data, status = await send_api_request(apiurl=distro_url)
            if status == 200:
                if statcode == 200:
                    distro_embed = discord.Embed(title=f"{collection.name} Holder Distribution",color=discord.Color.blurple(),
                                                description="Distribution Breakdown",timestamp=datetime.utcnow())
                    distro_embed.add_field(name="Supply", value=f"{collection.name.upper()} has a supply of {supply['supply']} NFTs of which:")
                    for key, value in data["holders"].items():
                        distro_embed.add_field(name="", value=f'[ {value} ] holders own [ {key} ] NFTs from the collection', inline=False)
                    
                    distro_embed.add_field(name="Holder Count", value=f"{data['totalHolders']}", inline=False)
                    distro_embed.add_field(name="Holder Ratio", value=f"""
                                           on average, each holder has a share of approximately {math.ceil(int(supply['supply'])/data['totalHolders'])} units from the total supply
                                           
                                           """)
                    distro_embed.set_thumbnail(url="https://hermonsters.com/core/views/96a589a588/assets/images/hm_logo.png")
                    await interaction.followup.send(embed=distro_embed)
                else:
                    await interaction.followup.send(content="server-side error")
            else:
                await interaction.followup.send(content="server-side error")
        except Exception as e:
            await interaction.followup.send("errrrr")
            print(e)



    @app_commands.command(name = "floor")
    @app_commands.choices(collection = [
        app_commands.Choice(name="HM Millitia", value="fec7dfa59902eb40f65a62812662769962d5662f2a6bc2804b829881"),
        app_commands.Choice(name="HM Prio + Prototypes", value="5cf33cfea1b37c289060f55fa09c1fb3b9cb6972e40d9ed2f94a5ada"),
        app_commands.Choice(name="HM Apartments", value="40f9007b2fadb91a1c1aa69d651e3177547d123713b755eebbe09f54")
    ])
    async def floor(self, interaction: discord.Interaction, collection: app_commands.Choice[str]):
        """check the floor price of listed collections"""
        await interaction.response.defer()

        url = f"https://server.jpgstoreapis.com/collection/{collection.value}/floor"
        floor_url =f"https://server.jpgstoreapis.com/search/tokens?policyIds={collection.value}&saleType=default&sortBy=price-low-to-high&traits=e30%3D&listingTypes=ALL_LISTINGS&nameQuery=&verified=default&onlyMainBundleAsset=false&size=1"

        try:
            floor_nft , statcode = await send_api_request(apiurl=floor_url)
            for item in floor_nft["tokens"]:
                floor_nft_name = item["display_name"]
                floor_nft_id = item["asset_name"]
                floor_nft_img = item["media_urls"][3]
                
            data, status = await send_api_request(apiurl=url)

            if status==200:
                if statcode ==200:
                    floor_embed = discord.Embed(title=f"{collection.name} Floor Price", color=discord.Color.brand_green(), timestamp=datetime.utcnow())
                    floor_embed.add_field(name=f'{data["floor"]/1_000_000.0:,.0f} ₳',value="")
                    floor_embed.add_field(name="Current Floor Asset",value=f"{floor_nft_name}")
                    floor_embed.set_thumbnail(url=floor_nft_img)

                    view = Buttons()
                    view.add_item(
                        discord.ui.Button(
                            label=f"Buy on jpg.store",
                            style=discord.ButtonStyle.green,
                            url=f"https://www.jpg.store/asset/{floor_nft_id}",
                            emoji="<:hmoji:1042497799658410037>",)
                        )
                    await interaction.followup.send(embed=floor_embed, view=view)
                    return
                else:
                    await interaction.followup.send("errrr")
            else:
                await interaction.followup.send(content="server-side error. try again later :)")
        except Exception as e:
            await interaction.followup.send("errrr")
            print(e)

async def setup(bot):
    await bot.add_cog(HolderStats(bot))