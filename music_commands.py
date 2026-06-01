import asyncio
import math
import random
import helpers


player = None
bot = None

def setup(bott, music_player):
    global bot, player
    bot = bott
    player = music_player
    helpers.setup(bott, music_player)

async def skip():
    """Command to skip the currently playing song."""
    if player.channel and player.channel.is_playing():
        if player.playall_active:  # Check if playall is active
            player.channel.stop()  # Stop the current song
            await helpers.success("Song Skipped!")
            return ("Song Skipped!")
        elif player.playing:  # Check if playall is active
            player.channel.stop()  # Stop the current song
            await helpers.success("Song Skipped!")
            return ("Song Skipped!")
        else:
            await helpers.error("Playall queue or Play queue is not active.")
            return ("Playall queue or Play queue is not active.")
    else:
        await helpers.error("No audio is currently playing.")
        return ("No audio is currently playing.")
    

async def play(song_name):

    if not song_name:
        await helpers.error("You need to specify an id!")
        return

    song_list = []

    song_name = song_name.replace(" ", "")

    if "," in song_name:
        song_list = song_name.split(",")
    else:
        song_list.append(song_name)

    songs = await helpers.get_song_list()

    selected = []

    for requested_id in song_list[:]:
        for song in songs:
            if song["Id"].casefold() == requested_id.casefold():
                selected.append(song)
                song_list.remove(requested_id)
                break

    if not selected:
        await helpers.error(
            "Sorry, I can't find any of the songs provided. Please choose from !songs"
        )
        return

    if song_list:
        await helpers.error(f"Found {len(song_list)} invalid song ids")

    result = await helpers.playqueue(selected)

    return result
    

async def leave():
    """Command to make the bot leave the voice channel"""
    if player.channel:
        player.channel.disconnect()
        await helpers.success("Disconnected from the voice channel")
    else:
        await helpers.error("I'm not connected to a voice channel!")


async def ping():
    """Command to make the bot leave the voice channel"""
    await helpers.success("Pong!")




async def playnext(song_name):
    """Command to add a song to the queue."""    
    
    if not song_name:
        await helpers.error("You need to specifify a id!")
        return
    
    if not player.queue_list:
        await helpers.error("The queue is currently Empty.")
        return

    song_list = ""
    if " " in song_name:
        song_name = song_name.replace(" ", "")
        if "," in song_name:
            song_list = song_name.split(",")
    elif "," in song_name:
            song_list = song_name.split(",")
    else:
        song_list = []
        song_list.append(song_name)
    # Join the song name parts into a single string (in case it's multi-word)
    songs = await helpers.get_song_list()

    # Check if the song is in the available list

    selected = []
    songed_list = song_list
    for ii in songed_list[:]:
        for i in songs:
            song = i["Id"]
            if song.casefold() == ii.casefold():
                selected.append(i)       
                song_list.remove(ii)
                if len(song_list) == 0:
                    break
        


    if len(selected) == 0:
        await helpers.error(f"Sorry, I can't find any of the song/songs provided. Please choose from !songs")
        return
    
    if len(song_list) >= 1:
        invalid = len(song_list)
        await helpers.error(f"Found {invalid} invalid song ids")

    list = player.queue_list[:]
    player.queue_list.clear()
    for i in selected:
        artists_array = i.get("Artists")
        artist = artists_array[0]
        songe = f"{i.get('Name')} | **Artist:** {artist} | **Album:** {i.get('Album')} | **Id:** {i.get('Id')}"
        player.queue_list.append(songe)
    for ii in list:
        player.queue_list.append(ii)
    
    await helpers.success("The " + str(len(selected)) + " id/s provided will play next in the queue!")


async def playnow(song_name):
    """Command to add a song to the queue."""
        
    if not song_name:
        await helpers.error("You need to specifify an id!")
        return
    
    if not player.queue_list:
        await helpers.error("The queue is currently Empty.")
        return
    
    song_list = ""
    if " " in song_name:
        song_name = song_name.replace(" ", "")
        if "," in song_name:
            song_list = song_name.split(",")
    elif "," in song_name:
            song_list = song_name.split(",")
    else:
        song_list = []
        song_list.append(song_name)
    # Join the song name parts into a single string (in case it's multi-word)
    songs = await helpers.get_song_list()

    # Check if the song is in the available list

    selected = []
    songed_list = song_list
    for ii in songed_list[:]:
        for i in songs:
            song = i["Id"]
            if song.casefold() == ii.casefold():
                selected.append(i)       
                song_list.remove(ii)
                if len(song_list) == 0:
                    break
        


    if len(selected) == 0:
        await helpers.error(f"Sorry, I can't find any of the song/songs provided. Please choose from !songs")
        return
    
    if len(song_list) >= 1:
        invalid = len(song_list)
        await helpers.error(f"Found {invalid} invalid song ids")

    list = player.queue_list[:]
    player.queue_list.clear()
    for i in selected:
        artists_array = i.get("Artists")
        artist = artists_array[0]
        songe = f"{i.get('Name')} | **Artist:** {artist} | **Album:** {i.get('Album')} | **Id:** {i.get('Id')}"
        player.queue_list.append(songe)
    for ii in list:
        player.queue_list.append(ii)
    
    player.channel.stop()
    await helpers.success("The " + str(len(selected)) + " id/s provided will play now/next in the queue!")


async def pause():
    
    if  player.channel and (player.channel.is_playing() or player.channel.is_paused()):
        player.channel.pause()
        await helpers.success("Playback has been paused!")
    else:
        await helpers.error("Nothing to Pause!")


async def resume():
    
    if player.channel and (player.channel.is_playing() or player.channel.is_paused()):
        player.channel.resume()
        await helpers.success("Playback has been resumed!")
    else:
        await helpers.error("Nothing to resume!")


async def remove( *, song_name = ""):
    """Command to add a song to the queue."""
    
    if song_name == "":
        await helpers.error("You need to specifify an id!")
        return
    
    if not player.queue_list:
        await helpers.error("The queue is currently Empty.")
        return
    
    song_list = ""
    if " " in song_name:
        song_name = song_name.replace(" ", "")
        if "," in song_name:
            song_list = song_name.split(",")
    elif "," in song_name:
            song_list = song_name.split(",")
    else:
        song_list = []
        song_list.append(song_name)
    # Join the song name parts into a single string (in case it's multi-word)
    songs = await helpers.get_song_list()

    # Check if the song is in the available list

    selected = []
    songed_list = song_list
    for ii in songed_list[:]:
        for i in songs:
            song = i["Id"]
            if song.casefold() == ii.casefold():
                selected.append(i)       
                song_list.remove(ii)
                if len(song_list) == 0:
                    break
        


    if len(selected) == 0:
        await helpers.error(f"Sorry, I can't find any of the song/songs provided. Please choose from !songs")
        return
    
    if len(song_list) >= 1:
        invalid = len(song_list)
        await helpers.error(f"Found {invalid} invalid song ids")

    for i in selected:
        for ii in player.queue_list[:]:
            artists_array = i.get("Artists")
            artist = artists_array[0]
            songe = f"{i.get('Name')} | **Artist:** {artist} | **Album:** {i.get('Album')} | **Id:** {i.get('Id')}"
            if ii == songe:
                player.queue_list.remove(songe)

    await helpers.success("Removed " + str(len(selected)) + " ids from the Queue!")


async def version():
    # Check if the error is CommandNotFound
    await helpers.success("Blaik Network JellyFin Music Bot Version: 3.0")


async def randomsong():
    print ("getting random song...")
    """Command to add a random song to the queue."""    
    try:
        songs = await helpers.get_song_list()
        print("fetched songlist..")
        integer = random.randint(0, len(songs) - 1)
        song = []
        song.append(songs[integer])
        await helpers.playqueue(song)
        print("played song...")
    except Exception as e:
        print(f"randomerror: {e}")


async def queue( page=1):
    """Command to show what is currently in the queue."""
    
    message = ""
    if player.queue_list != []:
        songs = player.queue_list
        page_size = 10
        start = (page - 1) * page_size
        end = start + page_size

        # Calculate the total number of pages
        total_pages = math.ceil(len(songs) / page_size)

        # If the page number is invalid, notify the user
        if page < 1 or page > total_pages:
            await helpers.error(f"Invalid page number. Please choose a page between 1 and {total_pages}.")
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
        await helpers.embeded(f"**Page {page}/{total_pages}, The following songs are in the queue!:**", message)
    else:
        await helpers.error(f"The Queue is empty!")



async def clearqueue():
    if player.queue_list:
        player.queue_list.clear()
        await helpers.success("The Queue has been cleared!")
        return {"success": "The Queue has been cleared!"}
    else:
        await helpers.error("There is nothing in the Queue!")
        return {"error": "There is nothing in the Queue!"}


async def stop():
    """Command to stop any currently playing music."""
    voice = player.channel
    print("stop command executing...")
    try:
        if voice and (voice.is_playing() or voice.is_paused()):
            if player.playall_active:
                player.playall_active = False
                await helpers.success("The playall queue has been stopped.")
            elif player.looping:
                player.looping = False
                await helpers.success("The loop has been stopped.")
            else:
                player.playing = False
                await helpers.success("Stopped the current song.")
            player.queue_list = []
            voice.stop()
        else:
            await helpers.error("No audio is currently playing.")
    except Exception as e:
        print(f"Error occurred while executing stop: {e}")

    # If playall is active, stop it as well



async def randomplaylist( keywords: str):
    """Command to add multiple songs to the queue based on album, artist or random songs."""

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
        songss = await helpers.get_song_list()
        songs = []
        for songd in songss:
            if keywords:
                keyword = keywords[1:]
                search_query = " ".join(keyword).lower()
                search_query = str(search_query)
                if keywords[0].casefold() == "album:":
                    songe = []
                    songe.append(songd)
                    songeee = songe[0]
                    if search_query.casefold() in songeee["Album"].casefold():
                        songs.append(songd)
                elif keywords[0].lower() == "artist:":
                    songe = []
                    songe.append(songd)
                    songeee = songe[0]
                    for songee in songeee["Artists"]:
                        if search_query.casefold() in songee.casefold():
                            songs.append(songd)
            else:
                songs.append(songd)

        if songs:
            for i in range(count):
                integer = random.randint(0, len(songs) - 1)
                song.append(songs[integer])
            await helpers.playqueue(song)
        else:
            await helpers.error("No Songs were found!")

    else:
        await helpers.error("You can only add 10,000 songs at a time!")



async def songs( page: int = 1):
    """Command to list all available songs, paginated by 10 songs per page."""

    # Calculate the start and end index for the requested page
    songs = await helpers.get_song_list()
    page_size = 10
    start = (page - 1) * page_size
    end = start + page_size

    # Calculate the total number of pages
    total_pages = math.ceil(len(songs) / page_size)

    # If the page number is invalid, notify the user
    if page < 1 or page > total_pages:
        await helpers.error(f"Invalid page number. Please choose a page between 1 and {total_pages}.")
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
    await helpers.embeded(f"**Page {page}/{total_pages}**", message)



async def playall():
    """Command to play all songs in the list one by one"""
    # Check if the bot is currently playing audio
    if player.channel and (player.channel.is_playing() or player.channel.is_paused()):
        await helpers.error(f"{player.channel}, Could not play all songs, A song is currently playing")
        return

    songs = await helpers.get_song_list()
    
    player.playall_active = True

    # Loop through each song and play it
    for song_name in songs:
        if not player.playall_active:  # Check if playall_active is False to break the loop
            break

        Artists = song_name.get("Artists")
        Artist = Artists[0]
        songe = f"{song_name.get('Name')} | **Artist:** {Artist} | **Album:** {song_name.get('Album')} | **Id:** {song_name.get('Id')}"

        if await helpers.plays(songe):
            await helpers.nowplayingEmbed(songe)
        else:
            await helpers.error(f"Song '{songe}' not found!")

        # Wait for the song to finish before moving to the next one
        while player.channel.is_playing():
            await asyncio.sleep(1)  # Wait until the song finishes

    await helpers.success("All songs have been played.")
    await player.channel.disconnect()



async def loop(song_name = ""):
    """Command to play loop a song from the list."""
    print("looping...")
    # Check if the bot is currently playing audio
    if player.channel and (player.channel.is_playing() or player.channel.is_paused()):
        await helpers.error("Could not loop song, A song is currently playing")
        return

        
    if song_name == "":
        print("song_name = ''")
        await helpers.error("You need to specifify a id!")
        return

    # Join the song name parts into a single string (in case it's multi-word)
    
    player.looping = True

    # Check if the song is in the available list
    songs = await helpers.get_song_list()
    selected = []
    for i in songs:
        song = i["Id"]
        if song.casefold() == song_name:
            selected.append(i)
            break
        else:
            continue
    else:
        await helpers.error(
            f"Sorry, I can't find a song with id '{song_name}'. Please choose from !songs"
        )
        return

    song = selected[0]
    # Play the song using FFmpeg
    while player.looping:
        await asyncio.sleep(1)
        if not player.looping:  # Check if playall_active is False to break the loop
            break

        Artists = song.get("Artists")
        Artist = Artists[0]
        songe = f"{song.get('Name')} | **Artist:** {Artist} | **Album:** {song.get('Album')} | **Id:** {song.get('Id')}"

        if await helpers.plays(songe):
            await helpers.nowplayingEmbed(songe)
        else:
            player.looping = False
            await helpers.error(f"Song '{song_name}' not found!")

        while player.channel.is_playing():
            await asyncio.sleep(1)  # Wait until the song finishes



async def search( keywords):
    """Command to search for songs based on the artist, album or song name."""
    if not keywords:
        await helpers.error("Please provide some keywords to search for.")
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
    song_list = await helpers.get_song_list()

    # Filter the song list to find matches
    matching_songs = []
    if keywords[0].lower() == "album:":
        search_query = search_query.replace("album: ", "")
        for song in song_list:
            if search_query.casefold() in song["Album"].casefold():
                match = str(song["Name"] + " | Id: " + song["Id"] + "\n")
                matching_songs.append(match)
    elif keywords[0].lower() == "artist:":
        search_query = search_query.replace("artist: ", "")
        for song in song_list:
            for songe in song["Artists"]:
                if search_query.casefold() in songe.casefold():
                    match = str(song["Name"] + " | Id: " + song["Id"] + "\n")
                    matching_songs.append(match)
    else:
        for song in song_list:
            if search_query.casefold() in song["Name"].casefold():
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
            await helpers.error(
                f"Invalid page number. Please choose a page between 1 and {total_pages}."
            )
            return

        # Get the songs for the current page
        page_songs = songs[start:end]

        # Create the message for the page
        message = "".join(page_songs)

        # Send the message to the channel
        await helpers.embeded(f"**Page {page}/{total_pages}, Found the following songs matching '{search_query}':**", message)
    else:
        await helpers.error(f"No songs found matching '{search_query}'.")



async def updatesongs():
    """Command to update the songs database for the bot."""
    if helpers.getsongs():
        await helpers.success(f"Song database updated successfully.")
    else:
        await helpers.error(f"Error updating song database.")




async def instantmix(id = "", limit=15):
    """Command to add an instant mix to the queue."""
    # Check if the bot is currently playing audio

        
    if id == "":
        await helpers.error("You need to specifify an id!")
        return

    await helpers.success(f"Getting an Instant Mix from JellyFin server!")
    try:
        songs = await helpers.getinstantmix(id, limit)
        if songs:
            await helpers.success(f"Instant Mix retrieved from JellyFin server!")
        await helpers.playqueue(songs)
        return
    except:
        await helpers.error(f"Could not Retrieve Instant Mix from JellyFin server!")
