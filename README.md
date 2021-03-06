# interpolate.py [![Build Status](https://travis-ci.org/radium226/interpol.svg?branch=master)](https://travis-ci.org/radium226/interpol) [![Coverage Status](https://coveralls.io/repos/radium226/interpol/badge.svg)](https://coveralls.io/r/radium226/interpol)
Tiny module which can interpolate an iterator on the fly with linear interpolation. 
![example of interpolation](https://raw.github.com/radium226/interpol/master/interpol/example_interpolate.png)
 - [ ] Use Scipy interpolators
 - [ ] Refactor `Interpolate.__call__` directly into a function
 - [ ] Replace `all_none` by an external `is_missing` function
 - [ ] Handle any kind of data by putting the interpolator function elsewhere

## Example
Run :
```
while true; do cat <<EOCAT; sleep 1 ; done | python -m interpol
1
2

4
5
6
7



10
9
8



EOCAT

```

## Install
You can install the package directly from Github: `pip install git+git://github.com/radium226/interpol.git`.
