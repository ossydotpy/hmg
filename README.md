# About this project

The HMG Bot is a discord bot that's used for retrieving nft metadata for the Hermonsters project on cardano.

# How to run the app
1. Clone the repo
2. Get your bot keys from [here](https://discord.com/developers/)
3. create a `.env` file in the main directory. 
   copy and edit this variable
   
`BOT_TOKEN=your_bot_token`
   to run the bot.
edit other environmental variables if you want to use other fucntions that require them.
reference .env exmaple file for variable names
5. Run main.py
Make sure to invite the bot to your server!

# Customize the bot for your project.
You can do this by 
- change the policy ID in [this code](https://github.com/ossydotpy/hmg/blob/master/get_metadata.py)
- select your desired features using [this code](https://github.com/ossydotpy/hmg/blob/master/save_features.py)
- modify [this code](https://github.com/ossydotpy/hmg/blob/master/cogs/prio_cog.py) to search through your saved features.

- star this repo(haha, not required)
