import os
import base64
import pytest
import tempfile
from unittest.mock import patch, MagicMock
from collections import namedtuple
from src.rmlst_api.rmlst import rmlst_api
from src.rmlst_api.constants import uri

@pytest.fixture
def mock_assembly_file():
    """Creates a temporary assembly file for testing."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as temp_file:
        temp_file.write(">test_seq\nATGCATGCATGC")
        temp_file_path = temp_file.name
    yield temp_file_path
    os.remove(temp_file_path)  # Cleanup after test

@patch("requests.post")  # Mock the requests.post function
def test_rmlst_api(mock_post, mock_assembly_file):
    """Test the rmlst_api function."""
    
    # Define mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    mock_post.return_value = mock_response  # Set mock return value
    
    # Expected sample name (extracted from file name)
    expected_sample = os.path.splitext(os.path.basename(mock_assembly_file))[0]

    # Call the function
    result = rmlst_api(mock_assembly_file)

    # Validate the API call
    with open(mock_assembly_file, "r") as f:
        fasta_data = f.read()
    expected_payload = {
        "base64": True,
        "details": True,
        "sequence": base64.b64encode(fasta_data.encode()).decode(),
    }
    
    # Ensure correct API request was made
    mock_post.assert_called_once_with(uri, data=str(expected_payload))  # Ensure the correct URI is used

    # Ensure the returned named tuple has the expected values
    RmlstApiOutput = namedtuple("rmlst_api_output", ["sample", "api_response", "data"])
    expected_output = RmlstApiOutput(sample=expected_sample, api_response=mock_response, data={"result": "success", "sample": expected_sample})

    assert result.sample == expected_output.sample
    assert result.api_response.status_code == 200
    assert result.data == expected_output.data
