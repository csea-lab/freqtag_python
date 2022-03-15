import numpy as np
from typing import List


def FFT(data: np.array, fsamp: float) -> List[np.array]:
    """
    Apply the Discrete Fourier Transform on a 2-D array.

    Args:
        data (np.array): Sensors by time points 2-D matrix
        fsamp (float): Sampling rate in Hz.

    Returns:
        np.array: Columns in the array are:
            amp: amplitude spectrum (amp)
            phase: phase spectrum
            freqs: frequencies available in the spectrum
            fftcomp: complex fourier components
    """
    num_points = data.shape[-1]
    midpoint = round(num_points / 2)
    untrimmed_freqs = np.fft.fftfreq(num_points, d=1/fsamp)

    fftcomp = np.fft.fftn(data, axes=[-1])
    untrimmed_phase = np.angle(fftcomp)

    # Get amplitude, taking care of doubled DC or Nyquist frequencies.
    untrimmed_amp = np.abs(fftcomp)
    untrimmed_amp[:, 0] = untrimmed_amp[:, 0] / 2
    if num_points % 2 == 0:
        untrimmed_amp[:, midpoint] = untrimmed_amp[:, midpoint] / 2
    untrimmed_amp = untrimmed_amp / num_points

    # Trim to remove opposite side of FFT operation.
    phase = untrimmed_phase[:, :midpoint]
    freqs = untrimmed_freqs[:midpoint]
    amp = untrimmed_amp[:, :midpoint]

    return [amp, phase, freqs, fftcomp]
