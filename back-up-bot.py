import discord
from discord.ext import commands

# Don't forget to change the messages and add your personality!

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required to fetch members and their roles

bot = commands.Bot(command_prefix="!", intents=intents)

# Function to load keys from a file
def load_keys(filename="keys.txt"):
    keys = []
    try:
        with open(filename, "r") as file:
            keys = [line.strip() for line in file if line.strip() and "- SENT to" not in line]
    except FileNotFoundError:
        print("Error: 'keys.txt' file not found.")
    return keys

# Load keys for distribution
keys = load_keys()

# Role names or IDs required
PRIMARY_ROLES = ["role 1", "role 2"]  # Roles where either can qualify
REQUIRED_ROLE = "Super Role"  # Role that is required along with any primary role

# List of User IDs to ignore (do not send keys to these users)
IGNORED_USER_IDS = []  # Replace with actual User IDs to ignore

@bot.event
async def on_ready():
    print(f'Bot is ready and logged in as {bot.user}')

# Command to distribute keys by DM to members with the required roles
@bot.command()
@commands.has_permissions(administrator=True)  # Only admins can use this command
async def distribute_keys(ctx):
    global keys

    if not keys:
        await ctx.send("No keys available.")
        return

    message_template = (
        "Input your message here!"
    )

    primary_role_ids = [role.id for role in ctx.guild.roles if role.name in PRIMARY_ROLES]
    required_role_id = next((role.id for role in ctx.guild.roles if role.name == REQUIRED_ROLE), None)

    if not required_role_id:
        await ctx.send(f"Required role '{REQUIRED_ROLE}' not found.")
        return

    # Find members with the required roles
    eligible_members = []
    for member in ctx.guild.members:
        # Check if member has the required role and one of the primary roles
        member_role_ids = {role.id for role in member.roles}
        if required_role_id in member_role_ids and any(role_id in member_role_ids for role_id in primary_role_ids):
            eligible_members.append(member)

    if not eligible_members:
        await ctx.send("No members found with the specified role requirements.")
        return

    # Send keys to eligible members and log sent keys with recipient details
    updated_keys = []
    for member in eligible_members:
        # Skip member if their user ID is in the ignored list
        if str(member.id) in IGNORED_USER_IDS:
            print(f"Skipping {member.display_name} ({member.id}) - Ignored")
            continue

        if not keys:
            await ctx.send("Ran out of keys before all users received one.")
            break

        key = keys.pop(0)  # Get the first available key
        personalized_message = f"{message_template}\nYour key: {key}"

        try:
            await member.send(personalized_message)
            print(f"Sent key to {member.display_name} ({member.id})")

            # Record the key as sent to the user in the updated list
            updated_keys.append(f"{key} - SENT to {member.display_name} ({member.id})")
        except Exception as e:
            print(f"Could not send DM to {member.display_name} ({member.id}): {e}")
            updated_keys.append(key)  # Retain unsent key in the list

    # Append remaining unsent keys to updated_keys
    updated_keys.extend(keys)

    # Save the updated keys back to the file with recipient info for sent keys
    with open("keys.txt", "w") as file:
        for k in updated_keys:
            file.write(f"{k}\n")

    await ctx.send("Keys have been sent to eligible users via DM.")
bot.run("somekey978withnumbersandstuff93891") #Bot Token
