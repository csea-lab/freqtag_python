import numpy as np
from typing import List


def freqtag_FFT(data: np.array, fsamp: float) -> List[np.array]:
    """
    Applies the Discrete Fourier Transform on EEG data.

    Args:
      data:
        (m, n) array. Each row is the time series of a sensor.
        There are m sensors and n time points.
      fsamp:
        Sampling rate in Hz.

    Returns:
      A list containing 4 arrays in the following order:
        (m, n/2) array:
          Each row is the amplitude spectrum of a sensor.
        (m, n/2) array:
          Each row is the phase spectrum of a sensor.
        (n/2) array:
          Available frequencies in the data.
        (m, n) array:
          Each row is the complex Fourier components of a sensor.
    """
    num_points = data.shape[-1]
    midpoint = round(num_points / 2)
    untrimmed_freqs = np.fft.fftfreq(num_points, d=1 / fsamp)

    fftcomp = np.fft.fftn(data, axes=[-1])
    untrimmed_phase = np.angle(fftcomp)

    # Get amplitude, taking care of doubled DC or Nyquist frequencies.
    untrimmed_amp = np.abs(fftcomp)
    untrimmed_amp[:, 0] = untrimmed_amp[:, 0] / 2
    if num_points % 2 == 0:  # TODO: Confirm Nyquist frequency is processed correctly
        untrimmed_amp[:, midpoint] = untrimmed_amp[:, midpoint] / 2
    untrimmed_amp = untrimmed_amp / num_points

    # Trim to remove opposite side of FFT operation.
    phase = untrimmed_phase[:, :midpoint]
    freqs = untrimmed_freqs[:midpoint]
    amp = untrimmed_amp[:, :midpoint]

    return [amp, phase, freqs, fftcomp]
