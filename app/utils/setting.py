import discord
import os


data_folder = "./app/data"
os.makedirs(data_folder, exist_ok=True)
serversettings = os.path.join(data_folder, "serversettings.json")


def init():
    try:
        with open(serversettings, "r") as f:
            if f.read() == "":
                with open(serversettings, "w") as f:
                    f.write("{}")
    except FileNotFoundError:
        print("[!] serversettings.json not found. Attempting to create it now.")
        try:
            with open(serversettings, "w") as f:
                f.write("{}")
            print("[+] serversettings.json created successfully")
        except Exception as e:
            print("[!!] Error creating serversettings.json file. Check permissions on the folder.\n^-- Error: ", e)


def get_cogs():
    cogs = []
    for root, dirs, files in os.walk("app/cogs"):
        dirs[:] = [d for d in dirs if not d.startswith("!")]
        for file in files:
            if file.endswith(".py") and not file.startswith("!"):
                relative_path = os.path.relpath(os.path.join(root, file), "app")
                module_path = relative_path.replace(os.sep, ".")[:-3]  # حذف .py
                cogs.append(f"app.{module_path}")
    return cogs


intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.members = True
intents.presences = True
