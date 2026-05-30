import asyncio
from DiscordJellyFinBot import main as botmain
from api import main as apimain

async def main():

    await asyncio.gather(
        apimain(),
        botmain()
    )

if __name__ == "__main__":
    asyncio.run(main())