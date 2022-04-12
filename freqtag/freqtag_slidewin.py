import math
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

    NTrials = data.shape[-1]
    NSensors = data.shape[0]
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

    trialamp = np.empty([NSensors, NTrials])
    trialSNR = np.empty([NSensors, NTrials])
    phasestabmat = np.empty([NSensors, NTrials])

    winmat3d = np.empty([NSensors, shiftcycle, NTrials])

    print("Trial index:")

    for trial in range(NTrials):

        Data = data[:, ssvepvec, trial]
        fouriersum = None
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
            regressed_mat = freqtag_regressionMAT(regression_input)
            winmatsum += regressed_mat

            # XXX: Check first bin being different from MATLAB doesn't break anything.
            # Looks like the first bin is never accessed elsewhere in the code,
            # so it's probably OK.
            fouriermat = np.fft.fft(regressed_mat, axis=1)

            fouriercomp = fouriermat[:, targetbin].squeeze()
            if fouriersum is None:
                fouriersum = fouriercomp / np.abs(fouriercomp)
            else:
                fouriersum += fouriercomp / np.abs(fouriercomp)

            # TODO: Add plots.

        winmat = winmatsum / len(winshiftvec)
        NFFT = shiftcycle - 1
        NumUniquePoints = math.ceil(shiftcycle / 2)
        fftMat = np.fft.fft(winmat, n=NFFT, axis=1)
        Mag = _get_corrected_magnitude(fftMat)

        trialamp[:, trial] = Mag.T[targetbin]
        trialSNR[:, trial] = _get_trialSNR(Mag, targetbin)

        phasestabmat[:, trial] = np.abs(fouriersum / (winshiftstep + 1))
        winmat3d[:, :, trial] = winmat

    result = trialamp, winmat3d, phasestabmat, trialSNR
    return result


def _get_trialSNR(Mag: np.ndarray, targetbin: int) -> np.ndarray:
    """
    Returns a very crude SNR of a trial within the magnitude array.
    """
    trial = Mag.T[targetbin].squeeze()
    older_trial = Mag.T[targetbin - 2].squeeze()
    newer_trial = Mag.T[targetbin + 2].squeeze()
    older_and_newer_trials = np.stack([older_trial, newer_trial])
    mean_of_older_and_newer = np.mean(older_and_newer_trials, axis=0)
    snr = np.log10(trial / mean_of_older_and_newer) * 10

    return snr


def _get_corrected_magnitude(fftMat: np.ndarray) -> np.ndarray:
    """
    Returns the adjusted magnitudes of a complex FFT matrix.

    Corrects magnitudes by multiplying them by 2 and dividing by the total number
    of points. NOTE: Unlike in the MATLAB code, doesn't do anything more for
    the Nyquist or DC frequencies.
    """
    num_points = fftMat.shape[1]

    Mag = np.abs(fftMat)
    Mag = Mag * 2
    Mag = Mag / num_points

    return Mag
