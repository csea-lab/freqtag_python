import numpy as np
import scipy.signal

from bslcorr import bslcorr
from freqtag_regressionMAT import freqtag_regressionMAT


def freqtag_slidewin(
    data: np.ndarray,
    bslvec: np.ndarray,
    ssvepvec: np.ndarray,
    foi: float | int,
    sampnew: float | int,
    fsamp: float | int,
) -> list[np.ndarray]:
    """
    Performs a sliding window averaging analysis.

    Described in Morgan et al. 1996; Wieser % et al., 2016.

    Args:
      data:
        (m sensors, n time points, k trials) array.
        Time series of each sensor.
      bslvec:
        (p sample points) array.
        Sample points to be used for baseline subtraction.
      ssvepvec:
        (j sample points) array.
        Sample points to be used in sliding window analysis.
      foi:
        Driving frequency of interest in Hz.
      sampnew:
        New sample rate (if needed).
      fsamp:
        Sampling rate.

    Returns:
      List containing arrays in the following order:
        (m sensors, k trials) array.
          ssVEP amplitude at the frequency of interest for each trial.
        (m sensors, TODO averages, k trials) array.
          Sliding window averages for each trial in the time domain.
        (m sensors, k trials) array.
          Phase stability average of complex coefficients across moving windows.
        (m sensors, k trials) array.
          ssVEP signal-to-noise ratio in decibels at frequency of interest
          for each trial.
    """
    # TODO: Input validation.

    sampcycle = 1000 / sampnew
    tempvec = round((1000 / foi) / sampcycle)
    longvec = np.full(200, tempvec)
    winshiftvec_long = np.insert(np.cumsum(longvec) + 1, 0, 1)
    tempindexvec = np.flatnonzero(
        winshiftvec_long > (ssvepvec[-1] - ssvepvec[0]) * sampnew / fsamp
    )
    endindex = tempindexvec[0]
    winshiftvec = winshiftvec_long[: endindex - 3]

    shiftcycle = round(tempvec * 4)
    samp = 1000 / sampnew
    freqres = 1000 / (shiftcycle * samp)
    freqbins = np.arange(sampnew / 2 + freqres, step=freqres)
    min_diff_vec = np.abs(freqbins - foi)
    targetbin = np.flatnonzero(min_diff_vec == np.min(min_diff_vec))

    trialamp = []
    trialSNR = []
    phasestabmat = []

    NTrials = data.shape[-1]

    print("Trial index:")

    for trial in range(NTrials):

        Data = data[:, ssvepvec, trial]
        fouriersum = []
        print(trial)

        # TODO: Check that resampling works on various datasets.
        resampled = scipy.signal.resample(
            Data, Data.shape[-1] * sampnew // fsamp, axis=-1
        )

        datamat = bslcorr(resampled, bslvec)

        winmatsum = np.zeros((datamat.shape[0], shiftcycle))

        for winshiftstep in range(len(winshiftvec)):

            win_start = winshiftvec[winshiftstep] - 1
            win_end = win_start + shiftcycle
            index = np.arange(win_start, win_end)
            regression_input = datamat[:, tuple(index)]
            winmatsum += freqtag_regressionMAT(
                regression_input
            )

            pass

    pass
