import configparser
from fastapi import FastAPI
from fastapi.responses import FileResponse
import uvicorn
import music_commands as commands

config = configparser.ConfigParser()

# Read the config file
config.read('config.cfg')

#api
port = config.getint('API', 'port')

# FastAPI server
app = FastAPI()

def setup(music_player):
    global player
    player = music_player


@app.get("/")
async def web_home():
    return FileResponse("index.html")

@app.get("/api/")
async def home():
    return {"status": "online"}

@app.api_route("/api/play/", methods=["GET", "POST"])
async def play(song_name=" "):    
    try:
        result = await commands.play(song_name)
        return result
    except Exception as e:
        return (f"error playing: {e}")

@app.api_route("/api/clearqueue/", methods=["GET", "POST"])
async def clearqueueapi():
    result = await commands.clearqueue()
    return result

@app.api_route("/api/queue/", methods=["GET", "POST"])
async def queueapi():
    result = player.queue_list
    return result

@app.api_route("/api/skip/", methods=["GET", "POST"])
async def skipapi():
    result = await commands.skip()
    return result

@app.api_route("/api/randomplaylist/", methods=["GET", "POST"])
async def randompl(args: str = ""):
    args = tuple(args.split())
    result = await commands.randomplaylist(args)
    return result

@app.get("/api/randomsong/")
async def randoms():
    return await commands.randomsong()

@app.get("/api/pause/")
async def pause():
    return await commands.pause()

@app.get("/api/resume/")
async def resume():
    return await commands.resume()

@app.get("/api/stop/")
async def stop():
    return await commands.stop()

@app.get("/api/loop/")
async def loop(id=""):
    return await commands.loop(id)

@app.get("/api/instantmix/")
async def instantmix():
    return await commands.instantmix()

@app.get("/api/songs/")
async def songs():
    return await commands.songs()

@app.get("/api/currentlyplayingsong/")
async def currently_playing_song():
    return player.nowplaying

@app.get("/api/playnow/")
async def playnow():
    return await commands.playnow()

@app.get("/api/playnext/")
async def playnext():
    return await commands.playnext()

@app.get("/api/updatesongs/")
async def updatesongs():
    return await commands.updatesongs()


async def start_api(port):
    print(f"Starting API on port {port}...")
    config = uvicorn.Config(app, host="0.0.0.0", port=port)
    server = uvicorn.Server(config)
    await server.serve()

# Run both together
async def main():
    
    await start_api(port)
