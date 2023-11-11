import json
import os
import re
import requests
from bs4 import BeautifulSoup
from termcolor import colored
from urllib.parse import urljoin


def format_heading(text):
    return colored(text, "blue")


def fetch_bright_network_jobs():
    """
    The approach in this function is to use requests function to fetch the HTML content of the page, then use BeautifulSoup to parse the HTML content and extract the job listings.
    This only works because bright network does not use dynamic JavaScript to render pages. Meaning this approach will not work for all websites. For other websites, we will need to use selenium or go back to nodejs and use playwright like a sane person.
    """
    url = input("Please enter the Bright Network page with the roles you're interested in, e.g. https://www.brightnetwork.co.uk/application-deadlines/jobs/graduate-schemes/technology/: \n")
    
    print(colored("Fetching job list ....", "yellow"))

    response = requests.get(url)
    response.raise_for_status()  # Raises HTTPError if the HTTP request returned an unsuccessful status code

    soup = BeautifulSoup(response.content, "html.parser")

    # Find all job listings
    job_elements = soup.select(".article-content li")
    jobs = []
    for index, job_element in enumerate(job_elements):
        company_name_element = job_element.find("span")
        job_link_element = job_element.find("a")

        if company_name_element and job_link_element:
            full_url = urljoin(url, job_link_element["href"])

            jobs.append(
                {
                    "company": company_name_element.get_text(strip=True),
                    "title": job_link_element.get_text(strip=True),
                    "link": full_url,
                    "description": None,  # Placeholder for the job description
                }
            )

    print(colored(f"Found {len(jobs)} jobs", "green"))

    # Fetch job descriptions
    print(colored("Getting job descriptions...", "yellow"))
    descriptions_missing = 0
    for index, job in enumerate(jobs):
        try:
            print(
                colored(
                    f"Getting job descriptions... {index + 1}/{len(jobs)}", "yellow"
                ),
                end="",
            )

            job_response = requests.get(job["link"])
            job_response.raise_for_status()

            job_soup = BeautifulSoup(job_response.content, "html.parser")
            body_element = job_soup.select_one("main article")

            if body_element:
                job["description"] = body_element.get_text(separator="\n", strip=True)
                # Find and format headings within the job description
                headings = body_element.find_all("h2")
                for heading in headings:
                    original_heading = heading.get_text(strip=True)
                    formatted_heading = format_heading(original_heading)
                    # Create regex to find the heading in the job description
                    heading_regex = re.escape(original_heading)
                    job["description"] = re.sub(
                        heading_regex, formatted_heading, job["description"]
                    )

                print(colored(" (Description fetched)", "green"))
            else:
                descriptions_missing += 1
                print(
                    colored(f" (Descriptions missing: {descriptions_missing})", "red")
                )
        except Exception as e:
            descriptions_missing += 1
            print(colored(f" (Failed due to an unexpected error: {e})", "red"))

    return jobs


def update_job_listings(fetch_jobs_function, existing_jobs_file, new_jobs_file=None):
    if new_jobs_file is None:
        new_jobs_file = existing_jobs_file

    # Fetch new job listings
    bn_jobs = fetch_jobs_function()

    # Check if the JSON file with existing jobs exists
    if os.path.exists(existing_jobs_file):
        # Read the existing jobs from the file
        with open(existing_jobs_file, "r", encoding="utf-8") as file:
            existing_jobs = json.load(file)
        print(f"existing jobs: {len(existing_jobs)}")

        # Filter out the jobs we've seen before
        bn_jobs = [
            job
            for job in bn_jobs
            if not any(
                job["link"] == existing_job["link"] for existing_job in existing_jobs
            )
        ]
    else:
        # If the file doesn't exist, assume no existing jobs
        existing_jobs = []

    print(f"new jobs: {len(bn_jobs)}")

    # Write the new list of jobs to the specified JSON file
    try:
        with open(new_jobs_file, "w", encoding="utf-8") as file:
            json.dump(bn_jobs, file, ensure_ascii=False, indent=4)
        print(f"Successfully updated {new_jobs_file}")
    except Exception as e:
        print(f"Error writing to {new_jobs_file}:", e)
        raise


if __name__ == "__main__":
    update_job_listings(
        fetch_bright_network_jobs,
        "bright-network-jobs.json",
        "bright-network-jobs.json",
    )
