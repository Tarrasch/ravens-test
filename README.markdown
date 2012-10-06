% Arash Rouhani
% Project 2 in Knowledge Based AI
%

# NOTE

Hi, the design report is not done. I've just included the information needed to run
the program here. The program itself if however complete in the sense that it
answers the questions.

## Installation and running the program

      $ python ArashRouhani_Project_2.py

Works for me. In the unlikely case that you don't have pyyaml, I've
included the lib in the zip. If that is not working because you have
python 3, you can download the source [here] and replace the `yaml`
folder with the one in the **source** (either `.zip` or `.tar.gz`)
archive from the `lib3` folder.

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

