import numpy


def FFT(data: numpy.array, fsamp: float) -> numpy.array:
    """
    Apply the Discrete Fourier Transform on a 2-D array.

    Args:
        data (numpy.array): Sensors by time points 2-D matrix
        fsamp (float): Sampling rate in Hz.

    Returns:
        numpy.array: Columns in the array are:
            amp: amplitude spectrum (amp)
            phase: phase spectrum
            freqs: frequencies available in the spectrum
            fftcomp: complex fourier components
    """
    # NFFT = data.shape[1]
    # numpy.fft.fft(a, n=None, axis=- 1, norm=None)
    # fftcomp = fft(data, NFFT)
	# phase = angle(fftcomp);      % Calculate the phase
    # Mag = abs(fftcomp);          % Calculate the amplitude
               
	
	# Mag(1,:) = Mag(1,:)/2;                                             % DC Frequency not twice
	# if ~rem(NFFT,2)                                                    % Nyquist Frequency not twice
	# 		Mag(NFFT/2+1, :)=Mag(NFFT/2+1, :)./2;
	# end
	
	# Mag=Mag/NFFT;               % After computing the fft, the coefficients will be 
    #                             % scaled in terms of frequency (in Hz) 
    
    # Mag = Mag';                 % Sensors as rows again
    # phase = phase';
    
    # amp = Mag(:,1:round(NFFT./2));              % Scaling the power
    # phase  = phase(:,1:round(NFFT./2));         % Scaling the phase
    # select = 1:(NFFT+1)/2;                      % Scaling the frequencies
    # freqs = (select - 1)'*fsamp/NFFT;
    pass
