"""
The freqtag pipeline: A principled approach to analyzing electrophysiological
time series in frequency tagging paradigms. Part 1: Measuring the time-varying
ssVEP envelope at each tagging frequency.
"""
import numpy as np
import scipy.io
import download_examples
from freqtag_FFT import freqtag_FFT
from freqtag_FFT3D import freqtag_FFT3D


SAMPLE_RATE = 500


def main():
    # 1-Load the 3-D file (129 electrodes x 3901 time points x 39 trials)
    download_examples.download()
    exampledata_1 = scipy.io.loadmat("raw/exampledata_1.mat")["data_1"]

    # 3-Define frequency axis and prepare spectral analysis, see section 3.1
    data_ssvep = exampledata_1[:, 700:3700, :]
    faxisall = np.arange(0, 250, 0.1667)
    faxis = faxisall[:196]

    # 4-Run a Discrete Fourier Transform on the data
    mean_ssvep = np.mean(data_ssvep, 2)
    amp, phase, freqs, fftcomp = freqtag_FFT(mean_ssvep, SAMPLE_RATE)

    # 7-Run FFT on single-trials
    amp, freqs, fftcomp = freqtag_FFT3D(data_ssvep, 500)


if __name__ == "__main__":
    main()
