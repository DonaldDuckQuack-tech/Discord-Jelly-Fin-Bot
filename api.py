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


app.get("/")
async def web_home():
    return FileResponse("index.html")

@app.get("/api/")
async def home():
    return {"status": "online"}

@app.api_route("/api/play/", methods=["GET", "POST"])
async def play(song_name: str):    
    try:
        await commands.play(song_name)
    except Exception as e:
        return (f"error playing: {e}")

@app.api_route("/api/clearqueue/", methods=["GET", "POST"])
async def clearqueueapi():
    result = await commands.clearqueue()
    return result

@app.api_route("/api/queue/", methods=["GET", "POST"])
async def queueapi():
    result = await commands.queue()
    return result

@app.api_route("/api/skip/", methods=["GET", "POST"])
async def skipapi():
    result = await commands.skip()
    return result

@app.get("/api/randomplaylist/")
async def randompl():
    return commands.randomplaylist

@app.get("/api/randomsong/")
async def randoms():
    return commands.randomsong()

@app.get("/api/pause/")
async def pause():
    return commands.pause()

@app.get("/api/resume/")
async def resume():
    return commands.resume()

@app.get("/api/stop/")
async def stop():
    return commands.stop()

@app.get("/api/loop/")
async def loop():
    return commands.loop()

@app.get("/api/instantmix/")
async def instantmix():
    return commands.instantmix()

@app.get("/api/songs/")
async def songs():
    return commands.songs()

@app.get("/api/currentlyplayingsong/")
async def currently_playing_song():
    return commands.nowplaying()

@app.get("/api/playnow/")
async def playnow():
    return commands.playnow()

@app.get("/api/playnext/")
async def playnext():
    return commands.playnext()

@app.get("/api/updatesongs/")
async def updatesongs():
    return commands.updatesongs()


async def start_api(port):
    print(f"Starting API on port {port}...")
    config = uvicorn.Config(app, host="0.0.0.0", port=port)
    server = uvicorn.Server(config)
    await server.serve()

# Run both together
async def main():
    
    await start_api(port)
