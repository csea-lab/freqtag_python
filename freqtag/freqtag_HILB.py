import numpy as np
import scipy.signal


def freqtag_HILB(
    data: np.ndarray, taggingfreq: float | int, filterorder: int, fsamp: float | int
) -> list[np.ndarray]:
    """
    Implements a simple filter-Hilbert analysis of a 2D array of EEG data.

    It outputs the time-varying ssVEP amplitude, the time-varying phase, and
    the complex (real and imaginary) components of the time-varying response,
    at the tagging frequency for each time point. If data has trials as 3rd
    dimension, use mean to average across trials.

    Args:
      data:
        (m electrodes, n time points) array.
        Time series of each electrode.
      taggingfreq:
        Tagging frequency.
      filterorder:
        Order of the filter to be applied on the data.
      fsamp:
        Sampling rate.

    Returns:
      List containing 3 arrays in the following order:
        (m electrodes, n time points) array.
            Amplitude over time (real part of complex number)
        (m electrodes, n time points) array.
            Phase over time.
        (m electrodes, n time points) array.
            Imaginary part of complex number.
    """
    # Design the LOW pass filter around the taggingfreq
    uppercutoffHz = taggingfreq + 0.5
    [Blow, Alow] = scipy.signal.butter(filterorder, uppercutoffHz / (fsamp / 2))

    # Design the HIGH pass filter around the taggingfreq
    lowercutoffHz = taggingfreq - 0.5
    [Bhigh, Ahigh] = scipy.signal.butter(
        filterorder, lowercutoffHz / (fsamp / 2), btype="highpass"
    )

    # Filter the data using the low-pass filter
    lowpassdata = scipy.signal.filtfilt(Blow, Alow, data)

    # Filter the low-pass data using the high-pass filter
    lowhighpassdata = scipy.signal.filtfilt(Bhigh, Ahigh, lowpassdata)

    # Calculate Hilbert Transform on the filtered data
    tempmat = scipy.signal.hilbert(lowhighpassdata)

    hilbamp = abs(tempmat)  # Amplitude over time (real part)
    phase = np.angle(tempmat)  # Phase over time
    complex = tempmat  # Imaginary part

    return hilbamp, phase, complex
