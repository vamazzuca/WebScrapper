# ----------------------
# Name: Vittorio Mazzuca
# Program: tabulate.py
# ----------------------

import math
import urllib.request

def main():
    info_dict = retrieve_customer_table()
    info_dict = call_table_calc(info_dict)
    print_table(info_dict)


def retrieve_customer_table():
    url = "https://webdocs.cs.ualberta.ca/~kondrak/cmput175/customer_table.html"
    page = urllib.request.urlopen(url)
    encoding = page.headers.get_content_charset()
    info_dict = {}
    
    for line in page:
        line = line.decode(encoding)
        if "<tr>" in line:
            info_list = line.split("</td>")
            info_dict[info_list[0][8:]] = [""]
            info_dict[info_list[0][8:]].extend((info_list[1][4:], 
                                                0,[0,0,0],0.0))

    return info_dict


def call_table_calc(info_dict):
    url = "https://webdocs.cs.ualberta.ca/~kondrak/cmput175/call_table.html"
    page = urllib.request.urlopen(url)
    encoding = page.headers.get_content_charset()
    
    for line in page:
        line = line.decode(encoding)
        if "<tr>" in line:
            info_list = line.split("</td>")
            phone_num = info_list[2][4:]
            info_dict = call_amount(info_dict, info_list)
            info_dict = duration_due_update(info_dict, info_list)
    
    info_dict = format_duration(info_dict)
    info_dict = char_assign(info_dict)
            
    return info_dict

          
def call_amount(info_dict, info_list):
    call_num = info_dict[info_list[1][4:]][2]
    call_num += 1
    info_dict[info_list[1][4:]][2] = call_num
    return info_dict


def duration_due_update(info_dict, info_list):
    duration = info_dict[info_list[1][4:]][3]
    duration[2] += int(info_list[3][4:])
    info_dict = due_calc(info_dict, info_list, int(info_list[3][4:]))
    
    while duration[2] >= 60:
        duration[1] += 1
        duration[2] = (duration[2] - 60)
        
    while duration[1] >= 60:
        duration[0] += 1
        duration[1] = (duration[1] - 60)
    
    info_dict[info_list[1][4:]][3] = duration
    return info_dict


def due_calc(info_dict, info_list, duration):
    minutes = 0
    while duration >= 60:
        minutes += 1
        duration -= 60
    if duration != 0:
        minutes += 1
    
    due = info_dict[info_list[1][4:]][4]
    rate = float(info_list[4][4:])
    total = due + (minutes * rate)
    info_dict[info_list[1][4:]][4] = round(total, 2)
    return info_dict


def format_duration(info_dict):
    for key in info_dict:
        if len(str(info_dict[key][3][2])) != 2:
            sec = "0" + str(info_dict[key][3][2])
            info_dict[key][3][2] = sec
        if len(str(info_dict[key][3][1])) != 2:
            mins = "0" + str(info_dict[key][3][1])
            info_dict[key][3][1] = mins
    return info_dict


def char_assign(info_dict):
    for key in info_dict:
        if (info_dict[key][4] > 850.0):
            info_dict[key][0] = "**"
        if (info_dict[key][4] <= 850.0) and (info_dict[key][2] > 350):
            info_dict[key][0] = "++"
    return info_dict
                   
    
def print_table(info_dict):
    num_list = []
    for key in info_dict:
        num_list.append(int(key))
    num_list.sort()
    total = total_calc(info_dict)
    top_block = """\
+--------------+------------------------------+---+---------+--------+
| Phone number | Name                         | # |Duration | Due    |
+--------------+------------------------------+---+---------+--------+ """
    print(top_block)
    for num in num_list:
        num = str(num)
        space = 30 - len(info_dict[num][1])
        print("|({}) {} {}|{:30s}|{}|{}h{}m{}s|${:7}|{}".format(
              num[0:3], num[3:6], num[6:10], info_dict[num][1], 
              info_dict[num][2], info_dict[num][3][0], info_dict[num][3][1],
              info_dict[num][3][2], info_dict[num][4], info_dict[num][0]))
    bottom_block = """\
+--------------+------------------------------+---+---------+--------+
| Total dues   |                                          ${:10}|
+--------------+-----------------------------------------------------+ """
    print(bottom_block.format(total))

def total_calc(info_dict):
    total = 0.0
    for key in info_dict:
        total += info_dict[key][4]
    return round(total, 2)


              
    
main()