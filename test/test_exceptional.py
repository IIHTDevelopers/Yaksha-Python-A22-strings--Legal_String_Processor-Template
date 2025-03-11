# Updated test_exceptional.py
import pytest
from test.TestUtils import TestUtils
from legal_string_processor import *

@pytest.fixture
def test_obj():
    return TestUtils()

def test_input_validation(test_obj):
    """Test input validation and error handling"""
    try:
        # Test with None inputs
        functions_to_test = [
            (extract_case_name, [None]),
            (extract_parties, [None]),
            (find_section, [None, "SECTION"]),
            (find_section, ["document", None]),
            (extract_client_info, [None, "Client"]),
            (extract_client_info, ["text", None]),
            (extract_date, [None])
        ]
        
        for func, args in functions_to_test:
            with pytest.raises(ValueError):
                func(*args)
        
        # Test with empty parameters where applicable
        with pytest.raises(ValueError):
            find_section("document", "")  # Empty heading
        
        with pytest.raises(ValueError):
            extract_client_info("text", "")  # Empty field
        
        test_obj.yakshaAssert("TestInputValidation", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestInputValidation", False, "exception")
        pytest.fail(f"Input validation test failed: {str(e)}")

def test_error_handling(test_obj):
    """Test specific error handling scenarios"""
    try:
        # Test correct error handling with invalid section
        assert find_section("Regular text", "NON-EXISTENT SECTION") == "", "Should return empty string for non-existent section"
        
        # Test error handling with unusual date formats
        assert extract_date("Meeting on 20230515") == "", "Should handle non-standard date format gracefully"
        
        test_obj.yakshaAssert("TestErrorHandling", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestErrorHandling", False, "exception")
        pytest.fail(f"Error handling test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])