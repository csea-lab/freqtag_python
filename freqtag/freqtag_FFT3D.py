import numpy as np


def freqtag_FFT3D(dataset: np.ndarray, fsamp: float | int) -> list[np.ndarray]:
    """
    Applies the Discrete Fourier Transform on a 3D array of EEG data.

    Transforms each trial into the spectral domain and averages the
    single-trial amplitude spectra to yield one output spectrum.

    Args:
      dataset:
        (m electrodes, n time points, k trials) array.
        Contains time series of each electrode for each trial.
      fsamp:
        Sampling rate in Hz.

    Returns:
      List containing 3 arrays in the following order:
        (m electrodes, n/2 bins) array:
          Amplitude spectrum of each electrode.
        (n/2 bins) array:
          Available frequencies in the data.
        (m electrodes, n/2 bins, k trials) array:
          Complex Fourier spectrum of each electrode for each trial.
    """
    # TODO: Raise errors on invalid input.

    num_points = dataset.shape[1]
    midpoint = round(num_points / 2)
    untrimmed_freqs = np.fft.fftfreq(num_points, d=1 / fsamp)
    untrimmed_fftcomp = np.fft.fftn(dataset, axes=[1])

    # Mean amplitudes over trials.
    untrimmed_amp = np.abs(untrimmed_fftcomp)
    untrimmed_amp[:, 0, :] = untrimmed_amp[:, 0, :] / 2
    if num_points % 2 == 0:  # TODO: Check odd num_points is handled correctly.
        untrimmed_amp[:, midpoint, :] = untrimmed_amp[:, midpoint, :] / 2
    untrimmed_amp = untrimmed_amp / num_points
    untrimmed_amp = np.mean(untrimmed_amp, axis=2)

    # Remove the spurious 2nd half of the FFT results.
    amp = untrimmed_amp[:, :midpoint]
    fftcomp = untrimmed_fftcomp[:, :midpoint, :]
    freqs = untrimmed_freqs[:midpoint]

    return amp, freqs, fftcomp
