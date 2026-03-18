#!/usr/bin/env python3
"""
extract_pdf_data.py

Extracts hourly TSA Throughput data from a large set of PDF files and creates a CSV file for each
"""

import glob
import os
import gc
import pandas as pd
import pdfplumber

# Directory containing all PDF files to process
DATA_DIRECTORY = 'tsa-throughput-raw-data'

# PDF Table configurations
BATCH_SIZE = 150  # try 100–200
TABLE_BBOX = (12, 65, 570, 770)
table_settings = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "intersection_tolerance": 5
}

def extract_pdf(pdf_path, output_path):
    """
    Extract tabulated data from the given pdf and write table data to output file in CSV format

    Parameters
    ----------
    pdf_path : str
        Path to the pdf file to extract data from
    output_path : str
        Path to the output CSV file to write tabulated data to
    """
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
    print(f"Extracting {total_pages} pages from {pdf_path}")
    first_page = True
    # Process the pages in batches to avoid over-consuming memory
    for start in range(0, total_pages, BATCH_SIZE):
       end = min(start + BATCH_SIZE, total_pages)
       print(f"\tProcessing pages {start+1}-{end}")

       # Open PDF and extract tables from page range
       with pdfplumber.open(pdf_path) as pdf:
           
           for page_number in range(start, end):
               page = pdf.pages[page_number]
               cropped = page.crop(TABLE_BBOX)
               table = cropped.extract_table(table_settings)
               if table:
                   df = pd.DataFrame(table)
                   df.to_csv(output_path,
                             index=False,
                             header=first_page,
                             mode='w' if first_page else 'a')
                   first_page = False
                   del df
               # Clean up
               del table, cropped
               gc.collect()  # force garbage collection
       # After each batch finishes, memory is released
       gc.collect()
    print(f"Finished processing PDF, saved results to {output_path}")
    return

def main():
    """
    Main execution function.
    """
    # Extract data from all PDF files in the specified directory
    for pdf_path in glob.glob(os.path.join(DATA_DIRECTORY, '*.pdf')):
        basename, _ = os.path.splitext(os.path.basename(pdf_path))
        output_path = os.path.join(DATA_DIRECTORY, f'{basename}.csv')
        extract_pdf(pdf_path, output_path)
    print(f"Finished processing all PDF files in {DATA_DIRECTORY}.")

if __name__ == "__main__":
    main()