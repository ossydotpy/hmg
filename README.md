# About this project
This is a discord bot for the Hermonsters NFT project on cardano.

its used for querying the nft metadata in discord.
can display 
- onchain metadata
- floor price
- holder distribution
- NFT trait floor

Note: this is specifically set u for [Hermonsters](https://hermonsters.com)\
contact or modify the code to suit your needs for a specific project\

# setup instructions
 - Clone the repo
 - Get your discord bot keys [here](https://discord.com/developers/)
 - Get your Blockfrost Api Key [here](https://blockfrost.io/)
 - create a `.env` file in the main directory. 
   In the `.env` file copy, paste and edit the following code.
   ```
   BOT_TOKEN=your_bot_token
   BLOCKFROST_API_KEY=your api key here


   add all other private information in ths file
   they can be called with `os.getenv(VARIABLENAME)` anywhere.
   ```
 - Start the discord bot by running `python main.py`
 - Invite your bot to your server.
 - use `~sync` on first launch to sync the commands to your server.

 - Star this repo [optional]
