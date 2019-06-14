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

import sys

usage = "\nUsage: INPUT.srt OUTPUT.ass\n OUTPUT is optional, the INPUT name will be used.\n\n"

# Gather data from .srt file and do some trimming, then returns a dictionary titled "subtitle_lines" 
#     structured: line_number[time_stamp, text0, text1, ... etc.]
def gather_data():
    subtitle_lines = {}
    not_EOF = True

    with open(sys.argv[1], 'r') as srt:

        while(not_EOF):

            # Grab the current line number (and do some filtering to grab the correct line number).
            line_number = ""
            line_number_unfiltered = srt.readline()
            for char in line_number_unfiltered:
                if char.isdigit():
                    line_number += char

            # Grab timestamp
            time_stamp = srt.readline()

            # Add the beginning of the Dialogue to 
            subtitle_lines[line_number] = [time_stamp[:-2]]

            # Grab the next line, and ensure it's not a new time stamp by checking if line contains only a newline.
            next_line = srt.readline()

            while next_line != "\n" and next_line != "":

                # Append new record to subtitle_lines
                subtitle_lines[line_number].append(next_line)
                next_line = srt.readline()

            # check for EOF
            if next_line == "":
                not_EOF = False    

    return(subtitle_lines)

def write_ass(OUTPUT, subtitle_lines):

    # Open default.ass header file, and write new file to OUTPUT
    try:
        with open('default.ass', 'r') as header:
            with open(OUTPUT, 'w') as out_file:
                out_file.write(header.read())
            
                for nums in range(1,len(subtitle_lines)):
                    out_line = ''

                    for i in range(len(subtitle_lines[str(nums)])):
                        if i == 0:
                            out_line += "Dialogue: 0," + subtitle_lines[str(nums)][i][1:11].replace(',','.') + ',' + subtitle_lines[str(nums)][i][18:-1].replace(',','.') + ",Default,,0,0,0,,"
                        else:
                            out_line += subtitle_lines[str(nums)][i]

                    out_line = out_line.replace("\n", "\\N")
                    if out_line[-2:] == "\\N":
                        out_file.write(out_line[:-2] + '\n')
                    else:
                        out_file.write(out_line + '\n')


    except:
        print("\nHaving trouble writing to new file...\n are you sure default.ass exists in $PATH?\n")
    

###############################
###########  MAIN  ############
###############################

def main():
    INPUT = sys.argv[1]

    # Check if user has supplied the INPUT and INPUT is .srt
    if len(sys.argv) >= 2 and INPUT[-3:] == "srt":
        try:
            OUTPUT = sys.argv[2]
        except:
            OUTPUT = sys.argv[1][:-3] + 'ass'
        write_ass(OUTPUT,gather_data())
        
    else:
        print(usage)

main()