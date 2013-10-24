#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2011 Aswad Rangnekar <aswad.r@gmail.com>
# Copyright 2012 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Stock parser:
Parses a csv if a specified format amd prompts max stock price.
A sample data is provided in csv folder.
"""

import argparse
import csv
import os
import sys

# Exit codes to signal user.
ERROR_FILE_NOT_FOUND = 1
ERROR_INVALID_OPTIONS = 2
ERROR_DATA_NOT_FOUND = 3


class FileNotFoundException(Exception):
    """Raised if target file is not found."""
    def __init__(self, message):
        """intializes exception"""
        Exception.__init__(self, message)
        self.exit_status = ERROR_FILE_NOT_FOUND
        self.message = message


class InvalidOptionException(Exception):
    """Raised if user passes invalid arguments/options."""
    def __init__(self, message):
        """intializes exception"""
        Exception.__init__(self, message)
        self.exit_status = ERROR_INVALID_OPTIONS
        self.message = message


class DataNotFoundException(Exception):
    """Raised if expected result data is not found."""
    def __init__(self, message):
        """intializes exception"""
        Exception.__init__(self, message)
        self.exit_status = ERROR_DATA_NOT_FOUND
        self.message = message


def parse_company_records(reader, company, year, month):
    """Finds maximum stock price for a company annualy or monthly."""
    result = None
    for row in reader:
        if year and row['Year'] != year:
            # skip unwanted data
            continue
        elif month and row['Month'] != month:
            # skip unwanted data
            continue
        else:    
            result = max([result, row.get(company)])
    return result


def parse_monthly_or_annual_records(reader, year, month):
    """Finds maximum stock price annualy or monthly or year-month."""
    result = None
    for row in reader:
        year_data, month_data = row[:2]

        if year and year_data != year:
            # skip unwanted data
            continue
        elif month and month_data != month:
            # skip unwanted data
            continue
        else:
            # Append result if it requires to parse multiple rows
            if result:
                row.append(result)

            result = max(row[2:])
            
    return result


def get_max(company, year, month, filepath):
    """Parse data from csv."""
    with open(filepath, 'rb') as data:
        field_names = data.next().replace('\n', '').split(',')

        if company and company not in field_names:
            msg = 'No data about company "%s" in "%s"' % (company, filepath)
            raise DataNotFoundException(msg)

        if company:
            reader = csv.DictReader(data, fieldnames=field_names,
                                    quotechar="\n")
            result = parse_company_records(reader, company, year, month)
        else:
            reader = csv.reader(data, quotechar="\n")
            result = parse_monthly_or_annual_records(reader, year, month)
    
        return result


def validate_arguments(args):
    """Validates arguments passed by user."""
    if not os.path.isfile(args.filepath):
        msg = "Error: File not found %s" %args.filepath
        raise FileNotFoundException(msg)

    if not (args.company or args.year or args.month):
        raise InvalidOptionException("Error: Atleast one option amongst"
                                     "-c, -y or -m  is required")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=__file__, description=__doc__)
    parser.add_argument('-c', '--company', help='Company name')
    parser.add_argument('-y', '--year', help='Year')
    parser.add_argument('-m', '--month', help='Month')
    parser.add_argument('-f', '--filepath', help='File path', required=True)
    args = parser.parse_args()

    try:
        validate_arguments(args)
        max_price = get_max(args.company, args.year, args.month, args.filepath)
        print "Max: %s" %(max_price or 'No data found.')
    except (FileNotFoundException, InvalidOptionException,
            DataNotFoundException) as ex:
        print ex.message
        sys.exit(ex.exit_status)
