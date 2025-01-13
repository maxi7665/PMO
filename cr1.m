%x2 = @(x1) (20 - 4 * x1) / 4;

x2_1 = @(x1) (4 - x1.*1) ./ 2;
x2_2 = @(x1) (6 - 2 .* x1);
x2_3 = @(x1) 8 - x1;
x2_4 = @(x1) 0;

x2 = @(x1) (6 - 2 .* x1);

hold on;

fplot(x2_1, DisplayName="x1+2x2<=4");
fplot(x2_2, LineWidth=2, color='red', DisplayName="2x1+x2<=6");
fplot(x2_3, DisplayName="x1+x2>=8");
fplot(x2, '--', color="blue", DisplayName="2x1+x2->min");
legend();
xline(0, '-', 'x');
yline(0, '-', 'y'); 

ylim([-5 15]);
xlim([-5 15]);



hold off;