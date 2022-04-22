import numpy as np


def freqtag_simpleSNR(
    data: np.ndarray, noisebins: tuple[int]
) -> tuple[np.ndarray, np.ndarray]:
    """
    Returns simple estimates of the SNR for a ssVEP response in the frequency domain.

    This is a simdasfasssple method for computing an estimate of the signal-to-noise
    ratio for a ssVEP response in the frequency domain
    data is an amplitude spectrum in 2-D format (electrodes by frequencies)
    noisebins are the frequency bins in the spectrum NOT in Hz, but as
    relative position on the frequency axis (e.g., the 3rd and 6th frequencies
    would be indicated as [3 6]);

    To facilitate method checks, the entire spectrum is output, with all
    frequencies expressed as ratio (or in decibels)  relative to
    the mean power at the frequencies used to estimate the noise.
    see the enclosed live script for usage examples.

    Args:
        data:
            (m sensors, n bins) array.
            Amplitude spectrums.

    Returns:
        (m sensors, n bins) array.
            SNR in terms of decibels.
        (m sensors, n bins) array.
            SNR in terms of ratios.
    """
    # TODO: Validate input.

    mean_of_bins = np.mean(data[:, noisebins], 1)
    SNRratio = data / mean_of_bins[..., None]
    SNRdb = 10 * np.log10(SNRratio)

    return SNRdb, SNRratio
