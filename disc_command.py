import discord
import dataManip
client = discord.Client()

@client.tree.command()
async def db_to_json_command(interaction: discord.Interaction, type: str = "db_to_json"):
    #database = REFERENS TILL DATABASEN
    file = dataManip.db_to_json()#db_to_json(database, aw=True)
    message = "I converted the database to .json-format. Here is the file for you: "
    await interaction.channel.send(message)
    await interaction.channel.send(file=discord.File(file))

"""
def db_to_json(database, aw=False):
    if aw:
        # Find a way to convert the database to .json-format
        return discord.File("database.json")
    else:
        return "Error! Couldn't convert the database to .json-format."
"""