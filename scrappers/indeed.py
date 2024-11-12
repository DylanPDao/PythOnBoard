import asyncio
import urllib.parse
from search_utils import launch_browser, open_page, wait_for_element, close_playwright, extract_job_listings

async def scrape_indeed(url, job_name, location):

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

if __name__ == "__main__":
    job_name = "Software Developer"
    location = "92843"

    # URL encode job name and location to handle spaces and special characters
    encoded_job_name = urllib.parse.quote_plus(job_name)
    encoded_location = urllib.parse.quote_plus(location)

    # Construct the URL dynamically
    job_url = f"https://www.indeed.com/jobs?q={encoded_job_name}&l={encoded_location}&fromage=1"

    jobs = asyncio.run(scrape_indeed(job_url, job_name, location))
    print(jobs)

#xvfb-run python indeed.py