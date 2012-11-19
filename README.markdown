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

## The visual representations

My program doesn't have any requirements for the dimensionality on the
image files as it will resize them once they are read. Furthemore since
the image quality were terrible in the provided image I had to redraw
some images.

## Visual Solution Overview

**This time I did the visual solution**. Which means I work directly on the
bitmap of the images and I do not use any anything from project 2 anymore.

My solution is simple. I define a *judge* as a function taking an image grid
and returning a score. For example, on a 2 by 2 grid, the judge for mirroring
will be the function that looks how much the mirroring of the top left image in
the grid is similar to the top right image in the grid. It then also checks the
corresponding similarity in the bottom row. If the images on the left with
mirroring appears to be alike it's right counterpart, then a high score is
awarded.

Then I implement a set of judges and run each judge on a grid with the unknown
figure replaced with each alternative and pick the alternative that has a
judge which gets most satisfied (gives highest score).

### Implemented judges

In order to be able to see different patterns, I've added judges for all
patterns present in the data set. Most of the judges are similarity based and
some other judges don't fall in any category.

#### Similarity based judges

In the case of 2x2 grids these judges work just like the mirroring judge
example above, only that there are transformations other than mirroring. In the
3x3 case these judges simple remove the second row and first column and treat
it as 2x2 grid. The concrete tranformations I have are rotation [2-1, 2-3, 2-7]
, copy mirroring (let right side of image be a mirrored copy of left side)
[2-2] and also the identity transformation [2-4]. To honor how my reasoning for
project 2 and 3 works, I decided to once again not consider mirroring as a
transformation.

#### xor rows and compare columns [2-5]

This is a 3x3 only solver. It captures the fact that a row has one part in
common and one that alternates. This judge will favor when the rows
individually has a common part but also has an alternating part that is equal.
For the [2.5] example the common part for the first row is the circle and for the last row it's the cross. They both exist, also the alternating parts, the configuration of the rod in the middle is the the same for both rows.

To actually implement this I combined a xor with other very basic bitmap
manipulations.


#### Pixel count variation [2-6, 2-8, 3-7, 3-8]

To solve the problems involving increasing triangles, I use the fact that the
number of triangles is proportional to the number of pixels. Again using xor and
other basic manipulations we capture yet another concept of images: Increasing
number of figures in a grid pattern.

To see the details of how this works I refer to the source code which is just a
very few and short lines. See `src/visual/transformations.py`

## Intelligence is hard

Naturally, since my program only has a few ways to reason if two images
are similar (aka judges) and their main specification was to "pass the
test data", this program won't be so intelligent and able to solve new
problems. However, since I think that there are so many patterns that
it's impossible to even begin to think how to handle them and in the end
one must add new logic for each new kind of pattern you want your
program to detect. I also think that my algorithm is just a mini-version
of the Affine Method described in *Taking a Look (Literally!) at the
Raven’s Intelligence Test: Two Visual Solution Strategies*. Even with
the extra features presented in their paper I don't see that their
Affine Method approach is adaptable to understanding new patterns.
Nevertheless both approaches have one intelligent component, they can
both describe what strategy they used to determine their answer. Since
the computer program can say why it choose the answer it did it will
appear much more intelligent just for that's sake.

## Meta reasoning

I strongly believe that my propositional solver from project 2 is very
powerful. What weakens it now is that it's search depth have been
extremely limited since it's so slow, also the representation extractor
from project 3 isn't perfect, for example it didn't work for problem
[3-8]. My visual reasoner is feels more like a hack, however, it
actually does the job for [3-8]. So I decided to use this meta
reasoning: **Begin.** If the representational solver finds a reasonable solution,
use that, otherwise entrust in the visual solver. **End.**  which makes sense at
least given how my methods works. Here "reasonable" means below a
certain threshold in penalty score.

## Ablation experiments

...
