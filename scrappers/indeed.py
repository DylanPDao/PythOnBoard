import asyncio
from search_utils import launch_browser, open_page, wait_for_element, type_into_element, click_element, close_playwright, click_dropdown

async def scrape_indeed(url, job_name, location):

    # Launch browser
    browser, playwright = await launch_browser() 
    jobs = []  # List to store job information

    try:
        # Go to specific page
        page = await open_page(browser, url)

        # Wait for search boxes to open
        await wait_for_element('#text-input-what', page)
        await wait_for_element('#text-input-where', page)

        # Type into search boxes
        await type_into_element('#text-input-what', job_name, page)
        await type_into_element('#text-input-where', location, page)

        # Hit submit
        await click_element('button[type="submit"]', page)

        #filter to last 24 hours    
        await click_dropdown(page, '#filter-dateposted','.yosegi-FilterPill-dropdownPillContainer', 'a:has-text("Last 24 hours")')

        # Wait for job listings to load
        await wait_for_element('.resultContent', page)

        # Grab listings
        job_listings = await page.query_selector_all('.resultContent')
        for job in job_listings:
            # Extract the job title
            title_element = await job.query_selector('h2.jobTitle span[title]') 
            title = await page.evaluate('(element) => element ? element.textContent : ""', title_element)

            # Extract the company name
            company_element = await job.query_selector('div.company_location [data-testid="company-name"]')
            company = await page.evaluate('(element) => element ? element.textContent : ""', company_element)

            # Extract the location
            location_element = await job.query_selector('div.company_location [data-testid="text-location"]')
            job_location = await page.evaluate('(element) => element ? element.textContent : ""', location_element)

            # Extract the job URL
            url_element = await job.query_selector('h2.jobTitle a.jcs-JobTitle')
            url = await page.evaluate('(element) => element ? element.href : ""', url_element)

            # Append job details to the jobs list
            jobs.append({
                "title": title,
                "company": company,
                "location": job_location,
                "url": url  
            })
    
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the browser closes
        await browser.close()
        await close_playwright(playwright)
    
    return jobs

if __name__ == "__main__":
    job_url = "https://www.indeed.com"
    job_name = "Software Developer"
    location = "92843"
    jobs = asyncio.run(scrape_indeed(job_url, job_name, location))
    print(jobs)
