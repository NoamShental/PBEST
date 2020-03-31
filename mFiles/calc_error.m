function error=calc_error(part,num_points,currM,currY,index)
%keyboard
dat = dec2bin(part,length(index));
dat = abs(dat)';
dat(find(dat==48)) = 0;
dat(find(dat==49)) = 1;


arr = zeros(num_points,size(dat,2));
arr(index,:) = dat;

val = currM*arr;
val(find(val)) = 1;

a = val-currY*ones(1,size(arr,2));

error = sum(abs(a),1);
