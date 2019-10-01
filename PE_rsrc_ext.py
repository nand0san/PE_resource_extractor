#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pefile
import hashlib
import xlsxwriter
import errno


# Declare name of section to export from PE files
resource_name = 'PSEXESVC'
expected_resource_type_to_export = '.exe'

# Identify folder containing PE files
dir_path = 'pe_files_dir'


# Prepare xlsx file
# Open XLSX file for writing
print 'Opening new XLSX file.'

file_name = "resources_hash_list.xlsx"
workbook = xlsxwriter.Workbook(file_name)
bold = workbook.add_format({'bold': True})
worksheet = workbook.add_worksheet()

# Write column headings
row = 0
worksheet.write('A1', 'PE file', bold)
worksheet.write('B1', 'md5 of internal resource', bold)
row += 1


def write_row(item, src_hash, _row):
    # Write hashes to xlsx
    worksheet.write(row, 0, item)
    worksheet.write(row, 1, src_hash)
    _row += 1
    return _row


def pe_resource_extract(item, _resource_name):
    print item
    pe = pefile.PE(item)
    # malcfg_data = ''
    offset = 0x0
    size = 0x0
    for rsrc in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        for entry in rsrc.directory.entries:
            if entry.name is not None:
                if entry.name.__str__() == _resource_name:
                    offset = entry.directory.entries[0].data.struct.OffsetToData
                    size = entry.directory.entries[0].data.struct.Size
    malcfg_data = pe.get_memory_mapped_image()[offset:offset + size]
    return malcfg_data


def dump_to_file(filename, data):
    filename = 'extracted\\' + filename
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, 'wb') as f:
        f.write(data)


def get_md5(item):
    print 'Hashing md5: ' + item
    fh = open(item, "rb")
    data = fh.read()
    fh.close()
    md5_hash = hashlib.md5(data).hexdigest()
    # print md5_hash
    return md5_hash


# main
def main():

    # Create a list of files with full path added
    file_list = []
    for folder, subfolder, files in os.walk(dir_path):
        for f in files:
            full_path = os.path.join(folder, f)
            file_list.append(full_path)
    counter = 0
    _row = 1
    for item in file_list:
        try:
            print 'Extracting from... ' + item
            embedded_bin = pe_resource_extract(item, resource_name)
            # print embedded_bin
            # formating extracted filename
            con = str(counter).zfill(2)
            item_name = os.path.basename(item)
            filename = item_name + '_' + resource_name + '_' + con + expected_resource_type_to_export
            counter = counter + 1

            dump_to_file(filename, embedded_bin)

            src_hash = get_md5(item)

            # write_row(item, src_hash, row)

            # Write hashes to xlsx
            worksheet.write(_row, 0, item)
            worksheet.write(_row, 1, src_hash)
            _row += 1

        except IOError:
            print' error IO'


if __name__ == '__main__':
    main()

    # Autofilter the xlsx file for easy viewing/sorting
    worksheet.autofilter(0, 0, row, 2)
    workbook.close()
