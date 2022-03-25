"""
The freqtag pipeline: A principled approach to analyzing electrophysiological
time series in frequency tagging paradigms.

Part 2: Measuring the ssVEP mplitude from single trials, using sliding window averaging.
"""
import download_examples
import scipy.io


SAMPLE_RATE = 500


def main():
    # 1-Load the 3-D file (109 electrodes x 2500 time points x 15 trials)
    download_examples.download()
    exampledata_2 = scipy.io.loadmat("raw/exampledata_2.mat")["data_2"]


if __name__ == "__main__":
    main()
