% Project 3 in Knowledge Based AI
% Arash Rouhani
%

## Terminology

I'm given 6 *images*, each containing a *grid* of *figures* and the
*program* must choose between 4 to 8 *figure alternatives*. A figure usually
contains 1-3 *subfigures*, like a circle or a rectangle.

I also use terminology like `Area`, `FilledArea` and `Eccentricity`.
These are features of an image region. See [this
page][http://www.mathworks.se/help/images/ref/regionprops.html] for details.

## Running the program

      $ python ArashRouhani_Project_3.py

Works for me. It takes a few minutes on my machine. My program depends on
*opencv* for most of it's image processing but also *pymorph* for the image
processing parts involving morphological operations. Meanwhile opencv
has to be installed on the graders machine (I know a lot of my class
mates used it), pymorph is attached in the zip file and should just
work.

### Experimenting with the programs verbosity

Just like for my second project you can experiment with my programs
verbosity by uncommenting a few lines in the file
`ArashRouhani_Project_3.py`. There is one line that will make my program
output the intermediete representation, experimenting with that should
make it somewhat easier to understand how my program thinks.

For instance, this is the outputted intermediete representation for the
second problem:

    {'1': [{'shape': 'shape_3', 'x': 0, 'y': 1},
           {'shape': 'shape_3', 'x': 0, 'y': 0}],
     '2': [{'shape': 'shape_3', 'x': 1, 'y': 0},
           {'shape': 'shape_3', 'x': 0, 'y': 0}],
     '3': [{'shape': 'shape_0', 'x': 1, 'y': 0},
           {'shape': 'shape_3', 'x': 0, 'y': 0}],
     '4': [{'shape': 'shape_10', 'x': 0, 'y': 0}],
     'grid': [[[{'shape': 'shape_0', 'x': 0, 'y': 0}],
               [{'shape': 'shape_0', 'x': 1, 'y': 0},
                {'shape': 'shape_0', 'x': 0, 'y': 0}]],
              [[{'shape': 'shape_3', 'x': 0, 'y': 0}]]]}

We notice two interesting things.

  1. The program naturally don't have any way to give mnemonic names to
     the shape. It doesn't need to, because it only needs to when shapes
     are different.
  2. It has filtered out irrelevant properties.  For instance 'rotation'
     isn't relevant to the second problem.

## Solution Overview

In project 2, a figure was a list of subfigures and each subfigure contained
*properties* with *values*. In pseudocode:

    rep = read_rep('rep.yaml')
    answer = solve(rep)

My approach to project 3 is to create `rep` from the images. In pseudocode:

    vis_rep = read_vis_rep('rep.png')
    rep = vis_rep_to_rep(vis_rep)
    answer = solve(rep)

In fact, I did almost no changes at all to the `solve()` function! That
is amazing, because it means that my representations for the second
project where described at a low level. Furthermore, the intermediete
representation extracted from the images are equivelent to my hand
written ones for project 2.  Naturally, this was my intention and not a
coincidence, but this too verifies that my second project worked at a
quite low level already.

## How I implement `vis_rep_to_rep()`

As I see it, what is worth discussing about my third project is how I
can extract the following attributes from the visual images.

  * Shape
  * Rotation
  * Filledness (a yes-no boolean indicating if the subfigure is filled or not)
  * Position

How I actually use these properties after they've been extracted has
already been explained in it's entirety in my design report for the
second project.

### Extracting shape

### Extracting rotation, filledness and position

Rotation, filledness and position are comparably simple.

After identifying a the shape of an object, *rotation* is found by
taking the symmetric difference of the shapes representant and the
actual current subfigure's pixelset. If the symmetric difference is small
for a given rotation of the current subfigure, then that will be the
rotation for that subfigure.

I consider a figure *filled* if the ratio of 'Area' and 'FilledArea' is
greater than `0.9`.

The *position* is inferred by considering one of the subfigures as the
upperleftmostest one and then I compare how much translated the current
image is in both dimensions.

### Extracting nested subfigures

## Changes made to `solve()` since the last project



## Discussing the quality of created representations

### Discussing solution qualities since project 2


