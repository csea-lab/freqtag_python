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
from freqtag_HILB import freqtag_HILB


SAMPLE_RATE = 500


def main():
    # 1-Load the 3-D file (129 electrodes x 3901 time points x 39 trials)
    download_examples.download()
    exampledata_1 = scipy.io.loadmat("raw/exampledata_1.mat")["data_1"]

    # TODO: 2-Plot the data, averaging the trials

    # 3-Define frequency axis and prepare spectral analysis, see section 3.1
    data_ssvep = exampledata_1[:, 700:3700, :]
    faxisall = np.arange(0, 250, 0.1667)
    faxis = faxisall[:196]

    # 4-Run a Discrete Fourier Transform on the data
    mean_ssvep = np.mean(data_ssvep, 2)
    amp, phase, freqs, fftcomp = freqtag_FFT(mean_ssvep, SAMPLE_RATE)

    # TODO: 6-Plot the FFT results

    # 7-Run FFT on single-trials
    amp_st, freqs_st, fftcomp_st = freqtag_FFT3D(data_ssvep, SAMPLE_RATE)

    # TODO: 8-Plot the FFT on single trials results

    # 9-Run Hilbert Transform
    mean_exampledata_1 = np.mean(exampledata_1, axis=2)
    amp5, phase5, complex5 = freqtag_HILB(
        mean_exampledata_1, 5, 10, 75, True, SAMPLE_RATE
    )
    amp6, phase6, complex6 = freqtag_HILB(
        mean_exampledata_1, 6, 10, 75, True, SAMPLE_RATE
    )

    # TODO: 10-Plot the Hilbert Transform results


if __name__ == "__main__":
    main()
