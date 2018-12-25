# Jackknife
Jackknife method for linear regression


f(x) = x + err, x in [-1, 1], err in N(0, 0.1)

Using grid with 0.2 step value by x. 
Shift object into jackknife method up to 3..10 \sigma.
Out of symmetry, use interval from left edge to middle point. 

RESULT format.

```
#---|---  LSE ---|---- JK ----|-- DELTA ---|-- SD_LSE --|--- SD_J ---
  0 | 0.99899005 | 0.99898997 | 0.00000817 | 0.10016589 | 0.10016589
----|------------|------------|------------|------------|------------
  1 | 0.96913627 | 0.96913992 | 0.00036190 | 0.14047137 | 0.14047137
  2 | 0.96976304 | 0.96976625 | 0.00031765 | 0.14061936 | 0.14061936
  4 | 0.97079940 | 0.97080181 | 0.00023810 | 0.14063194 | 0.14063194
...etc
```

Here:

        Columns:
                LSE     parameter value from LSE method for full sample
                JK      parameter value from Jackknife method
                DELTA   abs value for difference between LSE and JK

                SD_LSEl and 
                SD_J    var. for LSE and JK.

        Lines:
                First line for original samples.

                Next lines for samples with shifted objects. Number is 
                mean position that has been shifted (counting from left 
                edge).

For more precision results has been generated 10000 samples with objects
count N=100. General result is mean from this.





