import numpy as np
from sklearn.linear_model import LinearRegression


def freqtag_regressionMAT(InMat: np.ndarray) -> np.ndarray:
    """
    Computes and subtracts a linear regression for each sensor's time series.

    This removes any linear trend in the data.

    Args:
      InMat:
        (n sensors, m points) array.
        EEG data.

    Returns:
      (n sensors, m points) array.
        Data with each electrode's regression subtracted.
    """
    # TODO: Validate input.

    OutMat = np.zeros(InMat.shape)
    domain = np.arange(1, InMat.shape[1] + 1).reshape(-1, 1)
    for channel in range(InMat.shape[0]):
        model = LinearRegression().fit(domain, InMat[channel])
        trend_line = model.predict(domain)
        OutMat[channel] = InMat[channel] - trend_line

    return OutMat
