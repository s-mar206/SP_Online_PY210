#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import tempfile
from mailroom4 import *


#  Build our data structure to use in these tests

donor_db = {}  # dict that contains user/donation records
donor_db = populate_data()


'''
Lesson 6: Writing Unit Tests

'''


'''
Send Thank You tests
'''


def test_format_email():
    # test normal case for generating mail text
    assert format_email("James Butts", 100.00, 1000.00) == ''.join((
            "Dear James Butts,\n\n",
            "Thank you for your recent contribution of $100.00.\n\n",
            "We appreciate your generosity in support of our mission.\n\n",
            "Thank you for your lifetime contributions of $1000.00.\n\n"
            "Warmest Regards,\n\n",
            "Charity Staff\n"))

    # test for number formatting in mail text
    assert format_email("Joe Biden", 10000.9999, 1000.1) == ''.join((
            "Dear Joe Biden,\n\n",
            "Thank you for your recent contribution of $10001.00.\n\n",
            "We appreciate your generosity in support of our mission.\n\n",
            "Thank you for your lifetime contributions of $1000.10.\n\n"
            "Warmest Regards,\n\n",
            "Charity Staff\n"))

#  Test add_contribution()

#  Add contribution for a new donor
def test_add_contribution():
    add_contribution("James Butts", 100)
    assert donor_db["James Butts"][-1:] == [100]
    # Test that we are summing total contributions correctly
    assert sum(donor_db["James Butts"]) == 100


    #  Pass a contribution to a recurring donor
    add_contribution("Daenerys Targaryen", 100)
    assert donor_db["Daenerys Targaryen"][-1:] == [100]
    # Test that we are summing total contributions correctly
    assert sum(donor_db["Daenerys Targaryen"]) == 8355.00

    # Pass multiple contributions to a recurring donor
    add_contribution("Daenerys Targaryen", [100, 200])
    assert donor_db["Daenerys Targaryen"][-2:] == [100, 200]
    # Test that we are summing total contributions correctly for multiple contributions
    assert sum(donor_db["Daenerys Targaryen"]) == 8655.00

# Test listing of donors
def test_list_donors():
    # Test formatting and sorting of the dictionary when listing donors
    assert str(list_donors()).split("\n")[0] == "No.  Name   "
    assert str(list_donors()).split("\n")[1] == "==== ======="
    assert str(list_donors()).split("\n")[2] == "1    Arya Stark"


'''
Create Report tests
'''

def test_show_donors():
    #  Check calculations
    #  Number of donations
    assert len(donor_db["Melisandre"]) == 4
    #  Total donations
    assert sum(donor_db["Melisandre"]) == 300019.00
    #  Average donation
    assert sum(donor_db["Melisandre"]) / len(donor_db["Melisandre"]) == 75004.75

def test_get_donors_details():
    #  Check output and formating of get_donor_details()
    donor_list = get_donors_details()
    assert donor_list[1] == 'Arya Stark               $10899.92           5         $2179.98      \n'


'''
Send Letters tests
'''

#  Run the code in question to generate letters


def test_file_created():
    send_letter_to_all()
    file_to_test = tempfile.gettempdir() + "/James_Butts.txt"
    #  Make sure letters are getting created (written to temp)
    assert os.path.exists(file_to_test)



def test_get_letter_text():
    send_letter_to_all()
    letter_text = ""
    tempfilepath = tempfile.gettempdir() + "/James_Butts.txt"
    with open(tempfilepath, "r") as letter_file:
        letter_text = letter_file.readlines()
        letter_text = "".join(letter_text)
        print(letter_text)
        print(''.join(("Dear James Butts,\n\n",
        "Thank you for your recent contribution of $100.00.\n\n",
        "We appreciate your generosity in support of our mission.\n\n",
        "Thank you for your lifetime contributions of $100.00.\n\n",
        "Warmest Regards,\n\n",
        "Charity Staff\n")))
    assert letter_text == ''.join(("Dear James Butts,\n\n",
        "Thank you for your recent contribution of $100.00.\n\n",
        "We appreciate your generosity in support of our mission.\n\n",
        "Thank you for your lifetime contributions of $100.00.\n\n",
        "Warmest Regards,\n\n",
        "Charity Staff\n"))