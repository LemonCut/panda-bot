# bot.py
import discord
import config  # Your config.py file
import subprocess # Runs external scripts
import asyncio    # For non-blocking operations
import sys        # To find the correct python executable

# --- Setup the Bot ---
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Bot is online! Logged in as {client.user}')
    print('------')


# --- Helper Function to Run the Script ---
async def run_panda_survey(message, survey_code, email):
    """Runs the run_survey.py script as a subprocess."""
    
    await message.channel.send(
        f":panda_face: Got it! Running the survey for code: `{survey_code}`. I'll let you know when it's done..."
    )

    try:
        command = [
            sys.executable,
            'run_survey.py',
            survey_code,
            email
        ]

        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        if proc.returncode == 0:
            await message.channel.send(
                f":white_check_mark: **Success!** The survey is complete for `{email}`. The code has been sent."
            )
        else:
            # It failed! Decode the error to analyze it.
            stderr_decoded = stderr.decode()
            print(f"Script Error: {stderr_decoded}") # Log error to your terminal

            # --- THIS IS THE MODIFIED PART ---
            # Check for our specific, known error first.
            if "Survey code must be exactly 24 characters long" in stderr_decoded:
                await message.channel.send(
                    f":warning: **Invalid Code!** The survey code you provided is not the correct length. Please make sure it's 24 digits and try again."
                )
            else:
                # For any other unexpected errors, show the generic message.
                await message.channel.send(
                    f":x: **Error!** Something went wrong. The script failed.\n"
                    f"Error: ```{stderr_decoded}```"
                )

    except Exception as e:
        print(f"Bot Error: {e}")
        await message.channel.send(f":x: **Bot Error!** An unexpected error occurred in the bot itself: `{e}`")


# --- Event: When a message is sent ---
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send(':panda_face: Hello!')
        return

    if message.content.startswith('!panda'):
        parts = message.content.split()

        if len(parts) != 3:
            await message.channel.send(
                ":panda_face: Oops! Wrong format. Please use:\n`!panda <survey_code> <email>`"
            )
            return

        survey_code = parts[1]
        email = parts[2]
        
        asyncio.create_task(run_panda_survey(message, survey_code, email))
        return

# --- Run the Bot ---
try:
    client.run(config.DISCORD_TOKEN)
except discord.errors.LoginFailure:
    print("ERROR: Invalid Discord Token. Please check your config.py file.")
except Exception as e:
    print(f"An error occurred: {e}")