from playwright.async_api import async_playwright

from playwright.async_api import async_playwright

# Launch browser
async def launch_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)

    # Set the user agent in the context configuration
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        ignore_https_errors=True
    )

    page = await context.new_page()

    return browser, playwright

async def close_playwright(playwright):
    await playwright.stop()

# Go to a specific page with extended load time and debug statements
async def open_page(browser, url):
    page = await browser.new_page()
    await page.goto(url, wait_until="networkidle")  # Wait until network is idle
    await page.wait_for_load_state("domcontentloaded")  # Wait for DOM content to load
    await page.wait_for_timeout(3000)  # Additional 3-second wait for all elements to load
    return page

# Wait for an element to appear
async def wait_for_element(selector, page):
    await page.wait_for_selector(selector, timeout=60000, state="visible")  # 60 seconds timeout, ensure element is visible

# Type text into a search box
async def type_into_element(selector, text, page):
    await page.fill(selector, text)  # Use fill to enter text in the element

# Click a button and wait for navigation
async def click_element(selector, page):
    async with page.expect_navigation():
        await page.click(selector)


async def click_dropdown(page, dropdown_button, dropdown_menu_open_class, dropdown_item):
    # Step 1: Click the button to open the dropdown
    await page.click(dropdown_button)
    for _ in range(10):  # Retry up to 10 times
        is_expanded = await page.evaluate(f'document.querySelector("{dropdown_button}").getAttribute("aria-expanded") === "true"')
        if is_expanded:
            return True
        await page.wait_for_timeout(500)  # Wait 0.5 seconds between checks
        return False  # Return False if aria-expanded didn't change
    
    # Step 2: Wait until the dropdown menu gains the "is-dropdownOpen" class using JavaScript
    dropdown_open = False
    for _ in range(30):  # Retry for up to 30 seconds
        dropdown_open = await page.evaluate(f'''
            document.querySelector("{dropdown_menu_open_class}")?.classList.contains("is-dropdownOpen")
        ''')
        if dropdown_open:
            break
        await page.wait_for_timeout(1000)  # Wait 1 second between checks
    
    if not dropdown_open:
        raise Exception("Dropdown did not open within the timeout period.")

    # Step 3: Click the dropdown item and wait for navigation if necessary
    async with page.expect_navigation():
        await page.click(dropdown_item, force=True)
