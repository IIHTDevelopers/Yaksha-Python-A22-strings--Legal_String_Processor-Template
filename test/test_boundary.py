# Updated test_boundary.py
import pytest
from test.TestUtils import TestUtils
from legal_string_processor import *

@pytest.fixture
def test_obj():
    return TestUtils()

def test_boundary_cases(test_obj):
    """Test boundary scenarios for legal string operations"""
    try:
        # Test with empty strings
        empty_string = ""
        
        # Empty citation tests
        case_name = extract_case_name(empty_string)
        assert case_name == "", "Empty citation should return empty case name"
        
        parties = extract_parties(empty_string)
        assert parties == (empty_string, ""), "Empty case name should return empty parties"
        
        # Empty document tests
        section = find_section(empty_string, "SECTION")
        assert section == "", "Empty document should return empty section"
        
        # Test date extraction with no dates
        no_date = extract_date("This text has no dates in it")
        assert no_date == "", "No date should return empty string"
        
        # Test client info with missing field
        client_info = "Client: John Doe\nDOB: 1980-05-15"
        missing_field = extract_client_info(client_info, "Attorney")
        assert missing_field == "", "Missing field should return empty string"
        
        test_obj.yakshaAssert("TestBoundaryCases", True, "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestBoundaryCases", False, "boundary")
        pytest.fail(f"Boundary cases test failed: {str(e)}")

def test_edge_cases(test_obj):
    """Test edge cases for legal string operations"""
    try:
        # Test with unusual citation formats
        unusual = "The People ex rel. Smith v. Jones et al., 123 Cal.4th 456 (2023)"
        case_name = extract_case_name(unusual)
        assert "The People ex rel. Smith v. Jones et al." in case_name, "Should handle unusual citation format"
        
        # Test with complex party names
        complex_name = "John Smith, et al. v. Acme Corporation, Inc."
        parties = extract_parties(complex_name)
        assert "John Smith, et al." in parties[0], "Should handle complex plaintiff names"
        assert "Acme Corporation, Inc." in parties[1], "Should handle complex defendant names"
        
        # Test section finder with section in middle of text
        middle_section = "Intro\n\nSECTION 1. TEST\n\nContent\n\nEnd"
        section = find_section(middle_section, "SECTION 1. TEST")
        assert "Content" in section, "Should find section in middle of text"
        
        test_obj.yakshaAssert("TestEdgeCases", True, "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestEdgeCases", False, "boundary")
        pytest.fail(f"Edge cases test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])