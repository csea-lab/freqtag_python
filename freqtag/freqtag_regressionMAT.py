import numpy as np
from sklearn.linear_model import LinearRegression


def freqtag_regressionMAT(InMat: np.ndarray) -> np.ndarray:
    """
    Computes linear regression and subtracts regression from input array.

    The point of this is to detrend the timeseries.

    Args:
      InMat:
        (n sensors, m points) array.
        EEG data.

    Returns:
      (n sensors, m points) array.
        Data with the regression subtracted.
    """
    # TODO: Validate input.

    OutMat = np.zeros(InMat.shape)
    domain = np.arange(1, InMat.shape[1] + 1).reshape(-1, 1)
    for channel in range(InMat.shape[0]):
        model = LinearRegression().fit(domain, InMat[channel])
        trend_line = model.predict(domain)
        OutMat[channel] = InMat[channel] - trend_line

    return OutMat
