from freqtag.freqtag_FFT import FFT
from freqtag.download_examples import download
import pytest
import scipy.io
import numpy


@pytest.fixture
def exampledata_1_results():
    download()
    exampledata_1 = scipy.io.loadmat("raw/exampledata_1.mat")["data_1"]
    data_ssvep = exampledata_1[:, 700:3700, :]
    mean_ssvep = numpy.mean(data_ssvep, 2)
    return FFT(mean_ssvep, 500)


# NORMAL CASES
# The function outputs a 4xN array.
def test_output_shape(exampledata_1_results):
    assert exampledata_1_results.shape[0] == 4

# The first column contains correct amplitudes.
# The 2nd column contains correct phase spectrum.
# The 3rd column contains correct frequencies available in the spectrum.
# The 4th column contains correct complex fourier components.

# EDGE CASES
# The function throws an error when fsamp < 0.
# The function throws an error when data isn't a 2D array.
