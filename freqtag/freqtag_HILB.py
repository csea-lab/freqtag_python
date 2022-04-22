import numpy as np
import scipy.signal
import matplotlib.pyplot as plt


def freqtag_HILB(
    data: np.ndarray,
    taggingfreq: float | int,
    filterorder: int,
    sensor2plot: int,
    plotflag: bool,
    fsamp: float | int,
) -> list[np.ndarray]:
    """
    Implements a simple filter-Hilbert analysis of a 2D array of EEG data.

    It outputs the time-varying ssVEP amplitude, the time-varying phase, and
    the complex (real and imaginary) components of the time-varying response,
    at the tagging frequency for each time point. If your data have trials as 3rd
    dimension, average over them before using this function.

    If you choose to use plotflag, plot shows filtered data in blue, imaginary
    (hilbert) part in red, and absolute value (envelope) in black.

    Args:
        data:
            (m sensors, n time points) array.
            Time series of each sensor.
        taggingfreq:
            Tagging frequency.
        filterorder:
            Order of the filter to be applied on the data.
        sensor2plot:
            Sensor to be plotted with the phase shifted time series.
        plotflag:
            The option to plot or not plot the above information.
        fsamp:
            Sampling rate.

    Returns:
        List containing 3 arrays in the following order:
            (m sensors, n time points) array.
                Amplitude over time (real part of complex number)
            (m sensors, n time points) array.
                Phase over time.
            (m sensors, n time points) array.
                Imaginary part of complex number.
    """
    # TODO: Input validation.

    # Calculate the time axis.
    taxis = (
        np.arange(
            start=0,
            stop=(data.shape[-1] + 1) * 1000 / fsamp - 1000 / fsamp,
            step=1000 / fsamp,
        )
        / 1000
    )

    # Design the LOW pass filter around the taggingfreq
    uppercutoffHz = taggingfreq + 0.5
    [Blow, Alow] = scipy.signal.butter(filterorder, uppercutoffHz / (fsamp / 2))

    # Design the HIGH pass filter around the taggingfreq
    lowercutoffHz = taggingfreq - 0.5
    [Bhigh, Ahigh] = scipy.signal.butter(
        filterorder, lowercutoffHz / (fsamp / 2), btype="highpass"
    )

    # Filter the data using the low-pass filter
    lowpassdata = scipy.signal.filtfilt(Blow, Alow, data)

    # Filter the low-pass data using the high-pass filter
    lowhighpassdata = scipy.signal.filtfilt(Bhigh, Ahigh, lowpassdata)

    # Calculate Hilbert Transform on the filtered data
    tempmat = scipy.signal.hilbert(lowhighpassdata)

    # Make plot.
    if plotflag:
        sensor2plot -= 1  # Adjust sensor to match MATLAB style
        plt.figure("hilbert")
        plt.plot(taxis, lowhighpassdata[sensor2plot, :])
        plt.plot(taxis, np.imag(tempmat[sensor2plot, :]), "r")
        plt.plot(taxis, np.abs(tempmat[sensor2plot, :]), "k")
        plt.show()

    hilbamp = np.abs(tempmat)  # Amplitude over time (real part)
    phase = np.angle(tempmat)  # Phase over time
    complex = tempmat  # Imaginary part

    return hilbamp, phase, complex
