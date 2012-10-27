% Project 3 in Knowledge Based AI
% Arash Rouhani
%

## Terminology

I'm given 6 *images*, each containing a *grid* of *figures* and the
*program* must choose between 4 to 8 *figure alternatives*. A figure usually
contains 1-3 *subfigures*, like a circle or a rectangle.

## Running the program

      $ python ArashRouhani_Project_3.py

Works for me. It takes about one minute on my machine. My program depends on
*opencv* for most of it's image processing but also *pymorph* for the image
processing parts involving morphological operations.

## Overview

In project 2, a figure was a list of subfigures and each subfigure contained
*properties* with *values*. In pseudocode:

    rep = read_rep('rep.yaml')
    answer = solve(rep)

My approach to project 3 is to create `rep` from the images. In pseudocode:

    vis_rep = read_vis_rep('rep.png')
    rep = vis_rep_to_rep(vis_rep)
    answer = solve(rep)

In fact, I did almost no changes at all to the `solve()` function! That
is amazing, because it means that my representation where described at a
low level. Furthermore, the intermediete representation extracted from
the images are equivelent to my hand written ones for project 2.
Naturally, this was my intention and not a coincidence, but this too
verifies that my second project worked at a quite low level already.

## How I implement `vis_rep_to_rep()`

As I see it, what is worth discussing about my third project is how I
can extract the following values from the visual images.

  * Shape
  * Rotation
  * Filledness (a yes-no boolean indicating if the figure is filled or not)
  * Position

How I actually use these properties after they've been extracted has
already been explained in it's entirety in my design report for the
second project.

### Extracting shape

### Extracting rotation

### Extracting filledness

### Extracting position


## Changes made to `solve()` since the last project



## Discussing the quality of created representations

### Discussing solution qualities since project 2



### Experimenting with the programs verbosity

The verbosity of my program is configurable. By uncommenting a few
lines, then my program will output more verbose information, it'll say
"why" it chooses one solution over another. How to do this should be
apparent by looking in the file `ArashRouhani_Project_2.py`. The reason why
I didn't write a command line parser is because I know that the TA that
graded me the last time had python `2.6`, and from the switch to `2.7`
they changed parsing libraries.

This is for example what it outputs when solving the second problem in the
verbose mode:

    --------------------------------------------------------
    Solution to problem 2 is:
    (2,
     [(for (All) inplace (set `shape`s to circle), 'down'),
      (for (All) inplace (inc `xpos`s by 20) -- and then for (All) copy (set
      `xpos`s to -20),
      'right')],
    30)

My answer for problem 1 is 6. I discussed this with a couple of friends
and they seemed to agree that 4 is more likely for many reasons.
However, my program says 6 and here is it's motivation

    --------------------------------------------------------
    Solution to problem 1 is:
    (6,
     [(for (All) inplace (inc `start`s by -90), 'down'),
      (for (All) inplace (inc `start`s by 90), 'right')],
    20)

The `down` direction pattern
is to decrease the sectors starting angle by 90 degrees, which simply
means rotating clockwise by 90 degrees. For right direction it instead
choose to increase it by 90.

The last `20` is the penalty it gives to the answer.
