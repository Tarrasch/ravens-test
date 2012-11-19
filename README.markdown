% Project 4 in Knowledge Based AI
% Arash Rouhani
%

## Terminology

I'm given 6 *images*, each containing a *grid* of *figures* and the
*program* must choose between 4 to 8 *figure alternatives*. A figure usually
contains 1-3 *subfigures*, like a circle or a rectangle.

If not specified, the *similarity* between two images is just the definition
given in Kunda's presentation, namely the number of pixels in the  intersection
divided by the number of pixels in the union.

## Running the program

      $ python ArashRouhani_Project_4.py

Works for me. It takes a few minutes on my machine. My program uses
*opencv* for most of its image processing but also *pymorph* for the
parts involving morphological operations. Meanwhile opencv has to be
installed on the graders machine (I know a lot of my class mates used it
too), pymorph is attached in the zip file and should just work.

### Experimenting with the programs verbosity

Just like for my second project you can experiment with my programs verbosity
by uncommenting a few lines in the file `ArashRouhani_Project_4.py`. My program
does some meta reasoning by choosing which reasoner is most likely to be
correct, the visual or the representational one? The comments in that source
file will explain exactly how the verbosity switches work.

## Visual Solution Overview

**This time I did the visual solution**. Which means I work directly on the
bitmap of the images and I do not use any anything from project 2 anymore.

My solution is quite straight forward. I define a *judge* as a function taking
an image grid and returning a score. For example, on a 2 by 2 grid, the judge
for mirroring will be the function that looks how much the mirroring of the top
left image in the grid is similar to the top right image in the grid. Then
also checks the corresponding similarity in the bottom row.

Then I implement a set of judges and run each judge on a grid with the unknown
figure replaced with each alternative and pick the alternative that has a
judge which gets most satisfied (gives highest score).

### Implemented judges

#### Similarity based judges
...

#### xor rows and compare columns (How to solve 5)

#### Pixel count variation

## The issue of over fitting

...

## Meta reasoning

...

## Ablation experiments

...
