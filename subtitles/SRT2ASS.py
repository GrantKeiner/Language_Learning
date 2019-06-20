#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Grant Keiner

import re
import sys

usage = "\nUsage: INPUT.srt OUTPUT.ass\n OUTPUT is optional, the INPUT name will be used.\n\n"

# Gather data from .srt file and do some trimming, then returns a dictionary titled "subtitle_lines" 
#     structured: line_number[time_stamp, text0, text1, ... etc.]
def gather_data():
    subtitle_lines = {}
    regex = r"^(\d\d:.*)\n(.*\n.*)"
    
    with open(sys.argv[1], 'r') as srt:
        matches = re.finditer(regex, srt.read(), re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            subtitle_lines[matchNum] = list()

            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
            
                subtitle_lines[matchNum].append("{group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
    return(subtitle_lines)

def write_ass(OUTPUT, subtitle_lines):

    # Open default.ass header file, and write new file to OUTPUT
    try: 
    	# TODO: Change this up to allow custom ASS file headers
        header = open('default.ass', 'r')
    except:
        print("\nHaving trouble writing to new file...\n are you sure default.ass exists in $PATH?\n")
        
    with open(OUTPUT, 'w') as out_file:
        out_file.write(header.read())
        header.close()
    
        for nums in range(1,len(subtitle_lines)+1):
            out_file.write("Dialogue: 0," + subtitle_lines[nums][0][1:11].replace(',','.') + ',' + subtitle_lines[nums][0][18:-2].replace(',','.') + ",Default,,0,0,0,,"+ str(subtitle_lines[nums][1]).replace('\n','\\N')+'\n')

    

###############################
###########  MAIN  ############
###############################

def main():
    # Check if user has supplied the INPUT and INPUT is .srt
    try:
        INPUT = sys.argv[1]
    except:
        print(usage)

    if len(sys.argv) >= 2 and INPUT[-3:] == "srt":
        
        try:
            OUTPUT = sys.argv[2]
        except:
            OUTPUT = sys.argv[1][:-3] + 'ass'

        write_ass(OUTPUT,gather_data())
        
    else:
        print(usage)

main()