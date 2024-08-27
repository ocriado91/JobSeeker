# Job Seeker Abstract Factory implementation.

from abc import ABC, abstractmethod


class JobSeeker(ABC):
    def __init__(self, page_url: str) -> None:
        self.page_url = page_url
        self.location = ""
        self.description = ""
        self.job_data = {}
        self.job_data["url"] = page_url

    @abstractmethod
    def __enter__(self) -> dict:
        pass

    @abstractmethod
    def __exit__(self, exception_type, exception_value, tb):
        pass

    @abstractmethod
    def get_job_description(self) -> None:
        pass
