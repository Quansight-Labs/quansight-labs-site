<!--
.. title: But What are Traitelts ?
.. slug: what-are-traitlets
.. date: 2020-08-xx 22:00:00 UTC-00:00
.. author: Matthias Bussonnier
.. tags: Labs, IPython, traitlets, historical
.. category:
.. link:
.. description:
.. type: text
-->

You probably have head the name, you likely have used them, but you likely are
still confused ? What are `trailtlets`; in the following we'll discuss a bit
what traitlets are, where they came from, what is their use, and a tiny bit of
historical context.

<!-- TEASER_END -->

Traitlets 5.0 has recently been released / will be released soon, this was a
multi-year process to bring new features and cleanup the codebase without
breaking backward compatibility. Traitlets are used everywhere in
Jupyter/IPython, for configuration and CLI parsing.

Originally traitlets are a pure python limited implementation of the Enthought
`Traits` library included in the IPython (pre-jupyter) code base; Traits used
compiled code which at the time was a tough requirement for a Python REPL. Trait, and
traitlets initially offer runtime type checking, cohesion and validation at run
time. Traitlets were split as their own packages during [The Big Split](https://blog.jupyter.org/the-big-split-9d7b88a031a7).


Let's look at a traitlets usage example; IPython's `autocall`  feature and how
its value can be changed from the CLI, config file, and where this is defined in
the code.

Here is an extract of IPython main class:

```python
from traitlets import SingletonConfigurable, Enum

class InteractiveShell(SingletonConfigurable):

    ...

    autocall = Enum((0,1,2), default_value=0, help=
        """
        Make IPython automatically call any callable object even if you didn't
        type explicit parentheses. For example, 'str 43' becomes 'str(43)'
        automatically. The value can be '0' to disable the feature, '1' for
        'smart' autocall, where it is not applied if there are no more
        arguments on the line, and '2' for 'full' autocall, where all callable
        objects are automatically called (even if no arguments are present).
        """
    ).tag(config=True)

    ...
```

The ``autocall`` class attribute will be converted at instantiation to an
instance ``property``, in particular an ``Enum``, which values are ensured to be
either `0`,`1`, or `2`. Traitlets provides a number of utilities to decide
whether assigning incorrect values should raise an exception; or use some other
logic to guess the correct value.

While type – and value – checking at runtime is a nice features; most of these
options are usually user preferences. Traitlets provides way to automatically
create config files with help, as well as CLI parsing.

In the above you see that the traitlets have a ``help`` string, a
``default_value`` and is marked with ``config=True`` this allow any of the
jupyter app to automatically generate config files; decide of the option name
and document it. No need for the developer to decide of a configuration
parameter name.

On a brand new machine with IPython installed you will find the following in
yout `~/.ipython/profile_default/ipython_config.py`:

```
...
## Make IPython automatically call any callable object even if you didn't type
#  explicit parentheses. For example, 'str 43' becomes 'str(43)' automatically.
#  The value can be '0' to disable the feature, '1' for 'smart' autocall, where
#  it is not applied if there are no more arguments on the line, and '2' for
#  'full' autocall, where all callable objects are automatically called (even if
#  no arguments are present).
#c.InteractiveShell.autocall = 0
...
```

And if you update this file, uncomment the last line and change the value, you
guessed it, new instances of InteractiveShell will have a new default value.

Alternatively, traitlets also parse the command lines, so ``ipython
--InteractiveShell.autocall=3`` will take precedence over configuration files
and start IPython with this new confirm option.


Adding an option is a breeze, for example IPython can reformat your code with
black since [this pull request](https://github.com/ipython/ipython/pull/11734/files),
beyond the logic to actually do the reformat the complete diff to add the
options to the CLI, configuration file with help and automatic generation of
this option in sphinx doc is as followed.


```diff
@IPython/terminal/interactiveshell.py:98
Class TerminalInteractiveShell(InteractiveShell)
... snip ...
+     autoformatter = Unicode(None,
+        help="Autoformatter to reformat Terminal code. Can be `'black'` or `None`",
+        allow_none=True
+    ).tag(config=True)
```

If you have an application or library which potentially have a really large
number of configuration knobs and want to isolate changes;
Traitlets can help you expose all of those cleanly to a user.


# Configure what you do not yet know about

In an application with few parameters and only a couple plugins it might be
relatively straitforward to provide options and cli arguments; this becomes
harder when arbitrary plugins are involved and those plugins have arbitrary
configuration options you may, or may not know at startup time. 

One good example is JupyterHub; JupyterHub have spawners that decide how
notebook servers are started. You can find how to [use a custom
spawner](https://jupyterhub.readthedocs.io/en/stable/reference/spawners.html#writing-a-custom-spawner),
and many institutions have only minimal changes to Spawner to accommodate their
use case. It is critical to make it as simple as possible to provide
configuration options and make them available from Jupyter Configuration files.

Using a custom Spawner is simple:

```
c.JupyterHub.spawner_class = 'mypackage:MySpawner'
```

and this allow you  to also arbitrarily configure MySpawner with

```
c.MySpawner.myattribute = 'new value'
```

Traitlets is aware of class hierarchy, thus when `MySpawner` inherit from the
default Spawner, all `c.Spawner...` options will affect `MySpawner`, but
`c.MySpawner...` options will of course not affect super classes or siblings. 

It is thus also easy to configure differently siblings; a good  example is CLI
IPython vs IPykernel used in notebooks and lab. Both applications are subclasses
of InteractiveShell. Respectively ZMQInteractiveShell and
TerminalInteractiveShell.

I can thus configure both with `c.InteractiveShell.attribute=`, only CLI with
`c.TerminalInteractiveShell.attribute=`, or only notebooks-like with
`c.ZMQInteractiveShell.attribute=`; On my own machine I for example have by
default matplotlib in inline mode only for kernel and not terminal.


Thus if you have an application or library with a number of plugins, an for
which configure ability could be thoughts as tree-like for a class hierachy;
traitlets can help you. 


# Other functionalities 

## Observability

Beyond the configure ability part is observability; as we already had a great type
system with hooks, and the sometime you may want to mutate configuration of a
running application, traitlets allow you to observe value and propagate them to other places. 


To look at the above example with code reformatting, the reformatter con be
change dynamically things to the following:


```python

Class TerminalInteractiveShell(InteractiveShell)
...

    @observe('autoformatter')
    def _autoformatter_changed(self, change):
        formatter = change.new
        if formatter is None:
            self.reformat_handler = lambda x:x
        elif formatter == 'black':
            self.reformat_handler = black_reformat_handler
        else:
            raise ValueError
```



This is what powers
[ipywidgets](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Events.html?highlight=link#Linking-Widgets).

This can be useful to glue together models where parameter need to be
synchronized and react to changes.


## Dynamic default

Traitlets support [dynamic
default](https://traitlets.readthedocs.io/en/stable/api.html#dynamic-default-values)
if your default value may depend on some context. Configuration are also by
default Python scripts (but can be Json), so user config files can be share
across machines and have dynamic values.


## Context base configuration

Object configuration can also look at the creator of the object at instantiation
time.

```
c.Foo.Bar.attr = 1
c.Qux.Bar.attr = 2
```

With the above, `Bar()` object created by `Foo`, or by `Qux` will get different
default values; This is for example used in nbconvert; to decide which options
to activate depending on whether you to `--to=pdf`, or `--to-html`

## flag and aliases

Long flag names like `--InteractiveShell.debug=True` can be cumbersome to type.
That why Traitlets provide aliases and flags, so that `ipython --debug`, will
set `debug=True` to enable logging  on all classes supporting it; while still
allowing you to tweak the login level used on a per-class basis.


# Limitation

Of course with great power comes some limitations:

 - Your class names and attributes names become part of API
 - As configuration is loaded/read before any potential plugin are loaded it is
   impossible to detect typos or invalid configuration options.
 - Rely heavily on metaclass, so can add a construction cost to your objects,
   and can be hard to debug


# Going further


If you want to learn more, see [this JupyterCon 2018
talk](https://www.youtube.com/watch?v=_gYEVTaNuKU), and the [doc](https://traitlets.readthedocs.io/)

Try the new 5.x version and let us know if you have questions.















