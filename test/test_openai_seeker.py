from unittest.mock import patch, Mock
from seekers.openai_seeker import OpenAISeeker


@patch("selenium.webdriver.remote.webdriver.WebDriver.find_element")
def test_job_description(mock_find_element):
    """Test extracting a job description from a mocked OpenAI job offer."""

    # Mock the return value of find_element().text
    mock_element = Mock()
    mock_element.text = "Mocked!"
    mock_find_element.return_value = mock_element

    # Test the get_job_description method in the context of OpenAISeeker.
    # NOTE: We pass a random URL due to Selenium's find_element method
    # is mocked returning a fixed string value.
    with OpenAISeeker("https://www.openai.com") as seeker:
        job_data = seeker.get_job_description()

    # Assert that the job description was extracted correctly
    assert job_data["description"] == "Mocked!"
