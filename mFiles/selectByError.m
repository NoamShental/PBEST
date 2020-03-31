function [xOut]=selectByError(index,currM,currY)

num_points = size(currM,2);
maxNum = length(index);
if maxNum>=24
  disp(maxNum)
end

if maxNum>20
  error = zeros(1,2^maxNum-1);
  section = [1:2^20:2^maxNum-1 2^maxNum];
  for i=1:length(section)-1
    part = section(i):section(i+1)-1;
    error(part) = calc_error(part,num_points,currM,currY,index);
  end
else
  part = 1:2^maxNum-1;
  error = calc_error(part,num_points,currM,currY,index);
end

sel = find(error==min(error));

dat = dec2bin(sel,length(index));
dat = abs(dat)';
dat(find(dat==48)) = 0;
dat(find(dat==49)) = 1;
arr = zeros(num_points,length(sel));
arr(index,:) = dat;

if length(sel)>1 % means that there are collisions
  [~,tk_ind]=max(sum(arr,1));
  xOut = arr(:,tk_ind);
else
  xOut = arr;
end





%xOut = zeros(size(x_BB_mono_cont));

%if length(intersect(find(xOut),find(x)))<5
%  keyboard
%end

%disp('add the case 2')
%keyboard
if 1==2
  figure(2)
  plot(errorRound,'r')
end

  