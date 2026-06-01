# Discord-Jelly-Fin-Bot
A Bot to play and control music from a Jellyfin server on discord

### Installation
1. download the latest version from https://github.com/DonaldDuckQuack-tech/Discord-Jelly-Fin-Bot/releases/latest/
2. from within the source code directory run: pip install -r requirements.txt
3. fill in the required details in config.cfg.
4. run: python main.py

### Commands

#### <ins>!clearqueue</ins>

**Description:** Command to clear the queue.  
**Usage:** !clearqueue

#### <ins>!help</ins>

**Description:** Lists all available commands  
**Usage:** !help

#### <ins>!instantmix</ins>

**Description:** Command to add an instantmix to the queue.  
**Usage:** !instantmix [id] [limit]

#### <ins>!loop</ins>

**Description:** Command to play loop a song from the list.  
**Usage:** !loop [song_name]

#### <ins>!pause</ins>

**Description:** Command to pause currently playing audio  
**Usage:** !pause

#### <ins>!ping</ins>

**Description:** Command to ping the bot  
**Usage:** !ping

#### <ins>!play</ins>

**Description:** Command to add a song/s to the queue.  
**Usage:** !play [song_name]

#### <ins>!playall</ins>

**Description:** Command to play all the songs in the list one by one.  
**Usage:** !playall

#### <ins>!playnext</ins>

**Description:** Command to add a song/s next in the queue.  
**Usage:** !playnext [song_name]

#### <ins>!playnow</ins>

**Description:** Command to add a song/s next in the queue and play them.  
**Usage:** !playnow [song_name]

#### <ins>!queue</ins>

**Description:** Command to show what is currently in the queue.  
**Usage:** !queue [page]

#### <ins>!randomplaylist</ins>

**Description:** Command to add multiple songs to the queue based on album, artist or random songs.  
**Usage:** !randomplaylist <keywords...>

#### <ins>!randomsong</ins>

**Description:** Command to add a random song to the queue.  
**Usage:** !randomsong

#### <ins>!remove</ins>

**Description:** Command to remove a song from the queue.  
**Usage:** !remove [song_name]

#### <ins>!resume</ins>

**Description:** Command to resume currently playing audio  
**Usage:** !resume

#### <ins>!search</ins>

**Description:** Command to search for songs based on the artist, album or song name.  
**Usage:** !search <keywords...>

#### <ins>!skip</ins>

**Description:** Command to skip the currently playing song.  
**Usage:** !skip

#### <ins>!songs</ins>

**Description:** Command to list all available songs, paginated by 10 songs per page.  
**Usage:** !songs [page]

#### <ins>!stop</ins>

**Description:** Command to stop any currently playing music.  
**Usage:** !stop

#### <ins>!updatesongs</ins>

**Description:** Command to update the songs database for the bot.  
**Usage:** !updatesongs

#### <ins>!version</ins>

**Description:** Command to show JellyFin Music Bot Version  
**Usage:** !version


