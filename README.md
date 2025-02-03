# Install
```
git clone https://github.com/D-TACQ/FFIR_COEFFICIENTS.git
scp FFIR_COEFFICIENTS root@UUT:/mnt/local
```

# Preparing coefficients for FPGA FIR reload

We start from a list of floating point coefficients.

The utility scripts are used to :
- Scale the coefficients to the specified bitwidth of the target filter
- Reorder the coefficients into the bespoke order expected by the target filter

Each script performs operations on the output from the last.

# Worked example

Here we provide a trivial example which aims to demonstrate the function of the scripts.

## Example coeffs

```
acq2106_176> cat coeff.txt
1.1
2.2
3.3
4.4
5.5
6.6
7.7
8.8
9.9
10.1
```

## scale_coeffs.py

Scales and quantises floating point coefficients to N-bit fixed point coefficients

```
acq2106_176> ../scale_coeffs.py --coeff_width=2 coeff.txt
[1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.1]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Sum of coeffs = 59.6
Sum of scaled coeffs = 55
```

## convert_logical_coeffs.py

Reorders coefficients to match order specified in XXX_reload_order.txt

In this example, a simple reversal.

```
acq2106_176> cat DEMO_FIR_reload_order.txt
Reload index 0 = Coefficient 9
Reload index 1 = Coefficient 8
Reload index 2 = Coefficient 7
Reload index 3 = Coefficient 6
Reload index 4 = Coefficient 5
Reload index 5 = Coefficient 4
Reload index 6 = Coefficient 3
Reload index 7 = Coefficient 2
Reload index 8 = Coefficient 1
Reload index 9 = Coefficient 0
```

```
acq2106_176> ../convert_logical_coeffs.py --map DEMO_FIR_reload_order.txt --sym=0 coeff_scaled.txt
Saved as coeff_scaled_reordered.txt
acq2106_176> cat coeff_scaled_reordered.txt
10
9
8
7
6
5
4
3
2
1
```
