# PDF Data Extraction and MySQL Insertion

This project extracts data from a PDF file and inserts it into a MySQL database using Python. The data extraction is performed using the PyMuPDF library (fitz), and the data is inserted into a MySQL database using the mysql-connector-python library.

## Features

- Extracts IRIN numbers, acknowledgment numbers, and invoice numbers from specific pages of a PDF document.
- Inserts the extracted data into a MySQL database.
- Handles different patterns for various data types across multiple pages.

## Prerequisites

- Python 3.x
- MySQL server
- Required Python libraries:
  - `PyMuPDF`

## Installing the Libraries
pip install PyMuPDF
pip install Fitz
pip install PyMuPDF mysql-connector-python

- Set up the MySQL database
- Update the pdf_filename variable in the script to point to your PDF file
- Update MySQL connection settings



