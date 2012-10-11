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

## Running the program

      $ python ArashRouhani_Project_2.py

Works for me. It takes one minute on my machine.  In the unlikely case that you
don't have pyyaml, I've included the lib in the zip. If that is not working
because you have python 3, you can download the source [here][pyyaml] and replace the
`yaml` folder with the one in the **source** (either `.zip` or `.tar.gz`)
archive from the `lib3` folder.

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

In other words, It finds the pattern that a move in the `down` direction
is to decrease the sectors starting angle by 90 degrees, which simply
means rotating clockwise by 90 degrees. For right direction it instead
choose to increase it by 90.

The last `20` is the penalty it gives to the answer.

## Representations

The representations describes the grid and each alternative figure as mentioned
in the terminology. They are in the `.yaml` format so I get the parsing for
free.

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
  3. Define `s(subfig)` = True iff any property-value of subfig is in subset

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

## Analysis of architecture

Here is the critique and analysis of this architecture.

### The general approach

My solution entirely relies on that answer frame for all the ravens analogy
problems is like this: *In direction d~1~ has pattern p~1~ and direction d~2~
has pattern d~2~*. So in a 3 by 3 problem, if the first rightward movement has
one pattern and the second right movement a completely different. It's unlikely
that this program will solve it.

### The modification is too general

My representation for the eighth problem is a bit cheaty. Naturally, a
straight triangle should have `rotation=0` and a flipped one
`rotation=180`. However, I've adjusted my representation so the programs
can see it as incremental rotations.  The core issue is of course that
my program don't know that when we're talking about rotation, it should
count modulo 360! Then we didn't need to contrive our representation
like we've had. But that modification doesn't fit well in my
architecture. But, if my program were less general in the kind of
properties and values you can have, say if you restricted it to just
position, rotation, color and shape. Then it's very natural to implement
"special cases" like that the rotation should be counted modulo 360.

### Circular value-transformations

The transformation filters are very powerful because they can be composed.
However, there is an interesting problem with composing the
transformation functions.

Take a look at the eighth figure again. Instead of thinking that the
subfigures have a rotation, think of them having either `flipped=no` or
`flipped=yes`. Now, a move in either the right or the down direction
will cause `yes` to be `no` and `no` to become `yes`. Can two combined
transformation filters handle this? It might seem so to begin with. Just
construct two filters:

      t_1 = for (figs where flipped=yes) inplace (set flipped=no)
      t_2 = for (figs where flipped=no) inplace (set flipped=yes)

While it seems like combining these will work as expected, it actually
will not. Define `t(fig) = t_2(t_1(fig))`.  What happens if we throw in
a flipped subfigure? First `t_1` will unflip it and then `t_2` will get
an unflipped image which it will then flip back!

In conclusion, the transformation filter is extremely powerful since it
can compose with ohter transition filters to create more advanced ones.
But alternations of a property (like flipping), which is typical for
analogy tests, is not solved with this method.

As a consequence of this weakness, I couldn't make a good enough
transformation filter that solves the fifth image. Instead I just wrote
a the selection filters. Note that a transformation filter would have
worked for the fifth image if it weren't for this circular problem.  For
the right direction one could express how the rod in a circular pattern
goes `.. --> vertical --> horizontal --> nonexistent --> ..`. A similar
pattern exists for the diagonal direction but with the shape types
instead.

# Part 2 - A researchers point of view

## An example

Here is an example showing that my solution scales polynomially in the
number of subfigures, it's rather the complexity of the pattern that
pushes the boundraries. The representation of this file is in
`reps/t1.txt`

    +--------------+----------------+---------------+
    |              |                |               |
    |              |                |       #       |
    |              |       #        |       #       |
    |     #        |       #        |       #       |
    |     #        |       #        |       #       |
    |   #####      |    #######     |   #########   |
    |              |                |               |
    |              |                |               |
    +--------------+----------------+---------------+
    |              |                |       #       |
    |              |       #        |       #       |
    |     #        |       #        |       #       |
    |    ###       |     #####      |    #######    |
    |              |                |               |
    |              |                |               |
    +--------------+----------------+---------------+
    |              |                |               |
    |              |                |               |
    |              |       #        |               |
    |     #        |      ###       |       ?       |
    |              |                |               |
    |              |                |               |
    +--------------+----------------+---------------+

          1                2                3              4                5
    +--------------+----------------+---------------+----------------+---------------+
    |              |                |               |                |               |
    |              |                |       #       |                |       #       |
    |              |       #        |       #       |       #        |       #       |
    |     #        |      ###       |     #####     |       #        |       #       |
    |              |                |               |       #        |       #       |
    |              |                |               |    #######     |   #########   |
    +--------------+----------------+---------------+----------------+---------------+

In this visual representation each `#` is one subfigure. So the biggest
figure has 17 subfigures.

My program doesn't solve this. But I thought it would! For my program to
have a chance at this I tweaked the parameters a bit. The composition
was set to depth 3 so it can add one block for all the three kinds of
selection (max x, min x, max y). Furthermore, I also removed most features.
The features it had selectionwise is *max/min by x/y* and
*increment/decrement x/y*. Yet the program can't solve this?

In fact, I designed this particular problem to show off the power of
composing transformation filters. At first glance it should work!  The
problem is the figure with only one subfigure cause problems very alike
the circular problems we had earlier. One sound transformation could be
:

  1. Copy all figures with max x-coordinate and modify `xpos+=1`
  1. Copy all figures with min x-coordinate and modify `xpos-=1`
  1. Copy all figures with max y-coordinate and modify `ypos+=1`

Indeed, for each step we only select one single subfigure as desired.
But for the figure with only one subfigure, the third step will actually
select 3 subfigures since the first two steps each created one subfigure
which will have the same y coordinate.

To prove that my program otherwise works, I did run my program on a
modified image (not pictured) where each figure in the grid is of one
size bigger, that is having 3 more subfigures than the original problem.
I called this representation `reps/t2.txt`. This one get solved as
expected, here is the program output:

    --------------------------------------------------------
    Solution to problem t2 is:
    (4,
     [(for (min by x) remove -- and then for (max by y) remove -- and then for (max by x) remove,
       'down'),
      (for (max by y) copy (inc `y`s by 1) -- and then for (max by x) copy (inc `x`s by 1) -- and then for (min by x) copy (inc `x`s by -1),
       'right')],
     240),

Note, I also fixed a minor bug with how to remove images in order to produce this result.

These two examples do a superb job in showing off both the
strenghts and weaknesses in my program. The strength being that it can
discover a quite complicated pattern and handle many subfigures. On the
downsides, the combinatorial explosion of filters created when wanting 3
transformations required me to disable alot of features to decrease the
amount of filters. Furthermore, it didn't solve the first problem
because of issues with the way we compose transformations, we discussed
this earlier in the report.


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

