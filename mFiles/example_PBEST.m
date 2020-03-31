addpath('./mFiles')

clear
% a) load pooling matrix
load  ./mFiles/poolingMatrix

% b) PCR Ct values measured experimentally
[~,~,raw] = xlsread('./ExpData/ExpTwoCarriersResults.xlsx');
raw(1,:) = [];
raw = cell2mat(raw);

% change measurement values to binary
qMeasurement = zeros(48,1);
qMeasurement(find(raw(:,2))) = 1;

% c) Detecting carriers
% find candidates using GPSR.
maxNum = 20; % the largest 1:maxNum entries are considered 
dt = max(abs(poolingMatrix'*qMeasurement));
tau = 0.005*dt;
u = opm(qMeasurement,poolingMatrix,tau,maxNum);

% look for the solution with minimal error with the measurements
discreteOutput = selectByError(u,poolingMatrix,qMeasurement);
detected_samples = find(discreteOutput);

fprintf('Detected samples: \n')
disp(detected_samples)

