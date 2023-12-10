import logging.config
import sys

import discord
from discord.ext import commands

from config import COGS, DISCORD_API_SECRET, LOGGING_CONFIG
from database import db_setup

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("dheads")


# Custom logging set up for critical errors
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, Exception):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

# Set up database
logger.info("Setting up Database")
db_setup()

# Initialize our bot. Commands are prefixed with '?'
bot = commands.Bot(
    command_prefix="?", description="An example bot", intents=discord.Intents.all()
)

if __name__ == "__main__":
    for extension in COGS:
        bot.load_extension(f"{extension}.cog")

bot.run(DISCORD_API_SECRET)
