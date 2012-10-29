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
     the shape. It doesn't need to, because it only needs to know when
     if they are different.
  2. It has filtered out irrelevant properties.  For instance
     `'rotation'` isn't relevant to the second problem.

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

First we say that two shapes are the same even if they are rotations of
each other. We partition all subfigures into sets like this:

  1. Look at rotation invariant *features* of a subfigure. These are all
     real values so we can convert each subfigure to a point in a space
     with as many dimensions as we have features.
  2. Consider two subfigures being of the same shape if their points put
     in an euclidean space are not farther apart than a threshold value
     *t*.

While (1) is quite an established trick, (2) is a naive way to seperate
partition them, ideally one would have something like k means
clustering. But that's way too complicated. Unfortunately, using this
naive method in (2) made me configure the parameters (threshold and
coefficients) until the program distinguished the shapes in problem 1 to
6. This causes extreme overfitting which is really bad.

Also, we let the *shape represant* denote the first inhabitant of the
set for a given shape.

### Extracting rotation, filledness and position

Rotation, filledness and position are comparably simple.

After identifying the shape of an subfigure, *rotation* is found by
taking the symmetric difference of the shapes representant's pixelset
and the current subfigure's pixelset. If the symmetric difference is
small for a given rotation of the current subfigure, then that will be
the rotation for that subfigure.

I consider a figure *filled* if the ratio of 'Area' and 'FilledArea' is
greater than `0.9`.

The *position* is inferred by considering one of the subfigures as the
upperleftmostest one and then I compare how much translated the current
image is in both dimensions.

### Extracting nested subfigures

Get the composed subfigure: [fig1]

![orig](img/orig.png)

calculate it's thin (morphological term): [fig2]

![thin](img/thin.png)

bfs-kill away the perimeter: [fig3]

![bfs-kill](img/bfs-kill.png)

dilate back a couple of steps to get the inner subfigure: [fig4]

![dilated](img/dilated.png)

also create outer subfigure by set difference: [fig5]

![outer](img/outer.png)

## Changes made to `solve()` since the last project

Not much was changed. The major modification is that it treats the
rotation property specially in the sense that it understands that `360`
and `-360` degrees is the same as `0` degrees.

## Discussing the quality of created representations

The visually infered representations for the problems 1 to 6 are very
similar to the one I manually created. Of course there are no mnenomic
names for the shapes anymore but the representations are still
equivelent from `solve()`'s perspective. It turns out that the only
difference between the representations are that my program considers the
thick lines to be filled, which they really are but a human doesn't
think that way because the are just lines. It turned out that those
extra properties only helped `solve()` because the pattern between the
lines are now stronger since they have even more properties in common.

### About problem 7

It's very expected that my program understands the grid pattern. However
as of the overfiting issues with the shape recognition I was happy to
see that is considered big trinagles as different figures as small
triangles. While most features my program looks at are size invariant,
the features 'MajorAxisLength' and 'MinorAxisLength' are not, hence is
sees big and small triangles as different shapes and succesfully solves
the problem for the right reason.

### About problem 8

My program doesn't solve this for two reasons.

  1. The grid pattern is diffused since the frame will be the
     upperleftmost subfigure.
  2. There are three patterns here.
    1. Increase rows/cols of triangles
    2. Change frame 2 to 3 (right direction only)
    3. Change frame 1 to 2 (right direction only)

There is no grid in the representation because of (1) and my program is
hardcoded to only look for patterns in 2 steps, but it's clear from (2)
that that is not enough. If one also searches for patterns in 3 steps,
the program will run for hours or days.

## Ablation experiments

Ablation experiments could be done by removing the ability to infer the
four different kinds of properties, *shape, rotation, position* and
*filledness*. But this would turn out to give out the exact same results
from my ablation experiments from the last project. The only difference
now is that the visual inferences have dependencies To infer rotation,
shape need to be infered first, so you can't ablate out only shape
without also taking out rotation.
