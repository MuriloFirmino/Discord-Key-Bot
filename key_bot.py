import discord
from discord.ext import commands
import requests

# Initialize the bot with a command prefix, e.g., "!"
client = discord.Client(intents=discord.Intents.default())
bot = commands.Bot(command_prefix="/")

# Load keys from a text file into a list
def load_keys(filename="keys.txt"):
    try:
        with open(filename, "r") as file:
            keys = [line.strip() for line in file if line.strip()]
        return keys
    except FileNotFoundError:
        print("Error: 'keys.txt' file not found.")
        return []

keys = load_keys()  # Load keys initially

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Command to send a key to a specified user
@bot.command()
@commands.has_permissions(administrator=True)  # Only admins can use this command
async def send_key(ctx, user: discord.User):
    global keys
    if not keys:
        await ctx.send("No more keys available.")
        return

    key = keys.pop(0)  # Get the first key from the list
    try:
        await user.send(f"Here is your key: {key}")
        await ctx.send(f"Key sent to {user.name}.")

        # Save the updated keys list back to the file
        with open("keys.txt", "w") as file:
            for k in keys:
                file.write(f"{k}\n")

    except discord.Forbidden:
        await ctx.send(f"Could not send a DM to {user.name}. They may have DMs disabled.")

# Run the bot with your token
bot.run("e8fcf7b6e520cc26cbf8188c927a2b2edc0d6c8e9440993bbc7d7e9515726d84")

#580945866419328 - permission integer
#https://discord.com/oauth2/authorize?client_id=1305410445175296120&permissions=8&integration_type=0&scope=bot
