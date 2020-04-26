<!--
.. title: The people behind Spyder 4
.. slug: the-people-behind-spyder-4
.. date: 2020-03-05 14:00:00 UTC-05:00
.. author: Carlos Córdoba
.. tags: Labs, Spyder
.. category:
.. link:
.. description:
.. type: text
-->

After more than three years in development and more than 5000 commits from 60 authors around the world, Spyder 4 finally saw the light on December 5, 2019!
I decided to wait until now to write a blogpost about it because shortly after the initial release, we found several critical performance issues and some regressions with respect to Spyder 3, most of which are fixed now in [version 4.1.2](https://github.com/spyder-ide/spyder/releases/tag/v4.1.2), released on April 3rd 2020.

<!-- TEASER_END -->

This new release comes with a lengthy list of user-requested features aimed at providing an enhanced development experience at the level of top general-purpose editors and IDEs, while strengthening Spyder's specialized focus on scientific programming in Python.
The interested reader can take a look at some of them in [previous](https://labs.quansight.org/blog/2019/11/variable-explorer-improvements-in-Spyder-4/) [blog](https://labs.quansight.org/blog/2019/11/File-management-improvements-in-Spyder4/) [posts](https://labs.quansight.org/blog/2019/08/spyder-40-beta4-kite-integration-is-here/), and in detail in our [Changelog](https://github.com/spyder-ide/spyder/blob/master/CHANGELOG.md#version-400-2019-12-06).
However, this post is not meant to describe those improvements, but to acknowledge all people that contributed to making Spyder 4 possible.

Spyder 4 is the first version developed with financial support from multiple companies, as well as donations by the international user community.
However, as a project, we couldn't have been able to reach the level of maturity needed to receive and handle that support without the pivotal opportunities Travis Oliphant, former CEO of Anaconda and current leader of Quansight, gave me to work in Scientific Python.
Thanks to him, I became part of Anaconda Inc. in 2015; I was able to hire a small small team to improve Spyder within Anaconda in late 2016; and I was hired by Quansight to work solely on Spyder in 2018.
As with other projects in our ecosystem, such as [Bokeh](https://github.com/bokeh/bokeh), [Dask](https://github.com/dask/dask) and [Numba](https://github.com/numba/numba), Spyder benefited immensely from Travis' trust in the role these efforts and ours could play in the future.
He certainly believed in the vision their maintainers worked so hard to make a reality, even if their beginnings were humble and their chances of survival uncertain.
Therefore, my first big acknowledgment is to Travis: thanks for giving us a chance!

I also want to thank our community for its continued support.
As I've witnessed during my years as Spyder's lead developer, many newbies and veterans alike keep choosing Spyder as their primary tool for scientific programming in Python.
It's really you, the members of this fantastic community, which keep Spyder relevant in a highly competitive field by using and contributing back to it.
I'm also honored and humbled to have received such first-class additions to Spyder 4 from our volunteer contributors as significant improvements to our documentation, thanks to [CAM Gerlach](https://github.com/CAM-Gerlach).

Furthermore, when the future looked grim, after my team and I were let go from Anaconda at the end of 2017 (not by Travis' decision), a lot of users came to our rescue by making donations through our [Open Collective page](https://opencollective.com/spyder).
That, and a Numfocus development grant we received the next year, filled us with confidence and allowed us to continue with Spyder's development in 2018, even after losing part of our team in the process.

Last year it was also a pleasant surprise to learn that several companies were interested in seeing Spyder prosper and thrive.
Through Quansight Labs and its [Community Work Order](https://labs.quansight.org/blog/2019/05/community-driven-opensource-funded-development/) concept, we were able to sign contracts with two of them: [TDK-Micronas](https://www.micronas.tdk.com/en) and [Kite](https://kite.com/).
Their support was critical to finish Spyder 4 because it allowed me to hire most of my old Anaconda team back, plus two new additions, to work full-time on the project.
Therefore, I can't thank them enough for showing up just at the right time!

And finally, even when I am often seen as the public face of Spyder, due to my presence in our [issue tracker](https://github.com/spyder-ide/spyder/issues) and [Stack Overflow](https://stackoverflow.com/users/438386/carlos-cordoba), it's really the Spyder team that is in charge of implementing new features and fixing most bugs.
So my last round of acknowledgments goes to them.
I was fortunate enough to convince some of the most talented Colombian software developers to work for the project, and to attract the interest of several other equally accomplished developers from around the world. All of them did a hell of a job in this release!

[Jean-Sébastien Gosselin](https://github.com/jnsebgosselin) contributed our new Plots pane in its entirety; [Quentin Peter](https://github.com/impact27) did a complete re-architecting of our IPython console, which enabled numerous improvements to our debugger; [Jitse Niesen](https://github.com/jitseniesen) added auto-saving functionality to our editor; [Brian Olsen](https://github.com/bcolsen) contributed the initial implementation of the `runcell` command; [Gonzalo Peña-Castellanos](https://github.com/goanpeca/) helped us to greatly improve the user experience of code completion and linting in the editor, implemented most of the enhancements to the Files pane, and refactored and improved our configuration system; [Edgar Margffoy](https://github.com/andfoy) single-handedly created a client to support the same [protocol](https://microsoft.github.io/language-server-protocol/) used by VSCode to provide completion and linting for lots of programming languages, added code snippet completions and vastly improved code folding in the editor; [Daniel Althviz](https://github.com/dalthviz) developed the necessary infrastructure to install and use Kite smoothly within Spyder, and added the new object viewer to the Variable Explorer; and our junior developers, [Stephannie Jimenez](https://github.com/steff456) and [Juanita Gomez](https://github.com/juanis2112), although still finding their way around our complex codebase, managed to make important contributions, such as improving the icons we use per file type in Files (Juanita), and allowing users to run code in an external system terminal on macOS (Stephannie).

I hope you all enjoy the results of this massive effort! And happy Spydering!!!
