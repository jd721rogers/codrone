% Specify log file location
fname = 'altitude_control_P75_I5';
log_file = ['C:\Users\jd721\Documents\EN_525_661\codrone\mod6\' fname '.txt'];
ptitle = strrep(fname, '_', ' ');

% Load data
data = readtable(log_file);

% Plot data
figure;
subplot(3,1,1);hold on;grid on;
    plot(data.time,data.velocityX,'linewidth',1.5)
    plot(data.time,data.velocityX_cmd,'r--','linewidth',1.5)
    xlabel('Time (s)');ylabel ('Velocity X (cm/s)');set(gca,'fontweight','bold')
    title(ptitle);
subplot(3,1,2);hold on;grid on;
    plot(data.time,data.velocityY,'linewidth',1.5)
    plot(data.time,data.velocityY_cmd,'r--','linewidth',1.5)
    xlabel('Time (s)');ylabel ('Velocity Y (cm/s)');set(gca,'fontweight','bold')
subplot(3,1,3);hold on;grid on;
    plot(data.time,data.altitude,'linewidth',1.5)
    plot(data.time,data.altitude_cmd,'r--','linewidth',1.5)
    xlabel('Time (s)');ylabel ('Altitude (m)');set(gca,'fontweight','bold')