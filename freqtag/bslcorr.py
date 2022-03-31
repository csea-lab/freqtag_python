import numpy as np


def bslcorr(inmat: np.ndarray, bslvec: np.ndarray = None) -> np.ndarray:
    """
    Baseline corrects EEG data by subtracting mean of baseline in sample points.

    Args:
      inmat:
        (m sensors, n sample points) array.
        EEG data to baseline correct.
      bslvec:
        (j sample points) array.
        Vector containing indices of the data to use as the baseline.
        Defaults to indices of the whole dataset, n sample points.

    Returns:
      (m sensors, n sample points) array:
        Baseline corrected data.
    """
    # TODO: Input validation.

    if bslvec is None:
        sample_points = inmat.shape[1]
        bslvec = np.arange(sample_points)
    meanvec = np.mean(inmat[:, tuple(bslvec)], axis=1)
    return inmat - meanvec[:, None]
