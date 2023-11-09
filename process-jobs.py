import json
import os
from termcolor import colored


# Colorize terminal output
class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


import sys


def get_bright_network_jobs(
    bright_network_file="./bright-network-jobs.json",
    accepted_file="./accepted_jobs.json",
    rejected_file="./rejected_jobs.json",
    no_description_file="./no_description.json",
    other_interested_file="./other_interested.json",
):
    # Load bright network jobs
    with open(bright_network_file, "r") as file:
        data = json.load(file)

    # Load or initialize job arrays
    accepted_jobs = load_or_initialize(accepted_file)
    rejected_jobs = load_or_initialize(rejected_file)
    no_description = load_or_initialize(no_description_file)
    other_interested = load_or_initialize(other_interested_file)

    # Get all links from already sorted jobs
    all_links = get_all_links(
        accepted_jobs, rejected_jobs, no_description, other_interested
    )

    # Filter out jobs that have already been processed
    data = [job for job in data if job["link"] not in all_links]

    # Process each job by asking the user if they want to accept or reject it
    for index, job in enumerate(data):
        if "description" not in job or job["description"] is None:
            no_description.append(job)
            save_to_file(no_description, "no_description.json")
            continue

        # Clear the screen and print job details
        os.system("clear" if os.name == "posix" else "cls")
        print(
            colored(
                f"Job {len(all_links) + index + 1}/{len(data) + len(all_links)}",
                "yellow",
            )
        )
        print(colored(f"{job['title']} at {job['company']}", "green"))
        print(job["description"])
        response = input("Do you want to accept this job? (Y/N/O): ").lower()

        if response == "y":
            accepted_jobs.append(job)
            save_to_file(accepted_jobs, "accepted_jobs.json")
        elif response == "n":
            rejected_jobs.append(job)
            save_to_file(rejected_jobs, "rejected_jobs.json")
        elif response == "o":
            other_interested.append(job)
            save_to_file(other_interested, "other_interested.json")
        else:
            print("Invalid input. Please try again.")

        print_stats(accepted_jobs, rejected_jobs, no_description)


def load_or_initialize(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    return []


def get_all_links(*job_lists):
    return [job["link"] for job_list in job_lists for job in job_list]


def save_to_file(data, file_name):
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


def print_stats(accepted_jobs, rejected_jobs, no_description):
    print(f"Accepted jobs: {len(accepted_jobs)}")
    print(f"Rejected jobs: {len(rejected_jobs)}")
    print(f"No description: {len(no_description)}")


if __name__ == "__main__":
    get_bright_network_jobs("./bright-network-jobs-09-11.json")
