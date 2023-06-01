# Fourier Drawing

## Table of Contents

- [About](#about)
- [Usage](#usage)

## About <a name = "about"></a>

The idea of the project and the maths behind it come from [3b1b's video](https://www.youtube.com/watch?v=r6sGWTCMz2k&t=1s).
This little software replicates your drawings using circles rotating at a constant speed each. Tweaking the size and the initiale angle of each circle makes it possible to remake almost any shape using cycles.

## Usage <a name = "usage"></a>

All you have to do is to have python installed, tkinter comes built-in. Run ``python fourierDrawing.py`` and draw whatever shapes you want. Then press Start Fourier Drawing and the computer executes. Press New Drawing to restart.

As continuous fonctions, the Fourier Series used to make the circles are very bad at replicating anything that is made of more than one unique line. They are however very good at drawing complicated one-line shapes.

By default, the software uses 501 circles (250 clockwise, 250 anti-clockwise, 1 constant). Feel free to add or remove circles by editing the ``App.iterations`` variable in the python file. It represents the number of clockwise circles and is thus set to 250 by default.

