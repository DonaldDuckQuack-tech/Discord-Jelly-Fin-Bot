import discord
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
import math
import asyncio
import requests
import aiohttp
import random

# Replace with your bot's token
TOKEN = 'YOUR_BOT_TOKEN'
playall_active = False
song_list = []
queue_list = []
playing = False
data = []

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

# Define connection details
server_url = 'YOUR_JELLYFIN_SERVER_URL' # Replace with your Jellyfin server URL
api_key = 'YOUR_API_KEY'  # Your Jellyfin API key
download_urls = server_url + '/Items/<id>/Download?api_key=a82d70c04eb544a896a8120fdbf8dae2'  # Replace with your actual URL
custom_download_path = './cache/song_file.flac'  # Custom location to save the song
ffmpeg_path = r'H:\Program Files\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe'
ffmpeg_path_required = False

# Directory where the songs are stored
looping = False

async def plays(ctx, songe):
    global data
    if await song(songe):
        try:
            song_path = custom_download_path
            if ffmpeg_path_required == True:
                audio_source = FFmpegPCMAudio(
                    song_path,
                    executable=ffmpeg_path,
                    options='-filter:a "loudnorm=I=-16:TP=-1.5:LRA=11"',
                )
            else:
                audio_source = FFmpegPCMAudio(
                    song_path, options='-filter:a "loudnorm=I=-16:TP=-1.5:LRA=11"'
                )
            ctx.voice_client.play(audio_source, after=lambda e: print("done", e))
            return True
        except:
            await error(ctx, "Song Failed to play!")
            await ctx.voice_client.stop()
            return False
    return False

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# Function to get a list of songs in the directory
async def get_song_list():
    """Return a list of MP3 files in the song directory."""
    global song_list
    return song_list

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="List of available commands",
        color=discord.Color.dark_blue()
    )
    
    # Adding fields with inline=True creates the columns
    embed.add_field(name="!clearqueue", value="Command to clear the queue", inline=False)
    embed.add_field(name="!help", value="Shows this message", inline=False)
    embed.add_field(name="!instantmix", value="Command to add a instantmix to the queue", inline=False)
    embed.add_field(name="!join", value="Command to make the bot join the voice channel", inline=False)
    embed.add_field(name="!leave", value="Command to make the bot leave the voice channel", inline=False)
    embed.add_field(name="!loop", value="Command to loop a song", inline=False)
    embed.add_field(name="!play", value="Command to add a song to the queue", inline=False)
    embed.add_field(name="!playall", value="Command to play all the songs in the list one by one", inline=False)
    embed.add_field(name="!queue", value="Command to show what is currently in the queue", inline=False)
    embed.add_field(name="!randomplaylist", value="Command to add multiple songs to the queue based on album, artist or random song", inline=False)
    embed.add_field(name="!randomsong", value="Command to add a random song to the queue", inline=False)
    embed.add_field(name="!search", value="Command to search for songs based on the artist, album or song name", inline=False)
    embed.add_field(name="!skip", value="Command to skip the currently playing song", inline=False)
    embed.add_field(name="!songs", value="Command to list all the available songs", inline=False)
    embed.add_field(name="!stop", value="Command to stop any currently playing music", inline=False)
    embed.add_field(name="!updatesongs", value="Command to update the songs database for the bot", inline=False)
    embed.add_field(name="!version", value="Command to show the bot name and version", inline=False)
    
    await ctx.send(embed=embed)


# Regular command to join voice channel
@bot.command()
async def join(ctx):
    """Command to make the bot join the voice channel"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await success(ctx, f"Joined {channel.name}")
    else:
        await error(ctx, "You need to join a voice channel first!")


# Regular command to leave voice channel
@bot.command()
async def leave(ctx):
    """Command to make the bot leave the voice channel"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await success(ctx, "Disconnected from the voice channel")
    else:
        await error(ctx, "I'm not connected to a voice channel!")

# Regular command to leave voice channel
@bot.command()
async def ping(ctx):
    """Command to make the bot leave the voice channel"""
    await success(ctx, "Pong!")

# Command to play a song
@bot.command()
async def play(ctx, *, song_name = ""):
    """Command to add a song to the queue."""
    if not ctx.voice_client:
        # Make the bot join the channel
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await error(ctx, "You need to join a voice channel first!")
            return
    
    if song_name == "":
        await error(ctx, "You need to specifify a id!")
        return
    
    song_list = ""
    if " " in song_name:
        song_name = song_name.replace(" ", "")
        if "," in song_name:
            song_list = song_name.split(",")
    elif "," in song_name:
            song_list = song_name.split(",")
    else:
        song_list + song_name
    # Join the song name parts into a single string (in case it's multi-word)
    songs = await get_song_list()

    # Check if the song is in the available list
    selected = []
    songed_list = song_list
    for ii in songed_list[:]:
        for i in songs:
            song = i["Id"]
            if song.casefold() == ii.casefold():
                selected.append(i)
                print(song_list)
                print(ii)
                print(i)        
                song_list.remove(ii)
                if len(song_list) == 0:
                    break
        continue

    print("Selected: " + str(selected))
    print("Song_list: " + str(song_list))

    if len(selected) == 0:
        await error(ctx, f"Sorry, I can't find any of the song/songs provided. Please choose from !songs")
        return
    
    if len(song_list) >= 1:
        invalid = len(song_list)
        print(song_list)
        await error(ctx, f"Found {invalid} invalid song ids")

    await playqueue(ctx, selected)

async def embeded(ctx, status, songs):
    # Basic embed creation
    embed = discord.Embed(
        title=status,
        description=songs,
        color=discord.Color.dark_blue()
    )
    await ctx.send(embed = embed)

async def success(ctx, status):
    # Basic embed creation
    embed = discord.Embed(
        description=status,
        color=discord.Color.green()
    )
    await ctx.send(embed = embed)

async def errorr(ctx, status):
    await error(ctx, status)

async def error(ctx, status):
    # Basic embed creation
    embed = discord.Embed(
        title="Error!",
        description=status,
        color=discord.Color.red()
    )
    await ctx.send(embed = embed)

async def nowplayingEmbed(ctx, songe):
        song = await song2(songe)
        song_name = song.get('Name')
        album = song.get("Album")
        artists_array = song.get("Artists")
        artist = artists_array[0]
        albumId = song.get("AlbumId")
        albumart = f"https://jf.jmz10.com/Items/{albumId}/Images/Primary?width=256&height=256"
        presence = f"{song_name} by {artist}"
        nowplaying = f":musical_note: Now playing: {song_name}"
        desc = f"**Artist:** {artist}\n**Album:** {album}"
        embed = discord.Embed(title=nowplaying, description=desc, color=discord.Color.random())
        embed.set_thumbnail(url=albumart)
        server_name = ctx.guild.name
        channel_name = ctx.channel.name
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name=server_name + " " + channel_name,
            state=presence
        )
        await bot.change_presence(activity=activity)
        await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    # Check if the error is CommandNotFound
    if isinstance(error, commands.CommandNotFound):
        await errorr(ctx, "This command does not exist. Use !help for a list of commands.")
    else:
        # For other errors, raise them so they still show in the console
        await errorr(ctx, error)
        raise error
    
@bot.command()
async def version(ctx):
    # Check if the error is CommandNotFound
    await success(ctx, "Blaik Network JellyFin Music Bot Version: 2.9")

async def playqueue(ctx, song_name):
    global queue_list
    global playing
    songe = ""
    for i in song_name:
        artists_array = i.get("Artists")
        artist = artists_array[0]
        songe = f"{i.get('Name')} | **Artist:** {artist} | **Album:** {i.get('Album')} | **Id:** {i.get('Id')}"
        queue_list.append(songe)
    if playing == True:
        await success(ctx, f"{songe} added to Queue!")
    else:
        playing = True
        await success(ctx, f"{songe} added to Queue!")
        while playing:
            for i in range(len(queue_list)):
                song = queue_list[0]
                if await plays(ctx, song):
                    await nowplayingEmbed(ctx, song)
                else:
                    await error(ctx, f"Song '{song}' not found!")
                queue_list.remove(song)
                while ctx.voice_client.is_playing():
                    await asyncio.sleep(1)  #
                if not queue_list:
                    playing = False
                    await embeded(ctx, f"Queue is Empty", "Add more songs to continue playing!")
                    await ctx.voice_client.disconnect()
                    break
            if not queue_list:
                if playing:
                    playing = False
                    await embeded(ctx, f"Queue is Empty", "Add more songs to continue playing!")
                    await ctx.voice_client.disconnect()
                else:
                    continue


@bot.command()
async def randomsong(ctx):
    """Command to add a random song to the queue."""
    if not ctx.voice_client:
        # Make the bot join the channel
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await error(ctx, "You need to join a voice channel first!")
            return
    global playing
    if ctx.voice_client and ctx.voice_client.is_playing():
        if not playing:
            await error(ctx, "Could not play song, A song is currently playing")
            return

    # Join the song name parts into a single string (in case it's multi-word)
    songs = await get_song_list()
    integer = random.randint(1, len(songs))
    song = []
    song.append(songs[integer])
    await playqueue(ctx, song)


@bot.command()
async def queue(ctx, page=1):
    """Command to show what is currently in the queue."""
    global queue_list
    message = ""
    if queue_list != []:
        songs = queue_list
        page_size = 10
        start = (page - 1) * page_size
        end = start + page_size

        # Calculate the total number of pages
        total_pages = math.ceil(len(songs) / page_size)

        # If the page number is invalid, notify the user
        if page < 1 or page > total_pages:
            await error(ctx, f"Invalid page number. Please choose a page between 1 and {total_pages}.")
            return

        # Get the songs for the current page
        page_songs = songs[start:end]
        correct_page_songs = []

        for song in page_songs:
            songed = f"{song} \n"
            correct_page_songs.append(songed)

        # Create the message for the page
        message = "".join(correct_page_songs)

        # Send the message to the channel
        await embeded(ctx, f"**Page {page}/{total_pages}, The following songs are in the queue!:**", message)
    else:
        await error(ctx, f"The Queue is empty!")


@bot.command()
async def clearqueue(ctx):
    """Command to clear the queue"""
    global queue_list
    if queue_list != []:
        queue_list.clear()
        await success(ctx, f"The Queue has been cleared!")
    else:
        await error(ctx, f"There is nothing in the Queue!")


@bot.command()
async def stop(ctx):
    """Command to stop any currently playing music."""
    # Autocompletion for the song argument in play command
    global playall_active
    global looping
    global queue_list
    queue_list = []
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # Stop the current song
        if playall_active == True:
            playall_active = False
            await success(ctx, "The playall queue has been stopped.")
        elif looping == True:
            looping = False
            await success(ctx, "The loop has been stopped.")
        else:
            global playing
            playing = False
            await success(ctx, "Stopped the current song.")
    else:
        await error(ctx, "No audio is currently playing.")

    # If playall is active, stop it as well


@bot.command()
async def randomplaylist(ctx, *keywords: str):
    """Command to add multiple songs to the queue based on album, artist or random songs."""
    if not ctx.voice_client:
        # Make the bot join the channel
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await error(ctx, "You need to join a voice channel first!")
            return
    global playing
    if ctx.voice_client and ctx.voice_client.is_playing():
        if not playing:
            await error(ctx, "Could not play song, A song is currently playing")
            return

    if keywords:
        try:
            # Try to cast the last keyword to an integer
            count = int(keywords[-1])
            # If it's valid, remove it from the keywords
            keywords = keywords[:-1]
        except ValueError:
            # If the last keyword is not a number, default page to 1
            count = 10
    else:
        count = 10

    if count < 10001:
        # Join the song name parts into a single string (in case it's multi-word)
        song = []
        songss = await get_song_list()
        songs = []
        for songd in songss:
            if keywords:
                keyword = keywords[1:]
                search_query = " ".join(keyword).lower()
                search_query = str(search_query)
                if keywords[0].lower() == "album:":
                    songe = []
                    songe.append(songd)
                    songeee = songe[0]
                    if search_query.casefold() == songeee["Album"].casefold():
                        songs.append(songd)
                elif keywords[0].lower() == "artist:":
                    songe = []
                    songe.append(songd)
                    songeee = songe[0]
                    for songee in songeee["Artists"]:
                        if search_query.casefold() == songee.casefold():
                            songs.append(songd)
            else:
                songs.append(songd)

        if songs:
            for i in range(count):
                integer = random.randint(0, len(songs) - 1)
                song.append(songs[integer])
            await playqueue(ctx, song)
        else:
            await error(ctx, "No Songs were found!")

    else:
        await error(ctx, "You can only add 10,000 songs at a time!")


@bot.command()
async def skip(ctx):
    """Command to skip the currently playing song."""
    global playall_active
    global playing
    queue_list
    if ctx.voice_client and ctx.voice_client.is_playing():
        if playall_active:  # Check if playall is active
            ctx.voice_client.stop()  # Stop the current song
            await success(ctx, "Song Skipped!")
        elif playing:  # Check if playall is active
            ctx.voice_client.stop()  # Stop the current song
            await success(ctx, "Song Skipped!")
        else:
            await error(ctx, "Playall queue or Play queue is not active.")
    else:
        await error(ctx, "No audio is currently playing.")


# Autocompletion for the song argument in play command
@bot.command()
async def songs(ctx, page: int = 1):
    """Command to list all available songs, paginated by 10 songs per page."""

    # Calculate the start and end index for the requested page
    songs = await get_song_list()
    page_size = 10
    start = (page - 1) * page_size
    end = start + page_size

    # Calculate the total number of pages
    total_pages = math.ceil(len(songs) / page_size)

    # If the page number is invalid, notify the user
    if page < 1 or page > total_pages:
        await error(ctx, 
            f"Invalid page number. Please choose a page between 1 and {total_pages}."
        )
        return

    # Get the songs for the current page
    page_songs = songs[start:end]
    correct_page_songs = []

    for song in page_songs:
        songed = f"{song.get('Name')} | Artist: {song.get('Artists')} | Album: {song.get('Album')} | Id: {song.get('Id')} \n"
        correct_page_songs.append(songed)

    # Create the message for the page
    message = "".join(correct_page_songs)

    # Send the message to the channel
    await embeded(ctx, f"**Page {page}/{total_pages}**", message)


@bot.command()
async def playall(ctx):
    """Command to play all songs in the list one by one"""

    # Check if the bot is currently playing audio
    if ctx.voice_client and ctx.voice_client.is_playing():
        await error(ctx, "Could not play all songs, A song is currently playing")
        return

    # Check if the bot is connected to a voice channel
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await error(ctx, "You need to join a voice channel first!")
            return

    songs = await get_song_list()
    global playall_active
    playall_active = True

    # Loop through each song and play it
    for song_name in songs:
        if not playall_active:  # Check if playall_active is False to break the loop
            break

        Artists = song_name.get("Artists")
        Artist = Artists[0]
        songe = f"{song_name.get('Name')} | **Artist:** {Artist} | **Album:** {song_name.get('Album')} | **Id:** {song_name.get('Id')}"

        if await plays(ctx, songe):
            await nowplayingEmbed(ctx, songe)
        else:
            await error(ctx, f"Song '{songe}' not found!")

        # Wait for the song to finish before moving to the next one
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)  # Wait until the song finishes

    await success(ctx, "All songs have been played.")
    await ctx.voice_client.disconnect()


@bot.command()
async def loop(ctx, *, song_name = " "):
    """Command to play loop a song from the list."""

    # Check if the bot is currently playing audio
    if ctx.voice_client and ctx.voice_client.is_playing():
        await error(ctx, "Could not loop song, A song is currently playing")
        return

    # Check if the bot is connected to a voice channel
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await error(ctx, "You need to join a voice channel first!")
            return
        
    if song_name == "":
        await error(ctx, "You need to specifify a id!")
        return

    # Join the song name parts into a single string (in case it's multi-word)
    global looping
    looping = True

    # Check if the song is in the available list
    songs = await get_song_list()
    selected = []
    for i in songs:
        song = i["Id"]
        if song.casefold() == song_name:
            selected.append(i)
            break
        else:
            continue
    else:
        await error(
            ctx, f"Sorry, I can't find a song with id '{song_name}'. Please choose from !songs"
        )
        return

    song = selected[0]
    # Play the song using FFmpeg
    while looping:
        await asyncio.sleep(1)
        if not looping:  # Check if playall_active is False to break the loop
            break

        Artists = song.get("Artists")
        Artist = Artists[0]
        songe = f"{song.get('Name')} | **Artist:** {Artist} | **Album:** {song.get('Album')} | **Id:** {song.get('Id')}"

        if await plays(ctx, songe):
            await nowplayingEmbed(ctx, songe)
        else:
            looping = False
            await error(ctx, f"Song '{song_name}' not found!")

        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)  # Wait until the song finishes


@bot.command()
async def search(ctx, *keywords: str):
    """Command to search for songs based on the artist, album or song name."""
    if not keywords:
        await error(ctx, "Please provide some keywords to search for.")
        return

    # Join the keywords into a single search string
    try:
        # Try to cast the last keyword to an integer
        page = int(keywords[-1])
        # If it's valid, remove it from the keywords
        keywords = keywords[:-1]
    except ValueError:
        # If the last keyword is not a number, default page to 1
        page = 1

    search_query = " ".join(keywords).lower()
    search_query = str(search_query)

    # Fetch all the MP3 files in the SONG_DIR
    song_list = await get_song_list()

    # Filter the song list to find matches
    matching_songs = []
    if keywords[0].lower() == "album:":
        search_query = search_query.replace("album: ", "")
        for song in song_list:
            if search_query.lower() == song["Album"].lower():
                match = str(song["Name"] + " | Id: " + song["Id"] + "\n")
                matching_songs.append(match)
    elif keywords[0].lower() == "artist:":
        search_query = search_query.replace("artist: ", "")
        for song in song_list:
            for songe in song["Artists"]:
                if search_query == songe.lower():
                    match = str(song["Name"] + " | Id: " + song["Id"] + "\n")
                    matching_songs.append(match)
    else:
        for song in song_list:
            if search_query == song["Name"].lower():
                match = str(song["Name"] + " | Id: " + song["Id"] + "\n")
                matching_songs.append(match)

    if matching_songs:
        # If there are matches, send them to the user
        songs = matching_songs
        page_size = 20
        start = (page - 1) * page_size
        end = start + page_size

        # Calculate the total number of pages
        total_pages = math.ceil(len(songs) / page_size)

        # If the page number is invalid, notify the user
        if page < 1 or page > total_pages:
            await error(
                ctx, f"Invalid page number. Please choose a page between 1 and {total_pages}."
            )
            return

        # Get the songs for the current page
        page_songs = songs[start:end]

        # Create the message for the page
        message = "".join(page_songs)

        # Send the message to the channel
        await embeded(ctx, f"**Page {page}/{total_pages}, Found the following songs matching '{search_query}':**", message)
    else:
        await error(ctx, f"No songs found matching '{search_query}'.")


@bot.command()
async def updatesongs(ctx):
    """Command to update the songs database for the bot."""
    if getsongs():
        await success(ctx, f"Song database updated successfully.")
    else:
        await error(ctx, f"Error updating song database.")


@bot.command()
async def instantmix(ctx, id = "", limit=15):
    """Command to add a instant mix to the queue."""
    # Check if the bot is currently playing audio

    # Check if the bot is connected to a voice channel
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await error(ctx, "You need to join a voice channel first!")
            return
        
    if id == "":
        await error(ctx, "You need to specifify a id!")
        return

    await success(ctx, f"Getting an Instant Mix from JellyFin server!")
    try:
        songs = await getinstantmix(id, limit)
        if songs:
            await success(ctx, f"Instant Mix retrieved from JellyFin server!")
        await playqueue(ctx, songs)
        return
    except:
        await error(ctx, f"Could not Retrieve Instant Mix from JellyFin server!")


async def getinstantmix(id, limit):
    url = f"{server_url}/Items/{id}/InstantMix"

    params = {"limit": limit, "api_key": api_key}  # Provide API key

    # Send GET request to Jellyfin API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        songedd = []
        data = response.json()

        # Print song details
        for song in data["Items"]:
            artistlist = ""
            artists = song.get("Artists", [])
            if artists:
                artistlist = artists
            else:
                artistlist = "Unknown Artist"  # Fallback if no artists found
            album = ""
            albums = song.get("Album", [])
            albumId = song.get("AlbumId")
            if albums:
                album = albums
            else:
                album = "Unknown Album"
            songs = {
                "Name": song["Name"],
                "Artists": artistlist,  # List of artists
                "Album": album,  # Assuming album info is available
                "AlbumId": albumId,
                "Id": song["Id"],
            }

            songedd.append(songs)
        return songedd
    else:
        print(f"Error: {response.status_code} - {response.text}")


def getsongs():
    global song_list
    global data
    songs_list = []
    songed, data = songs()
    songs_list = songed
    for song in songs_list:
        song_list.append(song)
    return True


def songs():

    # API endpoint to get all songs
    url = f"{server_url}/Items"

    # Request parameters to filter audio items and sort by name
    params = {
        "Recursive": "true",  # Fetch items recursively (including albums, etc.)
        "IncludeItemTypes": "Audio",  # Only fetch audio items (songs)
        "SortBy": "SortName",  # Sort by name
        "api_key": api_key,  # Provide API key
    }

    # Send GET request to Jellyfin API
    response = requests.get(url, params=params)

    if response.status_code == 200:
        songed = []
        data = response.json()

        # Print song details
        for song in data["Items"]:
            artistlist = ""
            artists = song.get("Artists", [])
            if artists:
                artistlist = artists
            else:
                artistlist = "Unknown Artist"  # Fallback if no artists found
            album = ""
            albums = song.get("Album", [])
            albumId = song.get("AlbumId")
            if albums:
                album = albums
            else:
                album = "Unknown Album"
            songs = {
                "Name": song["Name"],
                "Artists": artistlist,  # List of artists
                "Album": album,  # Assuming album info is available
                "AlbumId": albumId,
                "Id": song["Id"],
            }

            songed.append(songs)
        return songed, data
    else:
        print(f"Error: {response.status_code} - {response.text}")


async def download(song_id):
    url = download_urls.replace("<id>", song_id)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:  # Check if the response is OK
                    with open(custom_download_path, "wb") as f:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            f.write(chunk)
                    print(f"File {song_id}.flac downloaded successfully.")
                else:
                    print(
                        f"Failed to download {song_id}. Status code: {response.status}"
                    )
        except aiohttp.ClientError as e:
            print(f"An error occurred while downloading {song_id}: {e}")
        else:
            # This will execute if the download was successful and the response status was 200
            print(f"Download of song {song_id} completed without any exceptions.")


async def song(songed):
    song_list = await get_song_list()
    for song in song_list:
        Artists = song.get("Artists")
        Artist = Artists[0]
        songe = f"{song.get('Name')} | **Artist:** {Artist} | **Album:** {song.get('Album')} | **Id:** {song.get('Id')}"
        if songe == songed:
            print("The id is: " + song["Id"])
            await download(song["Id"])
            return True

    print("Song: " + str(songed) + " not found")
    return False

async def song2(songed):
    song_list = await get_song_list()
    for song in song_list:
        Artists = song.get("Artists")
        Artist = Artists[0]
        songe = f"{song.get('Name')} | **Artist:** {Artist} | **Album:** {song.get('Album')} | **Id:** {song.get('Id')}"
        if songe == songed:   
            return song

    print("Song: " + str(songed) + " not found")
    return False


# Run the bot
print("Getting songs database from jellyfin server...")
getsongs()
print("Downloaded. Starting bot...")
bot.run(TOKEN)
