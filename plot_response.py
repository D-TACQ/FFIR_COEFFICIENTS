#!/usr/bin/python3

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import os,sys;
import argparse

def get_parser():
    parser = argparse.ArgumentParser(description='Visualise Coefficient Response')
    parser.add_argument('--coeff_width', type=int, required=True, help='Bitwidth of coefficients')
    parser.add_argument('cfile', help="file containing floating point coefficient set")
    return parser


def plot_response(fs, w, h, title, numtaps, color="b"):
    plt.figure()
    if numtaps == 24 or color == "r":
        plt.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)),'r')
    else:
        plt.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)))
    plt.ylim(-200, 5)
    plt.xlim(0, 0.5*fs)
    plt.grid(True)
    if fs > 1:
        plt.xlabel('Frequency (fs)')
    else:
        plt.xlabel('Normalised Frequency (fs)')
    plt.ylabel('Gain (dB)')
    plt.title(title)

def plot_phase_response(fs, w, h, title, numtaps, ymin=0, color="k"):
    plt.figure()
    unw_angle = np.unwrap(np.angle(h))
    if numtaps == 24 or color == "r":
        plt.plot(0.5*fs*w/np.pi, unw_angle*180/np.pi, 'r')
        #plt.plot(0.5*fs*w/np.pi, unw_angle),'r') #rads
    else:
        plt.plot(0.5*fs*w/np.pi, unw_angle*180/np.pi, 'k')
        #plt.plot(0.5*fs*w/np.pi, unw_angle, 'k') # rads

    if ymin < 0 :
        print(ymin + 0.1*ymin)
        plt.ylim(ymin + 0.1*ymin, 5)

    plt.xlim(0, 0.5*fs)
    plt.grid(True)
    if fs > 1:
        plt.xlabel('Frequency (Hz)')
    else:
        plt.xlabel('Normalised Frequency (fs)')
    plt.ylabel('Phase (Deg)')
    plt.title(title)

def plot_impulse(b,a=1):
    l = len(b)
    impulse = np.repeat(0.,l); impulse[0] =1.
    x = np.arange(0,l)
    response = signal.lfilter(taps,a,impulse)
    step = np.cumsum(response)
#    plt.stem(x, step)
    plt.plot(x, step)
    plt.ylabel('Amplitude')
    plt.xlabel(r'n (samples)')
    plt.title(r'Step response')

######################################################################################

def run_main(args):
    sf = 2**(args.coeff_width-1)-1 # Scale Factor, +ve full scale
    print(f'{os.path.split(args.cfile)[0]}')
    with open(args.cfile) as file:
        raw = file.read().splitlines()
    floats = [eval(i) for i in raw] # Convert from str to floats
    
    numtaps=len(raw)
    taps=floats
    fs=1
    
    # ## Scale the Filter
    sumcoeffs = np.sum(taps)
    scaletaps  = np.empty_like(taps)
    scaletaps = taps/sumcoeffs*sf
    scaletaps = np.round(scaletaps)
    print(scaletaps)
    # #scaletaps[:] = (taps/sumcoeffs)*2048
    # #scaletaps = np.round(scaletaps)
    # scaletaps = scaletaps.astype(int)
    # scaletaps_hex = scaletaps & 0xffffffff
    # #scaletaps[:] = (taps/sumcoeffs)*1
    # sumcoeffs2 = np.sum(scaletaps)
    
    if os.path.split(args.cfile)[0] == "": # If file is in local dir
        outfile = f'{os.path.split(args.cfile)[1].split(".")[0]}'
    else: # Put the file back from whence it came
        outfile = f'{os.path.split(args.cfile)[0]}/{os.path.split(args.cfile)[1].split(".")[0]}'

    #w1, h1 = signal.freqz(scaletaps/coeff_factor, [1], worN=2000)
    w1, h1 = signal.freqz(taps, [1], worN=512)
    plot_title="Frequency Response"
    plot_response(fs, w1, h1, plot_title, numtaps, "r")
    fig_file = f'{outfile}_freq_resp.pdf'
    plt.savefig(fig_file,format='pdf')

    # Plot quantised result
    w2, h2 = signal.freqz(scaletaps/sf, [1], worN=512)
    plot_title="Quantised Frequency Response"
    plot_response(fs, w2, h2, plot_title, numtaps, "b")
    fig_file = f'{outfile}_freq_resp_quant.pdf'
    plt.savefig(fig_file,format='pdf')

    plt.show()
    
    #plot_phase_response(fs, w1, h1, plot_title, numtaps, ymin=ymin,color="r")
    #plt.show()

if __name__ == '__main__':
    run_main(get_parser().parse_args())




