# Circle2Square

Interpolation between a circle and a square

```
python gen_mem.py 7
```

## Resampling of curves to keep even density

<p align="center">
  <img width="500" src="images/dens.gif">
</p>

## Constant number of points

<p align="center">
  <img width="500" src="images/dots.gif">
</p>

## Comparison

Here we compare the difference between both algorithms. In both cases we use a linear interpolation between both shapes. We first compare the difference between the default behaviour of both.

<p align="center">
  <img width="300" src="images/dens_default.png",  title="Resampling">
  <img width="300" src="images/dots.png",  title="No Resampling">
</p>
