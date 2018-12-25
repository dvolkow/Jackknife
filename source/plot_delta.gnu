set terminal postscript eps enhanced color 20
set output "delta.eps"
set key top right
set linestyle 1 lt 1 lw 3
set xlabel "N"
set ylabel "delta"
#set size ratio -1
set mxtics 5
set mytics 5
#set yrange [-1:1]
set xrange [0:30]
#f(x) = x
plot 'delta_3.txt' using 1:2 title "3" with l ls 1 lt rgb 'blue', 'delta_4.txt' using 1:2 title "4" with l ls 1 lt rgb 'red', 'delta_5.txt' using 1:2 title "5" with l ls 1 lt rgb 'green', 'delta_6.txt' using 1:2 title "6" with l ls 1 lt rgb 'grey', 'delta_7.txt' using 1:2 title "7" with l ls 1 lt rgb 'yellow', 'delta_8.txt' using 1:2 title "8" with l ls 1 lt rgb 'pink', 'delta_9.txt' using 1:2 title "9" with l ls 1 lt rgb 'brown', 'delta_10.txt' using 1:2 title "10" with l ls 1 lt rgb 'gold'  
reset
   










