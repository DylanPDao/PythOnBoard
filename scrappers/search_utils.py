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


#grab listings
async def extract_job_listings(page, job_container_selector, title_selector, company_selector, location_selector, url_selector):
    jobs = []
    
    # Grab all job listings
    job_listings = await page.query_selector_all(job_container_selector)
    
    for job in job_listings:
        # Extract the job title
        title_element = await job.query_selector(title_selector)
        title = await page.evaluate('(element) => element ? element.textContent : ""', title_element)

        # Extract the company name
        company_element = await job.query_selector(company_selector)
        company = await page.evaluate('(element) => element ? element.textContent : ""', company_element)

        # Extract the location
        location_element = await job.query_selector(location_selector)
        job_location = await page.evaluate('(element) => element ? element.textContent : ""', location_element)

        # Extract the job URL
        url_element = await job.query_selector(url_selector)
        url = await page.evaluate('(element) => element ? element.href : ""', url_element)

        # Append job details to the jobs list
        jobs.append({
            "title": title,
            "company": company,
            "location": job_location,
            "url": url  
        })

    return jobs
