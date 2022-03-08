function[Tsquarevec, pvalvec] = freqtag_Tsquare(complexmat)
% This function calcluates the circular Tsquare metric proposed by Vctor and Mast
% (1993), in a version that assesses the presence of a ssVEP signal. 

% Input: 
% complexmat, a 2-D matrix (electrodes by trials) containing single
% trial estimates of the ssvep frequency of interest (e.g. the driving
% frequency), as complex Fouruer components.


% Output: 
% Tsquarevec, the circular Tsquare statistic for each sensor 
% pvalvec, the corresponding p-values of the Tsquare for each sensor

M = size(complexmat, 2);

% 1 complex mean for each electrode: Z_est = xest + i Yest
meanZvec = mean(complexmat');

% 2 V_indiv for each electrode: Variance with 1/2(M-1) 
for elc = 1 : length(meanZvec)
	V_indiVec(elc) = sum(abs(complexmat(elc,:)-meanZvec(elc)).^2)./ (2*(M-1));% V_indiv for each sensor 
end

% 3 V_group for each electrode: depends on population mean 
% is signal present - i.e. is population mean = 0 i0 ?
for elc = 1 : length(meanZvec)
    V_groupVec(elc) = (abs(meanZvec(elc))).^2 .*(M/2); 
end

Tsquarevec = (V_groupVec ./ V_indiVec)' / M;
pvalvec  = fpdf(Tsquarevec, 2, 2*M-2);
pvalvec = pvalvec(:);

end








