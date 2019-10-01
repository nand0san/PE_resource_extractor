#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import pefile
import hashlib
import xlsxwriter

if __name__ == "__main__":

    # Identify specified folder with files
    dir_path = sys.argv[1]

    # Create a list of files with full path
    file_list = []
    for folder, subfolder, files in os.walk(dir_path):
        for f in files:
            full_path = os.path.join(folder, f)
            file_list.append(full_path)

    # Open XLSX file for writing
    file_name = "md5_list.xlsx"
    workbook = xlsxwriter.Workbook(file_name)
    bold = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet()

    # Write column headings
    row = 0
    worksheet.write('A1', 'MD5', bold)
    worksheet.write('B1', 'Imphash', bold)
    row += 1

    # Iterate through file_list to calculate imphash and md5 file hash
    for item in file_list:
        # Get md5
        print 'Hashing md5 of file: ' + item
        fh = open(item, "rb")
        data = fh.read()
        fh.close()
        md5 = hashlib.md5(data).hexdigest()

        # Get import table hash
        pe = pefile.PE(item)
        ihash = pe.get_imphash()

        # Write hashes to doc
        worksheet.write(row, 0, md5)
        worksheet.write(row, 1, ihash)
        row += 1

    # Autofilter the xlsx file for easy viewing/sorting
    worksheet.autofilter(0, 0, row, 2)
    workbook.close()
