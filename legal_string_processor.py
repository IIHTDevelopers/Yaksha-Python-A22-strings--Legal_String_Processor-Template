"""
Legal String Processor
Demonstrates basic string operations with legal text examples.
"""

def initialize_legal_samples():
    """Initialize sample legal text data."""
    # Sample case citation
    case_citation = "Smith v. Jones, 123 F.3d 456 (9th Cir. 2023)"
    
    # Sample client information
    client_info = "Client: John Doe\nDOB: 1980-05-15\nCase #: CR-2023-01234"
    
    # Sample contract section
    contract_section = """SECTION 1. DEFINITIONS
    
1.1 "Agreement" means this Service Agreement.
1.2 "Client" means the party engaging the Services.
"""
    
    # Sample legal document with dates
    legal_document = """SETTLEMENT AGREEMENT
    
This Agreement is made effective as of 2023-06-15, by and between 
Party A and Party B (collectively, the "Parties").

RECITALS:
WHEREAS, a dispute arose between the Parties on 2022-11-30;
"""
    
    return (case_citation, client_info, contract_section, legal_document)

def extract_case_name(citation):
    """Extract the case name from a case citation."""
    if citation is None:
        raise ValueError("Citation cannot be None")
    
    # Handle v. or vs. formats
    if " v. " in citation:
        separator = " v. "
    elif " vs. " in citation:
        separator = " vs. "
    else:
        comma_pos = citation.find(',')
        if comma_pos == -1:
            return citation
        return citation[:comma_pos].strip()
    
    # Split the citation at the separator
    parts = citation.split(separator)
    
    if len(parts) < 2:
        comma_pos = citation.find(',')
        if comma_pos == -1:
            return citation
        return citation[:comma_pos].strip()
    
    # Get plaintiff and defendant parts
    plaintiff = parts[0].strip()
    defendant_parts = parts[1].split(',')
    defendant = defendant_parts[0].strip()
    
    return f"{plaintiff}{separator}{defendant}"

def extract_parties(case_name):
    """Extract plaintiff and defendant from a case name."""
    if case_name is None:
        raise ValueError("Case name cannot be None")
    
    # Split by " v. " or " vs. " to get parties
    if " v. " in case_name:
        parties = case_name.split(" v. ")
    elif " vs. " in case_name:
        parties = case_name.split(" vs. ")
    else:
        return (case_name, "")
    
    if len(parties) == 2:
        return (parties[0].strip(), parties[1].strip())
    else:
        return (case_name, "")

def extract_date(text):
    """Extract a date in YYYY-MM-DD format from text."""
    if text is None:
        raise ValueError("Text cannot be None")
    
    # Find a date in YYYY-MM-DD format
    words = text.split()
    
    for word in words:
        # Clean the word from punctuation
        clean_word = word.strip(',.;:\'\"()[]{}')
        
        # Check if it matches date format YYYY-MM-DD
        if len(clean_word) == 10 and clean_word[4] == '-' and clean_word[7] == '-':
            year = clean_word[0:4]
            month = clean_word[5:7]
            day = clean_word[8:10]
            
            if year.isdigit() and month.isdigit() and day.isdigit():
                return clean_word
    
    return ""

def find_section(document, heading):
    """Find a section in a document by its heading."""
    if document is None or heading is None:
        raise ValueError("Document and heading cannot be None")
    
    if not heading:
        raise ValueError("Heading cannot be empty")
    
    # Find the heading position
    heading_pos = document.find(heading)
    if heading_pos == -1:
        return ""
    
    # Find the start of content (after heading and any newlines)
    content_start = document.find('\n', heading_pos)
    if content_start == -1:
        return ""
    
    # Find the next heading or end of document
    next_heading_pos = -1
    possible_headings = ["SECTION", "ARTICLE", "RECITALS"]
    
    for possible_heading in possible_headings:
        pos = document.find(possible_heading, content_start)
        if pos != -1 and (next_heading_pos == -1 or pos < next_heading_pos):
            next_heading_pos = pos
    
    # Extract the content
    if next_heading_pos != -1:
        content = document[content_start:next_heading_pos].strip()
    else:
        content = document[content_start:].strip()
    
    return content

def extract_client_info(text, field):
    """Extract specific client information by field name."""
    if text is None or field is None:
        raise ValueError("Text and field cannot be None")
    
    if not field:
        raise ValueError("Field cannot be empty")
    
    # Find the field in the text
    field_with_colon = f"{field}:"
    field_pos = text.find(field_with_colon)
    
    if field_pos == -1:
        return ""
    
    # Find the start of value (after field and colon)
    value_start = field_pos + len(field_with_colon)
    
    # Find the end of value (next newline or end of text)
    value_end = text.find('\n', value_start)
    if value_end == -1:
        value_end = len(text)
    
    # Extract and clean the value
    value = text[value_start:value_end].strip()
    return value

def display_result(original, operation, result):
    """Display the result of a string operation."""
    print(f"\nString Operation: {operation}")
    print(f"Original Text: {original}")
    print(f"Result: {result}")

def main():
    """Main program function."""
    (case_citation, client_info, contract_section, legal_document) = initialize_legal_samples()
    
    # Create a dictionary for easy access to samples
    samples = {
        "1": ("Case Citation", case_citation),
        "2": ("Client Information", client_info),
        "3": ("Contract Section", contract_section),
        "4": ("Legal Document", legal_document)
    }
    
    while True:
        print("\n===== LEGAL STRING PROCESSOR =====")
        print("Available Samples:")
        for key, (name, _) in samples.items():
            print(f"{key}. {name}")
        
        print("\nOperations Menu:")
        print("1. Extract Case Name and Parties")
        print("2. Extract Client Information")
        print("3. Find Document Section")
        print("4. Extract Date")
        print("5. Basic String Operations")
        print("0. Exit")
        
        choice = input("Enter your choice (0-5): ")
        
        if choice == "0":
            print("Thank you for using the Legal String Processor!")
            break
        
        elif choice == "1":
            text = samples["1"][1]
            case_name = extract_case_name(text)
            display_result(text, "Extract Case Name", case_name)
            
            plaintiff, defendant = extract_parties(case_name)
            display_result(case_name, "Extract Parties", f"Plaintiff: {plaintiff}, Defendant: {defendant}")
        
        elif choice == "2":
            text = samples["2"][1]
            print("\nClient Information Fields: Client, DOB, Case #")
            field = input("Enter field to extract: ")
            
            value = extract_client_info(text, field)
            display_result(text, f"Extract {field}", value)
        
        elif choice == "3":
            text = samples["3"][1]
            print("\nAvailable Sections: SECTION 1. DEFINITIONS")
            heading = input("Enter section heading to find: ")
            
            section = find_section(text, heading)
            display_result(text, f"Find Section '{heading}'", section)
        
        elif choice == "4":
            text = samples["4"][1]
            date = extract_date(text)
            display_result(text, "Extract Date", date if date else "No date found")
        
        elif choice == "5":
            print("\nBasic String Operations:")
            print("1. Slicing")
            print("2. Case Conversion")
            print("3. Finding")
            print("4. Replacing")
            operation = input("Select operation (1-4): ")
            
            text = input("Enter text: ")
            
            if operation == "1":
                try:
                    start = int(input("Enter start index: "))
                    end = int(input("Enter end index: "))
                    sliced = text[start:end]
                    display_result(text, f"Slice [{start}:{end}]", sliced)
                except ValueError:
                    print("Indices must be integers.")
            
            elif operation == "2":
                print("1. UPPERCASE")
                print("2. lowercase")
                print("3. Title Case")
                case_op = input("Select case conversion (1-3): ")
                
                if case_op == "1":
                    display_result(text, "UPPERCASE", text.upper())
                elif case_op == "2":
                    display_result(text, "lowercase", text.lower())
                elif case_op == "3":
                    display_result(text, "Title Case", text.title())
            
            elif operation == "3":
                substring = input("Enter text to find: ")
                position = text.find(substring)
                result = f"Found at position {position}" if position != -1 else "Not found"
                display_result(text, f"Find '{substring}'", result)
            
            elif operation == "4":
                old = input("Enter text to replace: ")
                new = input("Enter replacement text: ")
                result = text.replace(old, new)
                display_result(text, f"Replace '{old}' with '{new}'", result)
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()