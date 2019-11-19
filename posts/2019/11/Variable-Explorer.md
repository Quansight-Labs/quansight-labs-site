<!--
.. title: Variable Explorer improvements in Spyder 4
.. slug: Variable-Explorer-improvements-in-Spyder 4
.. date: 2019-11-12 12:00:00 UTC-05:00
.. author: Daniel Althviz
.. tags: Labs, Spyder
.. category: 
.. link: 
.. description: 
.. type: text
-->

Spyder 4.0 (https://www.spyder-ide.org/) will be released soon and it reflects the effort of the team to improve the users' experience. It contains lots of interesting new features that we will like you to check out! In this case, we will be talking about the improvements made to the Variable Explorer.

These include support to inspect any kind of Python object through a new viewer, the ability to filter and search for variables by name and type, and support for dataframes whose indexes have multiple dimensions.

It is important to mention that some of the above improvements were possible through the integration of code coming from two different projects into our own. The first of them is called [gtabview](https://github.com/TabViewer/gtabview), whose code was used for the implementation of multi-dimensional Pandas indexes. And the second one is [objbrowser](https://github.com/titusjan/objbrowser), used for viewing arbitrary Python objects.

<!-- TEASER_END -->


## New viewer for arbitrary Python objects


For Spyder 4 we added a long-requested functionality: inspecting any kind of Python object through the Variable Explorer. For a long time Spyder has had very good support to view and edit a small subset of Python objects: Numpy arrays, Pandas dataframes and series, and collections (i.e. lists, dictionaries and tuples). Other objects were displayed in a table-like view, and inspecting any of their attributes required showing a new table,

![Python Viewer](/images/spyder-variable-explorer/python-viewer.png)

This made very cumbersome to use this functionality, which was the reason why arbitrary Python objects were hidden by default from the Variable Explorer view.  
In this version we decided to integrate the excellent [objbrowser](https://github.com/titusjan/objbrowser) project, by Pepijn Kenter ([@titusjan](https://github.com/titusjan)), which provides a tree-like view of Python objects, for a much simpler and comfortable way to inspect them.

![Python Viewer Metadata](/images/spyder-variable-explorer/python-viewer-metadata.png)

As can be seen above, this viewer will also allow users to have access to some extra metadata about the inspected object, such as its documentation, source code and the file that holds it.  
It is very important to note that this work was accomplished thanks to the generosity of Pepijn, who kindly changed the license of [objbrowser](https://github.com/titusjan/objbrowser) to allow us integrating it with Spyder.
To expose this new functionality we also decided to turn off the Variable Explorer option called “Exclude unsupported types” and introduce a new one called “Exclude callables and modules” (turned on by default) to display a much larger fraction of objects after a file or cell execution.

![Exclude callables modules](/images/spyder-variable-explorer/exclude-callables-modules.png)

Finally, we added a context-menu action to allow using the object explorer viewer for all objects, regardless if they have a default viewer or not.

![View object explorer](/images/spyder-variable-explorer/view-object-explorer.png)

## Multi-index support in the dataframe viewer

One of the first enhancements we did to the Variable Explorer in Spyder 4 was adding support for multi-dimensional indexes to its dataframe viewer. In Spyder 3 the support was very limited, which made inspecting those indexes a painful experience:

![Multi-index support](/images/spyder-variable-explorer/multi-index-support.png)

For Spyder 4 we took advantage of the work done by Scott Hansen ([@firecat53](https://github.com/firecat53)) and Yuri D'Elia ([@wavexx](https://github.com/wavexx)) in their [gtabview](https://github.com/TabViewer/gtabview) project for this very purpose. The main element we took from it was its improved management of column and table headings, which allowed us to display the index shown above in a much nicer way:

![Table headings](/images/spyder-variable-explorer/table-headings.png)

## Fuzzy filtering of variables

This version also includes the ability to filter variables in the current namespace to focus only on the ones you are interested in. This filtering is done in a fuzzy way by matching any letter of text entered in the search field with the type and name of all available variables.
To access this functionality you need to press the keyboard shortcut `Ctrl+F` when the Variable Explorer has focus or by pressing the magnifying glass icon on top,


![Filter variables](/images/spyder-variable-explorer/filter-variables.png)

To remove the filtering, simply press `Esc` or `Ctrl + F` when the Variable Explorer is focused, or the magnifying glass icon again.

## Refresh while code is running

Finally, we restored the ability to refresh the Variable Explorer while code is running in the console. This was lost in Spyder 3.2, when we removed the old and unmaintained Python console. It’s coming back thanks to the fantastic work done by Quentin Peter ([@impact27](https://github.com/impact27)), who completely re-architectured the way the Spyder interface talks to the Jupyter kernels in charge of running code in our IPython console, by using [Jupyter Comms](https://jupyter-client.readthedocs.io/en/stable/messaging.html#custom-messages).

![Refresh](/images/spyder-variable-explorer/refresh.png)

This can be achieved by by pressing the refresh button on the Variable Explorer toolbar, or the the shortcut `Ctrl+R` when it has focus.



