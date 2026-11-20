import asyncio
from playwright.async_api import async_playwright, TimeoutError

ANSWER = "A"

accounts = [








{"username": "DSK-1", "wallet": "4Uyr3wM3ByLLXbSrn1t5zBMGgY6vu9nCiz8p3xjUAChF"},
{"username": "DSK-2", "wallet": "BPRdiz43i1DUwchJZeqxcXfZNiMrrfCGH4UF5MsACa7j"},
{"username": "DSK-3", "wallet": "5zR3kQ3v2MgEnHbfX78zWf1gFW4yycat1CpFTsijwxdq"},
{"username": "DSK-4", "wallet": "D8cwj1JvvEUuJ5uDppaN4Z92Ki3tuz5tMME4tKSeJmpP"},
{"username": "DSK-5", "wallet": "3gEuEfzoXHdxFzUQGe1psvAinhuu87MVy33WzJVZSxi3"},
{"username": "DSK-6", "wallet": "78VNqXHSGUEb79XrbPEtPfaCR42SHUxVXarJgTVf9pnk"},
{"username": "DSK-7", "wallet": "716Rnn8v6tpHYhp7bAowNExzPN69kKiD3sFqWQZa5XGV"},
{"username": "DSK-8", "wallet": "363z9828bP9PxbFRHq565Tuot3J1BhGoqWk2L7SeArrA"},
{"username": "DSK-9", "wallet": "F7DijzQaQQZjQL5YjkFaPzBCPCYLZS7g8KbVMjMt4UTk"},
{"username": "DSK-10", "wallet": "FaMrfyF7kNs4AdhA2o8BHJNtL3ULTmajJPRbYUC3ZQXY"},
{"username": "DSK-11", "wallet": "FwMqVQz7YKguHbMDEFuUvhXSUL9hkgw2RW49CkE9qzW2"},
{"username": "DSK-12", "wallet": "Cid2emHFX3gnu8bw3Bc5dyHsiJ5GPJvvFHURQ3aVxBH4"},
{"username": "DSK-13", "wallet": "8kf8CJtu8sZrV6uJdHQKgQgSFtWiqUo7nDEHpmYoCesU"},
{"username": "DSK-14", "wallet": "GFFH5FDwptWogq8rbhmw2W7PnwW9SkbBuvDKRaju2WjS"},
{"username": "DSK-15", "wallet": "HvbspxKHETHyeSJhWpQEYvmkupsybuykTbhBd5nPm87d"},
{"username": "DSK-16", "wallet": "AYpFyVtDA5T15zT4epepTihwbsrikUVcsnqbaPzTd24L"},
{"username": "DSK-17", "wallet": "8gcBWC1hxW1rLjAt3qs5D7ik4bbkW3kvUP7KXXNr2Yau"},
{"username": "DSK-18", "wallet": "8LR1MYXsivCZJdpttstoGbcgz5yBNcczaFhsUzXxCMGx"},
{"username": "DSK-19", "wallet": "5joAWedexWpUBFSixgRkbxVa4WoPYsc8qtbscJhYDht1"},
{"username": "DSK-20", "wallet": "GBjYaQ3UbBegk3BQMwWuc9bDbebbejL5e4eHJtR1ibUn"},
{"username": "DSK-21", "wallet": "DMPbJoDt5p3PTLDzFBHuCarw6g293QKsxvo23NKeizeH"},
{"username": "DSK-22", "wallet": "CpjVuR8S1fDht6F4VH8ec2Mj2ZiW1moWdN8mQczK56V9"},



    
]

async def handle_modal(page):
    modal = page.locator("#scamMigrationWarningModal")
    try:
        if await modal.is_visible(timeout=5000):
            print("⚠️ Closing modal...")
            buttons = modal.locator("button")
            if await buttons.count() > 0:
                await buttons.first.click()
                await page.wait_for_timeout(1000)
    except:
        pass

async def run_bot():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        for acc in accounts:
            context = await browser.new_context()
            page = await context.new_page()

            print("Running account:", acc["username"])

            try:
                await page.goto("https://theros.io/prelaunch", timeout=80000)
                await page.wait_for_load_state("networkidle", timeout=15000)
            except Exception as e:
                print(f"Connection error for {acc['username']}: {e}. Skipping account.")
                await context.close()
                continue

            await handle_modal(page)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_selector("input", timeout=15000)

            inputs = await page.query_selector_all("input")
            if len(inputs) < 2:
                print(f"Not enough inputs for {acc['username']}, skipping")
                await context.close()
                continue

            await inputs[0].fill(acc["username"])
            await inputs[1].fill(acc["wallet"])

            if len(inputs) > 2:
                await inputs[2].fill("bot")

            await handle_modal(page)

            create_btn = page.locator("#registerBtn")
            try:
                await create_btn.click(timeout=9000)
            except TimeoutError:
                await create_btn.click(force=True)

            next_btn = page.locator("#nextQuestionBtn")
            try:
                await next_btn.wait_for(state="visible", timeout=8000)
                await next_btn.click()
            except:
                pass

            answer_selector = f"#answer{ANSWER.upper()}"
            try:
                await page.locator(answer_selector).click(timeout=20000)
                print("Answered:", ANSWER)
            except Exception as e:
                print(f"Failed to answer: {e}")

            await page.wait_for_timeout(1000)
            await context.close()

        await browser.close()
        print("🎉 All accounts processed successfully!")

if __name__ == "__main__":
    asyncio.run(run_bot())
              
