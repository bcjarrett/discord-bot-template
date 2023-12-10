import logging
import random

import discord
from discord.ext import commands, tasks
from peewee import IntegrityError

from config import BOT_STATUS
from example.models import LastResponse
from example.util import populous_channel

# Initializing logger
logger = logging.getLogger(__name__)


class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def reply_to_message(self, message, response="Example Response"):
        """Respond to a message and log the message"""
        try:
            LastResponse.create(text=message.content, user_id=message.author.id)
        except IntegrityError as e:
            print(f"Error logging message: {e}")

        await message.channel.send(response)

    @commands.command(aliases=["random"])
    async def random_user(self, ctx):
        """Selects a random user from the most populous voice channel"""
        voice_channel = ctx.bot.get_channel(populous_channel(ctx))
        members = list(voice_channel.members)
        chosen = random.choice(members)
        snd = chosen.nick if chosen.nick else chosen
        await ctx.send(snd)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Reply to a random message 5% of the time"""
        if message.author != self.bot.user:
            if random.randint(0, 50) == 20:
                await self.reply_to_message(message)

    @tasks.loop(seconds=10)
    async def update_status(self):
        """Update the bot's status every 10 seconds with a random status from the config file"""
        await self.bot.change_presence(
            activity=discord.Game(name=random.choice(BOT_STATUS))
        )

    @update_status.before_loop
    async def before_printer(self):
        """Ensure the bot is ready before we start our update_status loop"""
        await self.bot.wait_until_ready()

    @commands.Cog.listener()
    async def on_ready(self):
        """Log some startup info when the bot is ready"""
        logger.info("Logged in as: %s - %s", self.bot.user.name, self.bot.user.id)
        logger.info("Version: %s", discord.__version__)
        logger.info("Connected to %s", [g.name for g in self.bot.guilds])


# Must include this line in all cogs so they are loaded
def setup(bot):
    bot.add_cog(ExampleCog(bot))
