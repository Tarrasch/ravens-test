% Project 2 in Knowledge Based AI
% Arash Rouhani
%

I've decided to split my design report into two parts, one describes my project
as a software engineer would, in the second part I'll analyze my project as a
researcher. But first, some basic terminology.

## Terminology

I'm given 6 *images*, each containing a grid of *figures* and 4 to 8
figure alternatives. A figure usually contains 1-3 *subfigures*, like a
circle or a rectangle. In other words, a figure is a list of subfigures.
Each subfigure contains *properties* with *values*.

A *transition* is seen as a pair of two figures. Intuitively the first
figure is the original one and if you "follow the pattern" you'll get
the second figure. So I'll only use the word transition when a pattern
is in context.

# Part 1 - A software engineers point of view

As a software engineer I'll say how one can run my program,
describe the programs architecture and specify the format of my knowledge
representation.

## Running the program

      $ python ArashRouhani_Project_2.py

Works for me. It takes one minute on my machine.  In the unlikely case that you
don't have pyyaml, I've included the lib in the zip. If that is not working
because you have python 3, you can download the source [here][pyyaml] and replace the
`yaml` folder with the one in the **source** (either `.zip` or `.tar.gz`)
archive from the `lib3` folder.

### Experimenting with the programs verbosity

Also, please check `ArashRouhani_Project_2.py`. By uncommenting a
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

In other words, It finds the pattern that a move in the `down` direction
is to decrease the sectors starting angle by 90 degrees, which simply
means rotating clockwise by 90 degrees. For right direction it instead
choose to increase it by 90.

The last `20` is the penalty it gives to the answer.


## Syntax of representations

The properties of the figures are only described from the subfigures
perspective. I use the human readable `.yaml` format since that gets parsed to
a python value using standard libraries. `.yaml` is inherently hierarchical and
I've taken that to my advantage. Furthermore I try to follow the DRY principles
in my representation, if the shape-property of a subfigure is not set, my
program automatically sets it to the id of the subfigure.

## The architecture and rationale

In this quite extensive chapter I'll describe the different design
choices I've made and with a short motivation why. Also, I try to link
each sub chapter with the actual code module it corresponds to.

### Directions

For each alternative the program looks at, it will look for a pattern in
three directions: Downwards, rightwards and diagonally (down-right
diagonally only though). The motivation for the diagonal direction is
that the fifth problem becomes easier when contemplating the diagonal.
In the end my program will choose the alternative that performed best
performed best on it's two most favorable directions. This way, we'll can
handle each direction independently, this greatly simplifies our task.

  * See `src/directions.py`

### Filters - the fundamental object in my program

A filter is simply a function representing a pattern. The function `f()`
will take two figures as inputs. `f(fig_A, fig_B)` will return true only if a
transition from `fig_A` to `fig_B` is following the pattern.

In order to make natural patterns compare better to contrived patterns.
A filter is also holding a `punishment` number. For value inspection
purposes, a filter also contains a `message`, it could for instance be
`"for (All) inplace (inc ``start``s by -90)"` which means that the
pattern is to subtract 90 from all subfigures `start` value.

But what's the equation for `f()`? Well, there are many clever patterns,
however, as I saw it I needed two kinds of implementations of filters to be
able to solve the 6 given input images. Transformation and selection filters.

  * See `src/filter.py`

#### Transformation filters

A transformation filter implements `f()` like this:

    f(fig_A, fig_B) = transform(fig_A) == fig_B

The `transform` function will take a figure transform it. It can delete,
copy and modify subfigures. When modifying a subfigure, it can change the
values of its properties, like increment it's `x-position` value. With
simple function composition, two transformation filters can be combined
into one.

  * See `src/pool/transforms.py`
    * Which is using `src/pool/modifiers.py`
    * and `src/pool/selectors.py`

#### Selection filters

A selection filter implements `f()` like this:

    f(fig_A, fig_B) = select_parts_of(fig_A) == select_parts_of(fig_B)

A selection filter checks if two figures are identical if you select out
some subfigures based on their properties. This filter was introduced
because of the lack of simple transformation patterns in the fifth
image.  In the fifth image you can use a selection that only looks at
circles, squares and crosses in the right direction. Similarly you only
look at the rod and the rotated rod in the diagonal direction.

  * See `src/pool/selectorfilter.py`

### Where filters come from

How do we create the filters? Obviously the filters must adapt for new
input images. So when creating filters we must know some sample
transitions. These are taken from the grid.

  * See `src/pool/pool.py`

### Using filters to select the correct answer

When we have generated filters from our grid. We try out each filter on
the last transition to see if the pattern matches. Here "last
transition" refers to the transition to the alternative figure that
maybe fits in the bottom right corner. We then choose the filter who has
the minimum punishment score. There will in fact always be one filter
that accepts the transition because we always generate one accept all
filter with a very high punishment.

By now the reader should have noticed that my solution entirely relies
on that answer frame for all the ravens analogy problems is like this: *In
direction d~1~ there is pattern p~1~ and in direction d~2~ there is
pattern d~2~*. So in a 3 by 3 problem, if the first rightward movement has one pattern and
the second right movement a completely different. It's unlikely that
this program will solve it. [Move to analysis!!!]

  * See `src/solve.py`

### Unit tests

For my owns sake when developing this software I wrote unit tests to
ensure that my functions work as I expect them. One can run the
unit tests simply with

    python -m unittest discover

## Algorithms

The algorithms worth discussing are:

  * Generating transformation filters
  * Combining two transformation filters into one
  * Generating selection filters

I choose these because these are the components where different minds
would implement differently. Meanwhile the other parts doesn't
require any creativity.

### Generating transformation

To generate a transformation you basically need to define a function
`t()` taking a figure and returning another figure. I divided this
function into three parts.

  *  Decide which subfigures you're gonna transform. We call this the
     *selection* part. (see
     `src/pool/selectors.py`)
  *  Decide the modification you're gonna apply. We call this the
     *transformation* part. (see
     `src/pool/modifiers.py`)
  *  Decide if you're gonna keep copies of the figures you modify.  We call
     this the *action* part.


Some examples where this works very well:

  * In image two in the downwards direction, when squares becomes
    circles, you build the transformation like this: Let the selection
    part be *select all* and the transformation part be *set property
    'shape' to value 'circle'*. Since we are gonna modify both subfigures
    in the rightmost downward direction we see the convenience in having
    a selection part that can be specified to modify all subfigures.

  * In the last image, the one with duplication of triangles. We see
    that the selection *pick all subfigures with maximum x-coordinate*
    together with a copy-modification *increase the x-coordinate*
    very simply captures the rightward directions pattern.

### Combining two transformation filters

To combine *t~1~()* with *t~2~()* is very trivial, just construct
*t(fig) =  t~2~(t~1~(fig))*.

This works well for example on the second image's rightward direction.
Which basically is *move all subfigures, to the left side* followed by
*copy all subfigures to the right side*. Note how the *all* quantifiers
only refer to one subfigure, but it works exactly how we want it too.

### Generating selection filters

Remember, a selection filter implements a filter with *f()* defined like

    f(fig_A, fig_B) = select_parts_of(fig_A) == select_parts_of(fig_B)

I let `select_parts_of` be a function that simply goes through the figure
(which is a list of subfigures) and then selecting out only some of the
subfigures. A subfigure is selected if it fulfills a selection function say
*s()*.  Hence, each selection filter I construct will have the same
*select_parts_of()* but with a different *s()*. Here is how I construct the
*s()* functions.

  1. Create a set with all possible property-value pairs
  2. Loop through all the subsets of size *sz*
  3. Define `s(subfig) = True if any property-value is in subset`

I loop with the variable *sz* from 2 to 5, these values
are somewhat arbitrary, but with a higher value there are
more ways to pick out the subset and more filters will be produced. I
consider a filter as "smarter" and hence having less punishment the
larger *sz* is.

This works great in the fifth image, you filter on the property-value subset
`{('circle', 'circle'), ('square', 'square'), ('cross', 'cross')}` in the right
direction. Here `('circle', 'circle')` represents a property-value tuple. The
properties don't need to be distinct. For example in the diagonal direction the
subset is `{('line', 'v0'), ('line', 'v90')}`. In human text this can be
interpreted as "The line parts of either rotation don't change on diagonal
transitions".  The properties and values I used in this paragraph are taken
from my representation of the fifth image.

# Part 2 - A researchers point of view

## Ablation experiments

Luckily, the structure of my program is suitable for ablation
experiments.  In the files
`src/pool/{selectors,modifiers,selectorfilter}.py`, each `yield`
statement corresponds to one way of reasoning and can be commented out.
Also, you can drop the number of compositions you do for the
transformation filters, that means the program can only do single-step
transformations.

So, let's get our hands dirty by doing some ablation experiments, I will run
the modified programs on the six given and the two extra images. The experiments
I've done are only a few of all possible combinations to remove features.

### Removing transformation compositions

Wow! The programs runs a lot faster now. We observe that the the set of
problems solved now are only *1, 4, 5, 6*. The fifth problem is still solved
because it relied on the selection filters not the transformation filters. As
for 1, 4 and 6 it's simply because that they only need one transformation.

### Removing the modification part in transformation filters

If I remove the possiblity to set a specific property to a value or do
increments/decrements on that value. We see that only *4 and 5* are solveable.
5 As of earlier reason and 4 because the subfigures don't have only parts of
them modified.

### Removing the selecting part in transformation filters

Removing the possiblity to select the subfigures who have the maximum/minimum
value had a very interesting consequences. I thought that it would no longer
solve the 6th problem, after all, the max value selector was designed with that
image in mind. However, it seems that a selection filter saw the unique pattern
that the subfigures with `x=0` stays the same in the right direction and the
subfigures with `y=0` stays the same in the down direction! I never thought
about that pattern! Indeed, that solution reaches the correct answer for the
wrong reason and a "`L`-shaped" figure fits that pattern too.

### Removing the action part in transformation filters

If we don't allow copying or deletion of subfigures, exactly what we expected
happens, it solves *all except for 2, 6 and 8*.



[pyyaml]: http://pypi.python.org/pypi/PyYAML

