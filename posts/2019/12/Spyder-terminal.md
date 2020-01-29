<!--
.. title: Creating the ultimate terminal experience in Spyder 4 with spyder-terminal
.. slug: creating-the-ultimate-terminal-experience-in-Spyder-4-with-spyder-terminal
.. date: 2019-12-23 16:00:00 UTC-05:00
.. author: Stephannie Jimenez
.. tags: Labs, Spyder
.. category:
.. link:
.. description:
.. type: text
-->

The [Spyder-Terminal project](https://github.com/spyder-ide/spyder-terminal) is revitalized! The new 0.3.0 version adds numerous features that improves the user experience, and enhances compatibility with the latest Spyder 4 release, in part thanks to the improvements made in the [xterm.js](https://xtermjs.org/) project.

<!-- TEASER_END -->

## ES6/JSX syntax
In the first place, we were able to update all the old JavaScript files to a ES6/JS syntax. This change simplified the code base and maintenance for the terminal. Also, it allows us to extend the project in an easier way to new functionalities that the xterm.js API offers. In order to compile this code and run it inside Spyder we migrated our deployment to Webpack. Additionally, the tests for the client terminal were updated to support the new syntax.

## Multiple shells per operative system

A new feature added to the terminal is that the user can configure which shell to use in the terminal. Now the terminal is able to start with `bash`, `sh`, `ksh`, `zsh`, `csh`, `pwsh`, `tcsh`, `screen`, `tmux`, `dash` and `rbash` in UNIX systems and `cmd` and `powershell` in Windows. This option is given on the preferences pane and a restart of Spyder is required to apply the changes.

![UNIX shell options for starting the terminal](/images/spyder-terminal/shells.png)

This is a great feature because it allows the user to determine their shell interpreter among the ones that are installed in their systems. In this way, Spyder-terminal can be configured with any of the existing shells as long as it is available on their machine. Some examples of the configurable options of the interpreter are shown below, with bash and tcsh.

![Spyder-terminal running on a bash shell](/images/spyder-terminal/bash.png)

![Spyder-terminal running on a tcsh shell](/images/spyder-terminal/tcsh.png)

## Theme configuration

Another big change in this new version of the terminal is that now all the Spyder themes options are available. In this way, when a user changes the palette that wants to use with Spyder, automatically the terminal will use the same theme including the font size. Some examples of the new supported themes for the terminal are shown below.

![Spyder-terminal with minimal color theme](/images/spyder-terminal/minimal.png)

![Spyder-terminal with Spyder dark color theme](/images/spyder-terminal/spyder-dark.png)

Building on the look and feel of the plugin, we also added configurable options for the terminal sounds and the cursor style. The first option determines if the terminal uses a bell sound or not. The second one allows selecting one of three cursor styles.

![Preferences pane for changing the terminal style](/images/spyder-terminal/preferences.png)

![Cursor options for Spyder-terminal](/images/spyder-terminal/cursor-style.png)

## Shortcut configuration

Lastly, the shortcuts on the terminal are configurable within the keyboard shortcuts in Spyder 4. In the previous version of the terminal, these shortcuts were hardcoded, but now the user is able to determine which combination of keys she wants to use to copy, paste and open a new terminal.

![Configurable shortcuts for the Terminal inside Spyder 4](/images/spyder-terminal/shortcuts.png)

![Open a new terminal with the configured shortcut](/images/spyder-terminal/new-term.gif)

The new Spyder-terminal version will enhance the user experience while using Spyder 4. We can't wait for users to install and experiment with the new features available. All the presented work was funded by a NumFOCUS small development grant and Quansight. Please don't forget to keep up with our updates and happy coding!
