import asyncio
from client import AsyncClient, AnnouncementId

async def main():
    client = AsyncClient()
    try:
        results, page = await client.get_news(AnnouncementId.ACADEMIC, pageinfo=True)
    except Exception as e:
        print(e)
    await client.close()
    print(page.num, page.rows, page.rows)
    for news in results:
        print(f"""[{news.time}] {news.title}
單位: {news.unitname}
點閱: {news.clicks}
ID: {news.id}
""")

if __name__ == "__main__":
    asyncio.run(main())