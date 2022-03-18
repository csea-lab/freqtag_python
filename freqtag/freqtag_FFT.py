import numpy as np
from typing import List


def freqtag_FFT(data: np.ndarray, fsamp: float | int) -> List[np.ndarray]:
    """
    Applies the Discrete Fourier Transform on a 2D array of EEG data.

    Args:
      data:
        (m electrodes, n time points) array.
        Contains time series of each electrode.
      fsamp:
        Sampling rate in Hz.

    Returns:
      A list containing 4 arrays in the following order:
        (m electrodes, n/2 bins) array:
          Amplitude spectrum of each electrode.
        (m electrodes, n/2 bins) array:
          Phase spectrum of each electrode.
        (n/2 bins) array:
          Available frequencies in the data.
        (m electrodes, n bins) array:
          Complex Fourier spectrum of each electrode.
    """
    # TODO: Raise an error if invalid input is passed.

    num_points = data.shape[-1]
    midpoint = round(num_points / 2)
    untrimmed_freqs = np.fft.fftfreq(num_points, d=1 / fsamp)

    fftcomp = np.fft.fftn(data, axes=[-1])
    untrimmed_phase = np.angle(fftcomp)

    # Get amplitude, taking care of doubled DC or Nyquist frequencies.
    untrimmed_amp = np.abs(fftcomp)
    untrimmed_amp[:, 0] = untrimmed_amp[:, 0] / 2
    if num_points % 2 == 0:  # TODO: Check Nyquist frequency is corrected.
        untrimmed_amp[:, midpoint] = untrimmed_amp[:, midpoint] / 2
    untrimmed_amp = untrimmed_amp / num_points

    # Trim to remove opposite side of FFT operation.
    phase = untrimmed_phase[:, :midpoint]
    freqs = untrimmed_freqs[:midpoint]
    amp = untrimmed_amp[:, :midpoint]

    return [amp, phase, freqs, fftcomp]
