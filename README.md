# Circle2Square

Interpolation between a circle and a square the single argument represents the radius of the inner circle

```
python gen_mem.py 7
```

## Resampling of curves to keep even density

The animation depicts the effect of shifting the exponent of the interpolation for the method in which the curves are resampled

<p align="center">
  <img width="500" src="images/dens.gif">
</p>

## Constant number of points

The animation depicts the effect of shifting the exponent of the interpolation for the method in which the curves have a constant number of points 

<p align="center">
  <img width="500" src="images/dots.gif">
</p>

## Comparison

Here we compare the difference between both algorithms. In both cases we use a linear interpolation between both shapes. We first compare the difference between the default behaviour of both. A red-white-blue color map is used to show the shortest distance for a given sphere to any other sphere inlcuding periodic boundary conditions (PBC) this help to visualize the difference in the packing from the desired 1.875 value. The values range from 0.5 (red) and -0.5 (blue).

<p align="center">
  <img width="250" src="images/dots.png">
  <em>No Resampling</em>
  <img width="250" src="images/dens_default.png">
  <em>Resampling</em>
</p>

We also included the effect of the $\sigma$ parameter that allows to further modify the packing of the spheres for the resampling method. 

<p align="center">
  <img width="250" src="images/dens_mod_2.png">
  <em>sigma = 2</em>
  <img width="250" src="images/dens_mod_4.png">
  <em>sigma = 4</em>
  <img width="250" src="images/dens_mod_6.png">
  <em>sigma = 6</em>
  <img width="250" src="images/dens_mod_8.png">
  <em>sigma = 8</em>
  <img width="250" src="images/dens_mod_10.png">
  <em>sigma = 10</em>
  <img width="250" src="images/dens_mod_12.png">
  <em>sigma = 12</em>
</p>

Based on this we finally provide a comparison between both models and the selected value of $\sigma = 11$ that optimizes the average to a value of 1.874 which is only 0.001 off the target value.

<p align="center">
  <img width="250" src="images/dots.png">
  <img width="250" src="images/dens_default.png">
  <img width="250" src="images/dens_opt.png">
</p>
