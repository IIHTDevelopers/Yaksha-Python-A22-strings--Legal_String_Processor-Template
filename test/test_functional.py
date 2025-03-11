import pytest
import inspect
import re
from test.TestUtils import TestUtils
from legal_string_processor import *

@pytest.fixture
def test_obj():
    return TestUtils()

def test_string_method_usage(test_obj):
    """Test that functions use appropriate string methods"""
    try:
        # Check each function for proper string method usage
        functions_to_check = [
            (extract_case_name, ["find", "split", "strip"]),
            (extract_parties, ["split", "strip"]),
            (extract_date, ["split", "strip", "isdigit"]),
            (find_section, ["find", "strip"]),
            (extract_client_info, ["find", "strip"])
        ]
        
        for func, expected_methods in functions_to_check:
            source = inspect.getsource(func)
            for method in expected_methods:
                assert method in source, f"{func.__name__} should use '{method}' string operation"
        
        test_obj.yakshaAssert("test_string_method_usage", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("test_string_method_usage", False, "functional")
        pytest.fail(f"String method usage test failed: {str(e)}")

def test_string_slicing_usage(test_obj):
    """Test that functions use string slicing appropriately"""
    try:
        # Check each function for slicing operations
        slicing_functions = [extract_case_name, extract_date, find_section, extract_client_info]
        
        for func in slicing_functions:
            source = inspect.getsource(func)
            # Check for slicing syntax [x:y]
            assert re.search(r'\[[^\]]*:[^\]]*\]', source), f"{func.__name__} should use string slicing"
        
        # Special case for extract_date which needs specific slicing
        date_source = inspect.getsource(extract_date)
        assert "0:4" in date_source, "extract_date should slice year component"
        assert "5:7" in date_source, "extract_date should slice month component"
        assert "8:10" in date_source, "extract_date should slice day component"
        
        test_obj.yakshaAssert("test_string_slicing_usage", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("test_string_slicing_usage", False, "functional")
        pytest.fail(f"String slicing usage test failed: {str(e)}")

def test_string_manipulation_accuracy(test_obj):
    """Test the accuracy of string manipulation operations"""
    try:
        # Test case name extraction with various formats
        assert extract_case_name("Smith v. Jones, 123 F.3d 456") == "Smith v. Jones", "Case name extraction failed"
        assert extract_case_name("Smith, et al. v. Jones Corp., 123 F.3d 456") == "Smith, et al. v. Jones Corp.", "Complex case name extraction failed"
        
        # Test party extraction
        plaintiff, defendant = extract_parties("Smith v. Jones")
        assert plaintiff == "Smith" and defendant == "Jones", "Party extraction failed"
        
        # Test date extraction
        assert extract_date("Filed on 2023-05-15") == "2023-05-15", "Date extraction failed"
        
        # Test section finding
        document = "SECTION 1. TEST\n\nThis is test content.\n\nSECTION 2. ANOTHER TEST\n\nMore content."
        section = find_section(document, "SECTION 1. TEST")
        assert "This is test content" in section, "Section finding failed"
        assert "SECTION 2" not in section, "Section finding included too much content"
        
        # Test client info extraction
        client_info = "Client: John Doe\nDOB: 1980-05-15"
        assert extract_client_info(client_info, "Client") == "John Doe", "Client info extraction failed"
        
        test_obj.yakshaAssert("test_string_manipulation_accuracy", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("test_string_manipulation_accuracy", False, "functional")
        pytest.fail(f"String manipulation accuracy test failed: {str(e)}")

def test_variable_names(test_obj):
    """Test that functions use appropriate variable names"""
    try:
        # Check for appropriate variable names in functions
        expected_variables = {
            "extract_case_name": ["citation", "separator", "parts", "plaintiff", "defendant"],
            "extract_parties": ["case_name", "parties"],
            "extract_date": ["text", "words", "year", "month", "day"],
            "find_section": ["document", "heading", "content", "heading_pos"],
            "extract_client_info": ["text", "field", "value"]
        }
        
        for func_name, expected_vars in expected_variables.items():
            func = globals()[func_name]
            source = inspect.getsource(func)
            for var in expected_vars:
                assert var in source, f"{func_name} should use variable name '{var}'"
        
        # Check initialize_legal_samples for required text samples
        init_source = inspect.getsource(initialize_legal_samples)
        required_variables = ["case_citation", "client_info", "contract_section", "legal_document"]
        for var in required_variables:
            assert var in init_source, f"initialize_legal_samples should define '{var}'"
        
        test_obj.yakshaAssert("test_variable_names", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("test_variable_names", False, "functional")
        pytest.fail(f"Variable names test failed: {str(e)}")

def test_sample_data_quality(test_obj):
    """Test the quality and correctness of sample data"""
    try:
        # Check if sample data meets requirements
        samples = initialize_legal_samples()
        assert len(samples) >= 4, "Should provide at least 4 different text samples"
        
        # Check case citation
        assert any("v." in sample for sample in samples), "Should include case citation with 'v.'"
        
        # Check client information
        assert any("Client:" in sample for sample in samples), "Should include client information"
        assert any("DOB:" in sample for sample in samples), "Should include date of birth field"
        
        # Check legal document structure
        assert any("SECTION" in sample for sample in samples), "Should include document with sections"
        
        # Check dates in standard format
        assert any(re.search(r'\d{4}-\d{2}-\d{2}', sample) for sample in samples), "Should include dates in YYYY-MM-DD format"
        
        test_obj.yakshaAssert("test_sample_data_quality", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("test_sample_data_quality", False, "functional")
        pytest.fail(f"Sample data quality test failed: {str(e)}")

def test_function_logic(test_obj):
    """Test the logical implementation of functions"""
    try:
        # Test extract_case_name logic with different formats
        case1 = extract_case_name("Smith v. Jones, 123 F.3d 456")
        case2 = extract_case_name("Brown vs. Board, 347 U.S. 483")
        case3 = extract_case_name("Martinez, Plaintiff v. Johnson, Defendant")
        
        assert case1 == "Smith v. Jones", "Should handle v. format"
        assert case2 == "Brown vs. Board", "Should handle vs. format"
        assert "Martinez" in case3, "Should handle complex format"
        
        # Test extract_parties with non-standard inputs
        p1, d1 = extract_parties("Smith v. Jones")
        p2, d2 = extract_parties("The State vs. Defendant")
        
        assert p1 == "Smith" and d1 == "Jones", "Basic party extraction"
        assert p2 == "The State", "Should handle multi-word parties"
        
        # Test extract_date logic
        date1 = extract_date("Date: 2023-05-15 is important")
        date2 = extract_date("Multiple dates: 2022-01-01 and 2023-12-31")
        date3 = extract_date("No valid dates here")
        
        assert date1 == "2023-05-15", "Should extract date regardless of position"
        assert date2 in ["2022-01-01", "2023-12-31"], "Should extract at least one date"
        assert date3 == "", "Should return empty string for no dates"
        
        # Test find_section with edge cases
        doc1 = "SECTION A\nContent A\nSECTION B\nContent B"
        doc2 = "SECTION X\nMultiple\nLines\nOf\nContent"
        
        sec1 = find_section(doc1, "SECTION A")
        sec2 = find_section(doc2, "SECTION X")
        
        assert "Content A" in sec1, "Should find single-line content"
        assert "Multiple" in sec2 and "Content" in sec2, "Should find multi-line content"
        
        # Test extract_client_info with different formats
        client1 = "Client: John Doe\nInfo: Important"
        client2 = "Name: Jane Smith\nClient: Not this\nDOB: 1990-01-01"
        
        info1 = extract_client_info(client1, "Client")
        info2 = extract_client_info(client1, "Info")
        info3 = extract_client_info(client2, "DOB")
        
        assert info1 == "John Doe", "Should extract value after colon"
        assert info2 == "Important", "Should work with any field name"
        assert info3 == "1990-01-01", "Should find field anywhere in text"
        
        test_obj.yakshaAssert("test_function_logic", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("test_function_logic", False, "functional")
        pytest.fail(f"Function logic test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])