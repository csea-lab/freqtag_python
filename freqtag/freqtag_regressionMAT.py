import numpy as np


def freqtag_regressionMAT(InMat: np.ndarray) -> np.ndarray:
    """
    Computes linear regression and subtracts regression from input array.

    Args:
      InMat:
        (n sensors, m points) array.
        Data.

    Returns:
      (n sensors, m points) array.
      Data with the regression subtracted.
    """
    # TODO: Validate input.

    OutMat = np.zeros(InMat.shape)
    num_points = InMat.shape[-1]
    X = _get_X(num_points)
    for channel in range(InMat.shape[0]):
        regkoefs = _get_regkoefs(InMat, channel, X)
        reggerade = np.arange(1, num_points + 1) * regkoefs[1, 0] + regkoefs[0, 0]
        OutMat[channel] = InMat[channel] - reggerade

    return OutMat


def _get_X(num_points: int) -> np.ndarray:
    """
    Returns a matrix containing a column of ones and an incrementing column.
    """
    ones_col = np.ones(num_points)
    increment_col = np.arange(1, num_points + 1)
    return np.stack([ones_col, increment_col]).T


def _get_regkoefs(InMat: np.ndarray, channel: int, X: np.ndarray) -> np.ndarray:
    """
    Returns the regression coefficients.
    """
    pseudoinverse_arg = np.linalg.pinv(np.matmul(X.T, X))
    other_arg = np.matmul(X.T, InMat[channel, :, None])
    return np.matmul(pseudoinverse_arg, other_arg)
