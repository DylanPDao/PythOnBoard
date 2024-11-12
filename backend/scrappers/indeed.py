from scrappers.search_utils import launch_browser, open_page, wait_for_element, close_playwright, extract_job_listings

async def scrape_indeed(url):

    # Define selectors for job listings on Indeed
    job_container_selector = '.resultContent'
    title_selector = 'h2.jobTitle span[title]'
    company_selector = 'div.company_location [data-testid="company-name"]'
    location_selector = 'div.company_location [data-testid="text-location"]'
    url_selector = 'h2.jobTitle a.jcs-JobTitle'

    # Launch browser
    browser, playwright = await launch_browser() 
    jobs = []  # List to store job information

    try:
        # Go to specific page
        page = await open_page(browser, url)

        # Wait for job listings to load
        await wait_for_element('.resultContent', page)

        # Call the utility function to extract job listings
        jobs = await extract_job_listings(page, job_container_selector, title_selector, company_selector, location_selector, url_selector)
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the browser closes
        await browser.close()
        await close_playwright(playwright)
    
    return jobs
