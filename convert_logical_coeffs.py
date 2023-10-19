#!/usr/bin/env python3

import argparse
import os

"""
Usage:
    ./convert_logical_coeffs.py ACQ480_FIR_DEC10_reload_order.txt  128tap_by20.txt --sym=1
    ./convert_logical_coeffs.py GA_FIR_BLOCK_reload_order.txt 28_Asymm_coeffs.txt --sym=0
"""

#    Symmetric coefficients imply that we will only load the first half of coefficients to the filter.
#    N.B! One must refer to the filter architecture to determine whether or not it is expecting symmetric coefficients
#    Any optimisations that can be applied when using symmetric coefficients are selected at FPGA compile time

#    e.g. If NTAPS = 180, cfile has 180 entries, then the reordered output will have only 90 entries,
#    reordered to match the map file (which should also have 90 entries)

def get_parser():
    parser = argparse.ArgumentParser(description='Coefficient Munger')
    parser.add_argument('--map', required=True, help='reorder file to apply')
    parser.add_argument('cfiles', nargs='+', help="files to munge")
    parser.add_argument('--sym', required=True, type=int, help='symmetric coefficient?')
    return parser

def run_main(args):
    order = []
    with open(args.map) as file:
        for line in file:
            value = line.split('Coefficient')[-1].strip()
            if value:
                order.append(int(value))

    for filename in args.cfiles:

        input = []
        with open(filename) as file:
            for line in file:
                input.append(int(line.strip()))

        order_len = len(order)
        input_len = len(input)
        padded = [0] * (order_len - int(input_len / (args.sym + 1)))

        if args.sym:
            padded = padded + input 
        else:
            padded = input + padded

        output = []
        for input_idx in order:
            output.append(padded[input_idx])

        outname = os.path.join(os.path.split(filename)[0], f"{os.path.split(filename)[1].split('.')[0]}_reordered.txt")
        with open(outname, 'w') as file:
            for value in output:
                file.write(f'{value}\n')

        #print(f'{filename} -> {args.order[0]} -> {outname}')
        print(f'Saved as {outname}')

if __name__ == '__main__':
    run_main(get_parser().parse_args())
