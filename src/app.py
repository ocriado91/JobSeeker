"""
A Streamlit Application to visualize the most demanding skills of
a list of job offers.
"""

import streamlit as st


from stqdm import stqdm
from streamlit_tags import st_tags

from seekers.job_seeker import JobSeeker
from seekers.openai_seeker import OpenAISeeker
from seekers.workable_seeker import WorkableSeeker
from seekers.factorial_seeker import FactorialSeeker
from seekers.clibrain_seeker import CliBrainSeeker
from seekers.intelygenz_seeker import Intelygenz

from utils.config import read_stack_file

seekers = {
    "openai.com": OpenAISeeker,
    "apply.workable.com": WorkableSeeker,
    "careers.factorialhr.com": FactorialSeeker,
    "empleo.clibrain.com": CliBrainSeeker,
    "recruitment.intelygenz.com": Intelygenz,
}


def process_job_descriptions(job_descriptions: list, stack: list) -> dict:
    """Method to retrieve keywords into job descriptions"""

    skills = {}
    for job_description in job_descriptions:
        for tech_stack in stack:
            if tech_stack in job_description:
                if tech_stack not in skills:
                    skills[tech_stack] = 1
                    continue
                skills[tech_stack] += 1

    return skills


def read_new_file(
    stack_file: str = "data/default_stack.dat",
) -> list:
    """Read stack file and export as list

    Parameters
    ----------
    stack_file (str): File with all target stack separated by newline.

    Returns
    ---------
    list: A list with all target stacks.

    """
    return stack_file.getvalue().decode("utf-8").split()


def extract_seeker(job_offer: str) -> JobSeeker:
    """Extract the job seeker object based on job offer url.

    Example of URL:
    https://www.main_page.com/awesome-job-offer

    Parameters:
    - job_offer (str): URL of job offer

    Returns:
    - JobSeeker: JobSeeker object
    """

    # Remove http or https prefix into URL
    _main_page = job_offer.split("//")[1]

    # Extract main page
    _main_page = _main_page.split("/")[0]
    return seekers[_main_page](job_offer)


if __name__ == "__main__":
    # Title of Streamlit UI
    st.title("Job Seeker")
    st.divider()

    # Set the list of default skills into a expander tab and set a
    with st.expander("Selected skills"):
        # Insert a new stack file
        new_stack_file = st.file_uploader("Insert a new stack file")
        if new_stack_file:
            stack_keywords = st_tags(
                value=read_new_file(new_stack_file), label="Keywords"
            )
        else:
            stack_keywords = st_tags(value=read_stack_file(), label="Keywords")

    # Lowerize stack keywords
    stack_keywords = [x.lower() for x in stack_keywords]

    # Create a text box to introduce the list of job offers to process
    # and split retrieved jobs into a list.
    job_offers = st.text_area(
        label="List of job offers (separated by newline)"
    )
    job_offers = job_offers.split("\n")

    jobs_data = []
    skills = {}
    if st.button("Analyze"):
        for idx in stqdm(range(len(job_offers)), desc="Processing Job offers"):
            job_offer = job_offers[idx]

            # Check if current job offer is empty or has been previously
            # processed.
            processed_jobs = [x["url"] for x in jobs_data]
            if not job_offer or job_offer in processed_jobs:
                continue

            # Select the Job Seeker object according to the job offer URL.
            try:
                job_seeker = extract_seeker(job_offer)
            except Exception as error:
                st.write(f"Seeker not found for {job_offer}: {error}")
                continue

            # Extract the job details of offer.
            try:
                with job_seeker as seeker:
                    jobs_data.append(seeker.get_job_description())
            except Exception as error:
                st.write(f"Error processing {job_offer}: {error}")
                continue

        # Process job descriptions and extract skills
        job_descriptions = [x["description"].lower() for x in jobs_data]
        skills = process_job_descriptions(
            job_descriptions=job_descriptions, stack=stack_keywords
        )

        # Sort skills based on their values.
        skills = dict(
            sorted(
                skills.items(),
                key=lambda x: x[1],
            )
        )

        # Show plot.
        st.divider()
        values = list(skills.values())
        words = list(skills.keys())
        st.bar_chart(skills, horizontal=True, use_container_width=True)
