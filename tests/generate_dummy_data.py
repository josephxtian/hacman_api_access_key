# Uses xeger to generate test dummy data.
# xeger uses standard regex expressions
# exports to csv file

import csv
from xeger import Xeger

csv_filename = 'dummy_data.csv'
number_of_lines = 50
headers = ["key_id","tool_id","announce_name","id"]

x = Xeger()
count = 0
fob_id = "e85d2h4s"

def fob_id_func():
    fob_id = x.xeger("([0-9a-z]){8}")
    print(fob_id)
    return fob_id

def pin_id_func():
    pin_id = x.xeger("ff([0-9]){8}")
    print(pin_id)
    return pin_id

def announce_name_func():
    announce_name = x.xeger("[😀0-9a-zA-Z]{0,20}")
    print(announce_name)
    return announce_name

def member_id_func():
    member_id = x.xeger("[0-9]{1,3}")
    print(member_id)
    return member_id

with open(csv_filename,'w',newline='') as csvfile:
    dummy_writer = csv.writer(csvfile, delimiter=',')
    dummy_writer.writerow(headers)
    while count < number_of_lines:
        # check if previous fob_id had 'b' in it.
        # if it did, generate a pin code, for randomness
        if fob_id.find('b') >= 0:
            fob_id = pin_id_func()
        else:
            fob_id = fob_id_func()
        announce_name = announce_name_func()
        member_id = member_id_func()

        dummy_writer.writerow([fob_id,announce_name,member_id])
        count += 1