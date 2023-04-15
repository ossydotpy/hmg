# About this project

The HMG Bot is a discord bot that's used for retrieving nft metadata for the Hermonsters project on cardano.

# How to run the app
1. Clone the repo
2. make sure to invite the bot to your server
3. run main.py

# Customize the bot for your project.
You can do this by 
- change the policy ID in [this code](https://github.com/ossydotpy/hmg/blob/master/get_metadata.py)
- select your desired features using [this code](https://github.com/ossydotpy/hmg/blob/master/save_features.py)
- modify the [search cog](https://github.com/ossydotpy/hmg/blob/master/cogs/nft_seach.py) to suit your features.
- star this repo(haha, not required)

# NOTE:
In this version, i've added a couple things
- separated the cogs into three
--one for each collection under the project.
- separated the save important metadata function into two files to help distiguish between the two types on nfts in the prio 360 drop.
