import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from ddgs import DDGS

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()


bot = MyBot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="fetch", description="Search the web")
@app_commands.describe(query="What do you want to search for?")
async def fetch(interaction: discord.Interaction, query: str):

    await interaction.response.defer()

    try:
        results = DDGS().text(query, max_results=5)

        if not results:
            await interaction.followup.send("❌ Couldn't find anything.")
            return

        message = f"🔎 **Results for:** `{query}`\n\n"

        for i, result in enumerate(results, 1):
            title = result.get("title", "No title")
            url = result.get("href", "")
            snippet = result.get("body", "")

            message += f"**{i}. {title}**\n"
            message += f"{snippet[:300]}\n"
            message += f"{url}\n\n"

        await interaction.followup.send(message[:2000])

    except Exception as e:
        await interaction.followup.send(f"❌ Error: `{e}`")


bot.run(TOKEN)