import os
import fitz  # PyMuPDF
import re
import mysql.connector

def extract_from_pdf_and_insert_to_mysql(pdf_filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(script_dir, pdf_filename)

    pdf_document = fitz.open(pdf_path)

    irin_list = []
    ack_no_list = []
    invoice_list = []

    patterns = [
        r'[0-9a-fA-F]{24}',  # IRIN number (page 1)
        r'[A-Z]{2}/[A-Z]{4}/[A-Z]{2}/[0-9]{3}/[0-9]{2}-[0-9]{2}',  # Invoice number (page 2)
        r'[A-Z]{3}-[0-9]{8}',  # Bill number (page 3)
        r'[0-9]{13}',  # Acknowledgment number (page 4)
        r'\b255\b',  # Specific Invoice number (page 5)
        r'\b552\b',  # Specific Invoice number (page 6)
        r'Invoice\s*No\s*[:]*\s*(IN\d+)',  # Invoice number (page 7)
    ]

    # Establish MySQL connection
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="liki",
        database="invoices",
        auth_plugin="mysql_native_password"
    )
    cursor = db_connection.cursor()

    # Iterate through each page and extract data
    for page_number, pattern in enumerate(patterns, start=1):
        page = pdf_document.load_page(page_number - 1)
        page_text = page.get_text()

        matches = re.findall(pattern, page_text)

        if page_number == 1:
            if matches:
                irin_list.append(matches[0])
                print(f"Page {page_number}: IRIN number - {matches[0]}")
        elif page_number == 2:
            invoice_list.extend(matches)
            print(f"Page {page_number}: Invoice number - {matches}")
        elif page_number == 3:
            print(f"Page {page_number}: Bill number - {matches}")
        elif page_number == 4:
            if matches:
                ack_no_list.append(matches[0])
                print(f"Page {page_number}: Acknowledgment number - {matches[0]}")
        elif page_number in [5, 6, 7]:
            invoice_list.extend(matches)
            print(f"Page {page_number}: Invoice number - {matches}")

    # Insert data into MySQL
    try:
        # Insert IRIN and Ack_No data
        for irin in irin_list:
            ack_no = ack_no_list[0] if ack_no_list else None
            insert_query = "INSERT INTO extracted_values (IRIN, Ack_No) VALUES (%s, %s)"
            cursor.execute(insert_query, (irin, ack_no))
        
        # Insert Invoice data
        for invoice in invoice_list:
            insert_query = "INSERT INTO extracted_invoices (Invoice) VALUES (%s)"
            cursor.execute(insert_query, (invoice,))

        # Commit changes
        db_connection.commit()
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        # Close resources
        pdf_document.close()
        cursor.close()
        db_connection.close()

    return irin_list, ack_no_list, invoice_list

# PDF file name
pdf_filename = "C:/Users/likit/Downloads/invoices (1).pdf"

# Perform extraction and insert to MySQL
irin_values, ack_no_values, invoice_values = extract_from_pdf_and_insert_to_mysql(pdf_filename)


