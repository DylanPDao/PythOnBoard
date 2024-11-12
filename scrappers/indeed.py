import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto('https://example.com', {'waitUntil': 'networkidle2'})
    content = await page.evaluate('document.querySelector("h1").innerText')
    print(content)
    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())