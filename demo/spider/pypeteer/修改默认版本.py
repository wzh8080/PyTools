"""
永久更改 pyppeteer 的chrome的默认路径
npm install puppeteer-core
"""

from pyppeteer import launch


async def main():
    browser = await launch(executablePath='D:\Tools\chrome-win\chrome.exe')
    page = await browser.newPage()
    # await page.goto('https://example.com')
    await browser.close()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
