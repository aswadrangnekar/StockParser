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
Test cases for stock parser.
"""

import argparse
import csv
import os
import unittest
from parser import *

class FakeArgs(object):
    """Fake class for Initializing arguments"""
    def __init__(self, company=None, year=None, month=None, filepath=None):
        self.company = company
        self.year = year
        self.month = month
        self.filepath = filepath


class ParserTestCase(unittest.TestCase):
    """Parser test cases."""
    def setUp(self):
        self.parser = argparse.ArgumentParser(prog="Test parser",
                                              description="Test")
        self.reader = [[1990, 'Jan', 20, 15, 20],
                       [1990, 'Feb', 10, 25, 30],
                       [1991, 'Jan', 50, 25, 10]]
        self.dict_reader = [{'Year': 1990, 'Month': 'Jan', 'Company A': 20,
                             'Company B': 15, 'Company C': 20},
                             {'Year': 1990, 'Month': 'Feb', 'Company A': 10,
                             'Company B': 25, 'Company C': 30},
                             {'Year': 1991, 'Month': 'Jan', 'Company A': 50,
                             'Company B': 25, 'Company C': 10}]

    def fake_os_isfile(self, filepath):
        """Fakes os.path.isfile to notify all file paths are valid."""
        return False

    def test_validate_args_invalid_filepath(self):
        """Tests invalid filepath."""
        args = FakeArgs(company='Company A', filepath='/invalid/file/path')
        self.assertRaises(FileNotFoundException, validate_arguments, args)

    def test_validate_args_atleast_one_of_company_year_or_month(self):
        """
        Tests uesr has passed atleast one argument among company year or month.
        """
        args = FakeArgs(filepath='../csv/data.csv')
        self.assertRaises(InvalidOptionException, validate_arguments, args)

    def test_parse_company_records_for_company(self):
        """Test result is correct for a company."""
        self.assertEqual(parse_company_records(self.dict_reader, 'Company A',
                                               None, None), 50)

    def test_parse_company_records_for_company_year(self):
        """Test result is correct for a company-year."""
        self.assertEqual(parse_company_records(self.dict_reader, 'Company A',
                                               1990, None), 20)

    def test_parse_company_records_for_company_month(self):
        """Test result is correct for a company-month."""
        self.assertEqual(parse_company_records(self.dict_reader, 'Company A',
                                               None, 'Jan'), 50)

    def test_parse_monthly_or_annual_records_annual(self):
        self.assertEqual(parse_monthly_or_annual_records(self.reader,
                                                         1990, None), 30)

    def test_parse_monthly_or_annual_records_monthly(self):
        self.assertEqual(parse_monthly_or_annual_records(self.reader,
                                                         None, 'Jan'), 50)

    def test_parse_monthly_or_annual_records_for_year_month(self):
        self.assertEqual(parse_monthly_or_annual_records(self.reader,
                                                         1990, 'Jan'), 20)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ParserTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

