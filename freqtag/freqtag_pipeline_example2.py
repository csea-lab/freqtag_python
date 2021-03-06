"""
The freqtag pipeline: A principled approach to analyzing electrophysiological
time series in frequency tagging paradigms.

Part 2: Measuring the ssVEP mplitude from single trials, using sliding window averaging.
"""
import scipy.io
import numpy as np

import download_examples
from freqtag_FFT import freqtag_FFT
from freqtag_FFT3D import freqtag_FFT3D
from freqtag_slidewin import freqtag_slidewin
from freqtag_simpleSNR import freqtag_simpleSNR


SAMPLE_RATE = 500


def main():
    # 1-Load the 3-D file (109 electrodes x 2500 time points x 15 trials)
    download_examples.download()
    exampledata_2 = scipy.io.loadmat("raw/exampledata_2.mat")["data_2"]

    # 2-Data visualization and check in the frequency domain
    mean_exampledata = np.mean(exampledata_2, 2)
    amp, phase, freqs, fftcomp = freqtag_FFT(mean_exampledata, SAMPLE_RATE)
    # TODO: Add plots for this section.

    # 3-Run FFT on single-trials and plot the results
    amp_st, freqs_st, fftcomp_st = freqtag_FFT3D(exampledata_2, SAMPLE_RATE)
    # TODO: Add plots for this section.

    # 4-Run a sliding window analysis
    vector = np.arange(2500)
    trialamp5Hz, winmat3d5Hz, phasestabmat5Hz, trialSNR5Hz = freqtag_slidewin(
        exampledata_2, vector, vector, 5, 500, SAMPLE_RATE
    )
    trialamp6Hz, winmat3d6Hz, phasestabmat6Hz, trialSNR6Hz = freqtag_slidewin(
        exampledata_2, vector, vector, 6, 600, SAMPLE_RATE
    )

    # 5-Examining and using the outputsfreqtag_slidewin
    # TODO: Add plotting capabilities to freqtag_slidewin.

    # There are almost no numbered labels on the remaining sections of the MATLAB
    # pipeline. I'm not sure what to port over aside from the freqtag_simpleSNR
    # function, so that's the last thing I'll do for now.
    meanwinmat = np.mean(winmat3d6Hz, 2)
    amp6Hz, phase6Hz, freqs6Hz, fftcomp6Hz = freqtag_FFT(meanwinmat, 600)
    SNRdb6Hz, SNRratio6Hz = freqtag_simpleSNR(amp6Hz, [3, 5, 7])


if __name__ == "__main__":
    main()
