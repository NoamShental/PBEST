function tk = opm(qMeasurement,pooling_matrix,tau,maxNum)
% do GPSR
fractionalOutput = applyGPSR(qMeasurement,pooling_matrix,tau);
[jj,ii] = sort(fractionalOutput,'descend');
firstZero = find(jj==0);
if isempty(firstZero)
  firstZero = length(jj);
else
  firstZero = firstZero(1);
end
tk = ii(1:min([maxNum,firstZero]));



