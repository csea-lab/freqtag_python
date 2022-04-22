import numpy as np


def freqtag_FFT(data: np.ndarray, fsamp: float | int) -> list[np.ndarray]:
    """
    Applies the Discrete Fourier Transform on a 2D array of EEG data.

    Args:
        data:
            (m sensors, n time points) array.
            Time series of each sensor.
        fsamp:
            Sampling rate in Hz.

    Returns:
        List containing 4 arrays in the following order:
            (m sensors, n/2 bins) array:
                Amplitude spectrum of each sensor.
            (m sensors, n/2 bins) array:
                Phase spectrum of each sensor.
            (n/2 bins) array:
                Available frequencies in the data.
            (m sensors, n bins) array:
                Complex Fourier spectrum of each sensor.
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
    if num_points % 2 == 0:  # TODO: Check odd num_points handled correctly.
        untrimmed_amp[:, midpoint] = untrimmed_amp[:, midpoint] / 2
    untrimmed_amp = untrimmed_amp / num_points

    # Trim to remove opposite side of FFT operation.
    phase = untrimmed_phase[:, :midpoint]
    freqs = untrimmed_freqs[:midpoint]
    amp = untrimmed_amp[:, :midpoint]

    return [amp, phase, freqs, fftcomp]
