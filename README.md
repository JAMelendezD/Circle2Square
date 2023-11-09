# Circle2Square

Interpolation between a circle and a square first argument represents the radius of the inner circle, the second argument is for a given value of sigma

```
python gen_mem.py 7 30
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

Here we compare the difference between both algorithms. In both cases we use a linear interpolation between both shapes. We first compare the difference between the default behaviour of both. A red-white-blue color map is used to show the shortest distance for a given sphere to any other sphere inlcuding periodic boundary conditions (PBC) this help to visualize the difference in the packing from the desired 1.875 value. The values range from 0.5 (red) and -0.5 (blue). Here the main focus is to avoid larges energies due to close contacts since the repulsive wall increases rapidly with distance, being slightly further is less problematic since the force decreases to 0 as long as there are no gaps in which water can permeate through

<p align="center">
  <img width="250" src="images/dots.png">
  <em>No Resampling</em>
  <img width="250" src="images/dens_mod_40.png">
  <em>Resampling</em>
</p>

We also included the effect of the $\sigma$ parameter that allows to further modify the packing of the spheres for the resampling method. 

<p align="center">
  <img width="250" src="images/dens_mod_2.png">
  <em>sigma = 2</em>
  <img width="250" src="images/dens_mod_4.png">
  <em>sigma = 4</em>
</p>

<p align="center">
  <img width="250" src="images/dens_mod_8.png">
  <em>sigma = 8</em>
  <img width="250" src="images/dens_mod_12.png">
  <em>sigma = 12</em>
</p>

<p align="center">
  <img width="250" src="images/dens_mod_16.png">
  <em>sigma = 16</em>
  <img width="250" src="images/dens_mod_20.png">
  <em>sigma = 20</em>
</p>

<p align="center">
  <img width="250" src="images/dens_mod_30.png">
  <em>sigma = 30</em>
  <img width="250" src="images/dens_mod_40.png">
  <em>sigma = 40</em>
</p>

Eventually for a large enough $\sigma$ the spacing converges to a final system.

## No interpolation

<p align="center">
  <img width="250" src="images/nointer_05.png">
  <em>eps = 0.5</em>
  <img width="250" src="images/nointer_11.png">
  <em>eps = 1.1</em>
</p>

<p align="center">
  <img width="250" src="images/nointer_15.png">
  <em>eps = 1.5</em>
  <img width="250" src="images/nointer_19.png">
  <em>eps = 1.9</em>
</p>

## 3D visualization 

<p align="center">
  <img width="250" src="images/mem_inter.png">
  <em>Interpolation</em>
  <img width="250" src="images/mem_nointer.png">
  <em>No interpolation</em>
</p>


