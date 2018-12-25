set terminal postscript eps enhanced color 20
set output "dataset.eps"
unset key
set linestyle 1 lt 1 lw 3
set xlabel "X"
set ylabel "Y"
set size ratio -1
set mxtics 5
set mytics 5
set yrange [-1:1]
set xrange [-1:1]
f(x) = x
plot 'dataset.txt' using 1:2 with p ps 0.1 lt rgb 'red', f(x) lt rgb 'blue'
reset
   










