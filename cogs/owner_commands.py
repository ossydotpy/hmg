from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='load')
    @commands.is_owner()
    async def load_cog(self, ctx, cog_name: str):
        try:
            self.bot.load_extension(cog_name)
            await ctx.send(f'Cog "{cog_name}" has been loaded.')
        except Exception as e:
            await ctx.send(f'Error loading cog "{cog_name}": {e}')
    
    @commands.command(name='unload')
    @commands.is_owner()
    async def unload_cog(self, ctx, cog_name: str):
        try:
            self.bot.unload_extension(cog_name)
            await ctx.send(f'Cog "{cog_name}" has been unloaded.')
        except Exception as e:
            await ctx.send(f'Error unloading cog "{cog_name}": {e}')
    
    @commands.command(name='reload')
    @commands.is_owner()
    async def reload_cog(self, ctx, cog_name: str):
        try:
            self.bot.reload_extension(cog_name)
            await ctx.send(f'Cog "{cog_name}" has been reloaded.')
        except Exception as e:
            await ctx.send(f'Error reloading cog "{cog_name}": {e}')


async def setup(bot):
    await bot.add_cog(Owner(bot))
