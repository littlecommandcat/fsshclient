import asyncio
from client import AsyncClient, AnnouncementId


client = AsyncClient()
last_id = 0

def update_id(new_id: int) -> bool:
    global last_id

    changed = new_id != last_id
    last_id = new_id
    return changed

def display(results):
    for news in results:
        print(f"""[{news.time}] {news.title}
            單位: {news.unitname}
            點閱: {news.clicks}
            ID: {news.id}
        """)
            
async def main():
    global client
    while True:
        try:
            results, page = await client.get_news(AnnouncementId.ACADEMIC, pageinfo=True)
        except Exception as e:
            print(e)
            await client.close()
            return

        if update_id(results[0].id):
            display(results)

        await asyncio.sleep(60)
    

if __name__ == "__main__":
    asyncio.run(main())