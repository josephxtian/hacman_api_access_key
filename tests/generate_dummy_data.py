# Uses xeger to generate test dummy data.
# xeger uses standard regex expressions
# exports to three csv files
# dev_doorbot_lines.csv - doorbot sample
# dev_toolbot_lines.csv - toolbot sample
# dev_tool_api_keys.csv - api keys for toolbot verification

import csv
from random import randint, sample
from xeger import Xeger

num_of_doorbot_lines = 50
tool_ids = ['001','062','077','496']
duplicate_list_for_pin_codes = True

count = 0
x = Xeger()
# starter fob_id
fob_id = "e85d2h4s"

y = Xeger(limit=8)

def fob_id_func():
    fob_id = x.xeger("([0-9a-z]){8}")
    return fob_id

def pin_id_func():
    pin_id = x.xeger("ff([0-9]){8}")
    return pin_id

def announce_name_func():
    announce_name = x.xeger("[😀0-9a-zA-Z]{0,20}")
    return announce_name

def member_id_func():
    member_id = x.xeger("[0-9]{1,3}")
    return member_id

with open("dev_doorbot_lines.csv",'w',newline='') as doorbot_file:
    doorbot_writer = csv.writer(doorbot_file, delimiter=',')
    doorbot_writer.writerow(["fob_id","announce_name","id"])
    with open("dev_toolbot_lines.csv",'w',newline='') as toolbot_file:
        toolbot_writer = csv.writer(toolbot_file, delimiter=',')
        toolbot_writer.writerow(["fob_id","tool_id","announce_name","id"])
        while count < num_of_doorbot_lines:
            # check if previous fob_id had 'b' in it.
            # if it did, generate a pin code, for randomness
            fob_id = fob_id_func()
            announce_name = announce_name_func()
            member_id = member_id_func()
            doorbot_writer.writerow([fob_id,announce_name,member_id])

            num_of_tools_inducted_on = randint(0,len(tool_ids))
            selected_tool_ids = sample(tool_ids,num_of_tools_inducted_on)
            for tool_id in selected_tool_ids:
                toolbot_writer.writerow([fob_id,tool_id,announce_name,member_id])

            if fob_id.find('b') >= 0:
                fob_id = pin_id_func()
                doorbot_writer.writerow([fob_id,announce_name,member_id])
                count += 1
                if duplicate_list_for_pin_codes:
                    for tool_id in selected_tool_ids:
                        toolbot_writer.writerow([fob_id,tool_id,announce_name,member_id])

            count += 1
        print("Created dev_doorbot_lines.csv")
        print("Created dev_toolbot_lines.csv")

    with open("dev_tool_api_keys.csv",'w',newline='') as tool_api_file:
        dummy_writer = csv.writer(tool_api_file, delimiter=',')
        dummy_writer.writerow(["tool_id","api_key"])
        for tool_id in tool_ids:
            dummy_writer.writerow([tool_id,y.xeger("[0-9A-Za-z]{8}")])
        print("Created dev_tool_api_keys.csv")