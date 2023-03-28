#!/usr/bin/env python3

import argparse

# ./mungerV2.py --map=ACQ480_FIR_DEC10_reload_order.txt  128tap_by20.txt 128tap_by20.txt

def get_parser():
    parser = argparse.ArgumentParser(description='Coefficient Munger')
    parser.add_argument('--map', required=True, help='reorder file to apply')
    parser.add_argument('--raw_len', default=128, help='length of raw coeff')
    parser.add_argument('cfiles', nargs='+', help="files to munge")
    return parser

def run_main(args):
    coeff_order = []
    with open(args.map) as file:
        for line in file:
            coeff_order.append(int(line.split('Coefficient')[1].strip()))
    for filename in args.cfiles:
        with open(filename) as file:
            raw = file.readlines()
        coeff_len = len(coeff_order)
        padded = ["0"] * (coeff_len - int(args.raw_len / 2))
        padded.extend(raw)
        reordered = []
        for index in coeff_order:
            reordered.append(int(padded[int(index)].rstrip()))
        outname = f'{filename.split(".")[0]}_{args.map.split(".")[0]}.munged'
        with open(outname, 'w') as file:
            for value in reordered:
                file.write(f'{value}\n')
        #print(f'{filename} -> {args.map} -> {outname}')
        print(f'Saved as {outname}')

if __name__ == '__main__':
    run_main(get_parser().parse_args())
