<!--
.. title: Better Jupyter Interactive Sessions with Pyflyby
.. slug: better-interactive-jupyter-sessions-with-pyflyby
.. date: 2021-03-21 08:00:00 UTC-00:00
.. author: Matthias Bussonnier, Aaron Meurer, 
.. tags: Labs, Pyflyby, Deshaw
.. category:
.. link:
.. description:
.. type: text
-->

Few things hinder productivity more than interruption.  When you are deep in
a complex analysis and a notification, random thought, or unrelated error pops up, 
your train of thought can get lost.  This can be a frustrating experience.

Forgetting an import statement in an interactive session in Jupyter is one of
those experiences. This is especially frustrating when using typical
abbreviations, like `np`, `pd`, `plt` where to the human reader it is obvious
what is meant, but not to the computer. The time-to-first-plot, and the 
ability to quickly cleanup one's notebook afterward are critical to an enjoyable 
and efficient workflow. 

In this blogpost we'll present to you
[pyflyby](https://github.com/deshaw/pyflyby), a project and an extension to
IPython and [JupyterLab](https://github.com/deshaw/jupyterlab-pyflyby), which,
among many things, will automatically insert imports for you and tidy your
python files and notebooks. 

<!-- TEASER_END -->

# How to get pyflyby

If you are the [TL:DR;](https://en.wikipedia.org/wiki/Wikipedia:Too_long;_didn%27t_read) kind, 
head [here](https://github.com/deshaw/pyflyby), and if you are a terminal IPython user:

```
$ pip install pyflyby 
$ py pyflyby.install_in_ipython_config_file
```

You can now use IPython as usual, but you don't need to write most of the import statements.  Read on
for more.

JupyterLab users can also install [the JupyterLab
Extension](https://github.com/deshaw/jupyterlab-pyflyby) which is notebook
aware, enabling even more features. 

# What is pyflyby?

Pyflyby is a set of tools to improve interactive and non-interactive workflows in
Python.  Pyflyby provide a number of utilities and extensions that make day to day work
with Python faster or simpler.

![gif of pyflyby in action](/images/2021/07/pfb-autoimport.gif)

## Autoimport

As you see in the introduction gif, one of the
capabilities of Pyflyby is to automatically import modules and objects that are
commonly used, leading to simpler, faster and less disruptive coding. In a new
session this lets you for example type:

```python
sin(arange(10))
```

And Pyflyby will hook into the execution mechanism of Python, execute the
correct import when necessary, and inform you of it with a message (Explicit is better than
implicit):

```text
[PYFLYBY] from numpy import arange
[PYFLYBY] from numpy import sin
```

pyflyby will do the same when running a command line file via
the `py` executable replacing python.

Of course with the `jupyterlab-pyflyby` extension, not only will the imports be
executed, but those imports will be inserted in the first cell of your notebook. 

![pyflyby-jupyterlab animation](/images/2021/07/jlpfb.gif)

## tidy-import

Being able to seamlessly import the right libraries while exploring is useful.  
So is having scripts and notebooks with explicit and correct imports. 

Pyflyby expose the `tidy-import` command line tool to gather, insert, and format
imports in python files. This is similar to
[black](https://pypi.org/project/black/) and
[isort](https://pypi.org/project/isort/) but with different styling options; though
neither of those are able to infer missing imports, which Pyflyby does.

`tidy-import` would thus include the imports to pandas and matplotlib, like in the
following example, and ask you whether to update the file.

```diff
$ tidy-imports example.py
[PYFLYBY] example.py: added 'import pandas as pd'
[PYFLYBY] example.py: added 'from matplotlib import pyplot'
--- example.py	2021-03-08 10:33:04.000000000 -0800
+++ example.py	2021-03-08 10:33:18.000000000 -0800
@@ -1,2 +1,7 @@
+from   matplotlib               import pyplot
+import pandas as pd
+
 data = pd.read_csv("./data/base-pop-2015.csv")
 pyplot.plot(data.population)

Replace example.py? [y/N]
```

## Other utilities

Pyflyby contains a number of other utilities to make it convenient to
manipulate or execute python code.  Refer to Pyflyby's 
[README](https://github.com/deshaw/pyflyby) for more information.

`py` is just one of my preferred ones. It is a Swiss Army Knife to either start
IPython or quickly execute commands from my shell without the need for imports. 
It supports many syntax options, allowing for quick calculation and making graphs. 

- Without any parameters, it will start IPython with the Pyflyby extension
  activated.
- With space-separated arguments, it will try to interpret them as Python
  function calls with the right imports.

```bash
$ py np.random.normal 0 1
[PYFLYBY] import numpy as np
[PYFLYBY] np.random.normal(0, 1)
-0.027577422117386
```

- or run a python expression when more control over the values is necessary:

```bash
$ py 'plot(scipy.stats.norm.pdf(linspace(-5, 5), 0, 1))'
[PYFLYBY] from numpy import linspace
[PYFLYBY] from matplotlib.pyplot import plot
[PYFLYBY] import scipy.stats
[PYFLYBY] plot(scipy.stats.norm.pdf(linspace(-5, 5), 0, 1))
[<matplotlib.lines.Line2D object at 0x132981940>]
```

![using pyflyby from bash to plot with matplotlib](/images/2021/07/py-exec-matplotlib.png)

`find-import` can be useful to find the function you are looking for in many
libraries by returning the relevant import.

```bash
$ find-import norm
from scipy.stats.distributions import norm
```

# Highly technical with a wide Python supported codebase

If you are looking for an atypical codebase to learn about new datastructures or
programming paradigms, the [Pyflyby
codebase](https://github.com/deshaw/pyflyby) is worth looking into. You will
find that its use of modules and programing concepts are rarely found in
more classical data science focused libraries. For example:

 - Pyflyby will do some non-trivial manipulation of the Python Abstract Syntax
   Tree (AST). The Python AST represents the code you write in the form of a
   tree, and Pyflyby uses it to find the missing imports and insert them. This
   is a feat in itself, but Pyflyby manages to do so even with the Python AST's
   exact representation changing with almost every minor release. 

 - Pyflyby also exposes some programing paradigms that might not be familiar to
   everyone. There I discovered [Aspect-Oriented
   programming](https://en.wikipedia.org/wiki/Aspect-oriented_programming), which
   also shows some of the flexibility of the Python programming model.

# Contribution to the wider ecosystem

While Pyflyby is itself a really useful project, its impact goes beyond this. 
It pushes the limits of what is done with the Python ecosystem and has found 
many limitations and bugs in Python and IPython through the years.  Fixing those bugs is a
[non-zero-sum game](https://en.wikipedia.org/wiki/Zero-sum_game) and has taken
time.

# Conclusion

Pyflyby is not only a tool worth using, it is in a rare category in
which you wonder how you were able to work without it. 

It has also not only been
created and maintained by highly qualified and efficient developers, but by a
team that understands the technical and sociological challenges of Open Source.
They are also not afraid to take the long and difficult road when it's the right
thing for the community.

# Acknowledgements

Pyflyby was created by Karl Chen and is supported by the [D. E. Shaw
group](https://www.deshaw.com/) in collaboration with [Quansight](https://www.quansight.com).











