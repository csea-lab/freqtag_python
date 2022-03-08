% bslcorrmat
% corrects 129 channel ar mat 
% by subtracting mean of baseline in samplepoints

function [data] = bslcorr(inmat, bslvec);

if isempty (bslvec), 
    bslvec = 1:size(inmat,2); 
end

for chan = 1 : size(inmat, 1)
data(chan,:) = inmat(chan,:)-mean(inmat(chan,bslvec),2);
end
