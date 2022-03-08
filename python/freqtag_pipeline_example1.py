"""
The freqtag pipeline: A principled approach to analyzing electrophysiological time series in frequency tagging paradigms. Part 1: Measuring the time-varying ssVEP envelope at each tagging frequency.
"""
import scipy.io

import download_examples


def main():
    exampledata_1 = load_data()
    breakpoint()


def load_data():
    """
    1-Load the 3-D file (129 electrodes x 3901 time points x 39 trials)
    - Each trial contains  400ms pre- and 7400ms post-stimulus onset;
    - During each trial, two spatially overlapping stimuli flicker at different frequencies (5 Hz and 6 Hz),
    """
    download_examples.download()
    return scipy.io.loadmat("raw/exampledata_1.mat")["data_1"]


if __name__ == "__main__":
    main()
