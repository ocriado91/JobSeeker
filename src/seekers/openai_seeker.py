# OpenAI Seeker class implementation.
# This class implements the Job Seeker child for OpenAI.

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from seekers.job_seeker import JobSeeker
from webdriver_manager.firefox import GeckoDriverManager


class OpenAISeeker(JobSeeker):
    def __enter__(self) -> dict:
        """Build the current page Selenium object"""
        # Configure Firefox webdriver to execute into a
        # virtual display.
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        print("Display started!")

        # Define the geckodriver path through Selenium Firefox webdriver
        # service, extract default Firefox options and pass them to
        # Firefox webdriver.
        service = Service(
            executable_path=GeckoDriverManager().install()

        )

        options = Options()
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")

        self.browser = webdriver.Firefox(
            service=service,
            options=options,
        )

        print(f"Extracting data from {self.page_url}")
        self.browser.get(self.page_url)
        return self

    def __exit__(self, exception_type, exception_value, tb):
        return self

    def get_job_description(self) -> str:
        """Extract job description from current page data"""
        print(f"Trying to extract job description from: {self.page_url}")
        element = self.browser.find_element(By.ID, "main")
        self.job_data["description"] = element.text

        # Stop virtual display before to return data
        self.display.stop()
        return self.job_data
