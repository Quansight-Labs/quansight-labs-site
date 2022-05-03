<!--
.. title: The evolution of SciPy CLI
.. slug: the-evolution-of-scipy-cli
.. date: 2022-05-03 8:00:00 UTC+05:30
.. author: Sayantika Banik
.. tags: CLI, SciPy, doit, typer, rich-click
.. category:
.. link:
.. description:
.. type: text
.. previewimage:
-->

#### 🤔 What is a command-line interface (CLI)?

Imagine a situation where there is a massive system with various tools and functionality. Every functionality requires a special command or an input from the user, CLI is designed to tackle such situations. Like a catalog it lists all the options present, helping the user to navigate. A CLI can be a simple list or a complex GUI based application, for example, shown below.

<p align="center">
  <img src="https://user-images.githubusercontent.com/17350312/166225781-3f2cfd4d-49a5-4e30-a3bf-841552d7338c.jpg" />
</p>

Now that we understand what a `CLI` is, how about we dive into the world of `SciPy`?

#### 🤓 SciPy CLI journey

An open-source project undergoes multiple iterations, and each iteration adds layers of tools and functionalities to incorporate. Right from the initial build, test, benchmarking, release notes, and beyond. Contribution guidelines start spanning across multiple pages, exponentially increasing efforts to maintain. 

The two homegrown CLI for SciPy are `runtests.py` and `dev.py` (for meson) built using python tooling `argparse`. 
Both of these toolings have multiple conditional blocks to achieve the desired outcome. Not only it is difficult to maintain, overall readability decreases drastically. The documentation runs into an infinite loop of updates, requiring additional efforts from maintainers. Another issue that remains is the lack of command bundling. A combined unit of commands linking to a single objective helps reduce confusion, very helpful for new contributors (like me :D).

Hence the idea of a developer command-line interface (CLI) was born. Easing the development experience with an intuitive and informative CLI. Removing dependency on legacy tooling like `paver` also added great value to the overall experience. Additional details could be found under [issue-#15489](https://github.com/scipy/scipy/issues/15489)

#### Planning and objective
Like any development activity, the goal was to experiment with tools available `doit` and `typer` were the first ones we picked. The 02 components of our interests were a `task runner`, and a ` command-line interface tool`.  

As a starting point, I began experimenting with existing `dev.py` options, wrapped around multiple composite `doit` and `typer` tasks. Both the [doit POC](https://github.com/sayantikabanik/scipy/blob/cli_poc/dodo.py) and [typer POC](https://github.com/sayantikabanik/scipy/blob/cli_poc/cli.py) were built with similar principles. 

As I progressed with the development of POCs using both tools, I experienced certain shortcomings. A Better way to integrate an external library for exposing a CLI was the missing piece. **Eduardo** author of doit developed an architecture combining the core elements of `doit` along with `click`. The journey in detail is captured under [issue-#133](https://github.com/rgommers/scipy/issues/133).

#### 💁🏽‍♀️  More about the architecture and core components

Combining these tools wasn’t a straightforward journey after multiple iterations we were able to achieve a stable state. Doit underwent updates to incorporate added functionality, helping the pieces come together live. Below are the core components for the `doit-click` based task definition.

1. ✍️ Click based approach to accept arguments/options/parameters
2. ☑️ Base class to define doit task and/or click command
3. 🏃 Method to execute a task `run()`
4. 🌟 Additional utilities like `task dependency` and metadata definition using class attribute `TASK_META`

##### Class based Click command definition
```python
@cli.cls_cmd('test')
class Test():
    """Run tests"""
    @classmethod
    def run(cls):
        print('Running tests...')
```
- Command may make use of a Click.Group context defining a `ctx` class attribute
- Command options are also defined as class attributes
```python
@cli.cls_cmd('test')
class Test():
    """Run tests"""
    ctx = CONTEXT
    verbose = Option(
        ['--verbose', '-v'], default=False, is_flag=True, help="verbosity")
    @classmethod
    def run(cls, **kwargs): # kwargs contains options from class and CONTEXT
        print('Running tests...')
```

#### 🎨 `rich-click` addition 

To incorporate the look and feel, I designed a layer on top of the existing CLI architecture with the help of `rich-click`.
It offers a variety of style options, markdown setting and flexibility to group tasks and options. Together it adds that perfect richness to the CLI command pallet.

```python
rich_click.STYLE_ERRORS_SUGGESTION = "yellow italic"
rich_click.SHOW_ARGUMENTS = True
rich_click.GROUP_ARGUMENTS_OPTIONS = False
rich_click.SHOW_METAVARS_COLUMN = True
rich_click.USE_MARKDOWN = True
rich_click.OPTION_GROUPS = {
    "do.py": [
        {
            "name": "Options",
            "options": [
                "--help", "--build-dir", "--no-build", "--install-prefix"],
        },
    ],

    "do.py test": [
        {
            "name": "Options",
            "options": ["--help", "--verbose", "--parallel", "--coverage"],
        },
        {
            "name": "Options: test selection",
            "options": ["--submodule", "--tests", "--mode"],
        },
    ],
}
```

#### 🎥 Devloper CLI in action

[![asciicast](https://asciinema.org/a/U9l9VvklvEjXdEi1xYS4A7u5M.svg)](https://asciinema.org/a/U9l9VvklvEjXdEi1xYS4A7u5M)

#### Current list of implemented tasks
* `Build & testing tasks`
     - build (build & install package on path)
     - test (Run tests along with options to run tests for a given submodule)
* `Static checker tasks`
     - pep8 ( Perform pep8 check with flake8)
     - mypy ( Run mypy on the codebase)
* `Environments`
     - shell (Start Unix shell with PYTHONPATH set)
     - python (Start a Python shell with PYTHONPATH set)
     - ipython (Start IPython shell with PYTHONPATH set )
* `Documentation tasks`
     - doc (Build documentation)
     - refguide-check  (Run refguide check)
 
* `Release tasks`
    -  notes   (Release notes and log generation)               
    -  authors  (Task to generate list the authors who contributed within a given revision interval)
* `Benchmarking tasks`
    - bench & bench compare

#### 👏🏽 Great Collaboration and teamwork

From an idea to developing a successful POC, the journey was a great learning opportunity for me. Planning, coordination, teamwork and clear communication played a very important role. Huge thanks to **Ralf Gommers** and **Eduardo Naufel Schettino** for the amazing collaboration and support. 

As a newcomer to the `SciPy codebase`, it was a steep learning curve. I asked a ton of questions, at times drifted to the ocean searching for answers. Learning something completely new be overwhelming, different emotions brush past. Thanks to Ralf and **Pamphile Roy** for addressing my questions. The learnings and achievements will stay with me for a long-long time.    

#### 😇 The possibilities next steps

The experimental CLI is available under `scipy/do.py` for the wider community to test and provide us with valuable feedback.
Some of the handy commands to quickly try out the CLI -
- Enabling the GUI: `python do.py`
- Listing the args/options for a task: `python do.py <task_name> --help`

**Outcomes**

1. 📜 Self documentation and hierarchical help option
2. 🧭 Easy to navigate and intuitive interface 
3. ⏩ Clear and concise examples to get started quickly
4. ⏱ Reduction in the time spent navigating documentation

With a great start comes possibilities. In the coming weeks, the CLI will become more mature and stable. After we receive wider usage and acceptance from the community, support for `dev.py` and `runtests.py` will be paused and `do.py` will be renamed to `dev.py`. The user documentation for the CLI components and usage will be made available for clear and concise understanding. 

We are excited to collaborate with other projects looking forward to adapting a similar developer command-line interface 😃

