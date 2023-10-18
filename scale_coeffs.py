#!/usr/bin/env python3

import argparse
import os

# ./scale_coeffs.py --coeff_width=24  128tap_by20.txt

def get_parser():
    parser = argparse.ArgumentParser(description='Coefficient Munger')
    parser.add_argument('--coeff_width', type=int, required=True, help='Bitwidth of coefficients')
    parser.add_argument('filename', help="floating point coefficients to scale and quantise")
    return parser

def run_main(args):
	sf = 2**(args.coeff_width-1)-1 # Scale Factor, +ve full scale
	print(f'{os.path.split(args.filename)[0]}')
	with open(args.filename) as file:
		raw = file.read().splitlines()
	floats = [eval(i) for i in raw] # Convert from str to floats
	print(floats)
	scaled_coeffs = [i * sf for i in floats] # Scale to coeff width
	print(scaled_coeffs)
	scaled_coeffs = [round(i) for i in scaled_coeffs] # Quantise
	print(scaled_coeffs)

	# Save scaled & quantised file
	outfile = f'{os.path.split(args.filename)[0]}/{os.path.split(args.filename)[1].split(".")[0]}_scaled.txt'
	#print(outfile)
	with open(outfile, 'w') as file:
		for value in scaled_coeffs:
			file.write(f'{value}\n')
	print(f'Saved as {outfile}')


if __name__ == '__main__':
    run_main(get_parser().parse_args())