function z=read_trace(filename) % z의 i 번째 열에 i 번째 전력파형을 로드
fid = fopen(filename, 'r');
header = fread(fid, 2, 'int')
trLen = header(1);
trNum = header(2);

for i = 1:trNum %z의 크기 trLen * trNum
    z(:,i) = fread(fid, trLen, 'float');
end
fclose(fid);
end