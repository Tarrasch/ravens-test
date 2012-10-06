% Arash Rouhani
% Project 2 in Knowledge Based AI
%

# NOTE

Hi, the design report is not done. I've just included the information needed to run
the program here. The program itself if however complete in the sense that it
answers the questions.

## Installation and running the program

      $ python ArashRouhani_Project_2.py

Works for me. It takes one minute on my machine.  In the unlikely case that you
don't have pyyaml, I've included the lib in the zip. If that is not working
because you have python 3, you can download the source [here] and replace the
`yaml` folder with the one in the **source** (either `.zip` or `.tar.gz`)
archive from the `lib3` folder.

## Experementing with the programs verbosity

Also, please checking in `ArashRouhani_Project_2.py`. By uncommenting a
few lines, then my program will output more verbose information, like say "why"
it chooses one solution over another. For instance, I tried this on the second
problem. How to do this should be clear by looking in the file
`ArashRouhani_Project_2.py`. The reason why I didn't write a command line
parser is because I know that the TA that graded me the last time had python
`2.6`, and from the switch to `2.7` they changed parsing libraries.

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

Also, please note that my answer for problem 1 is 6. I discussed this with a
couple of friends and they seemed to agree that 4 is more likely for many
reasons. However, my program says 6 and here is it's motivation

    --------------------------------------------------------
    Solution to problem 1 is:
    (6,
     [(for (All) inplace (inc `start`s by -90), 'down'),
      (for (All) inplace (inc `start`s by 90), 'right')],
    20)

In other words, It finds the pattern that a move in the `down` direction is to
decrease the sectors starting angle by 90 degrees. For right direction it
insteads chooes to increase it by 90.

The `20` is the penalty it gives to the best answer.


# Below here is not finished

## Terminology

I'm given 6 *images*, each containing a grid of *figures* and figure
alternatives. A figure usually contains 1-3 *subfigures*, like a circle or a
rectangle. Each subfigure contains *properties* with assigned *values*.

A *figure comparison* compares two figures like A and B, but a
*comparison comparison* compares two figure comparisons.

## Syntax of representations

The properties of the figures are only described from the subfigures
perspective. I use the human readable `.yaml` format since that gets parsed to
a python value using standard libraries. `.yaml` is inherently hierarchical and
I've taken that to my advantage. Furthermore I try to follow the DRY principles
in my representation, if the shape-property of a subfigure is not set, my
program automatically sets it to the id of the subfigure.

[here]: http://pypi.python.org/pypi/PyYAML

