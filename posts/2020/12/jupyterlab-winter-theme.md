<!--
.. title: JupyterLab Winter Theme
.. slug: jupyterlab-winder-theme
.. date: 2020-12-01 09:00:00 UTC-00:00
.. author: Matthias Bussonnier, Isabela Presedo Floyd, Eric Charles
.. tags: Labs, Jupyter, Theme, JupyterLab
.. category:
.. link:
.. description:
.. type: text
-->

JupyterLab 3.0 is about to be release/ has been released, it provides a lo of improvement to the extension system  and
in particular theming. 

While theming is often disregarded as purely cosmetic endeavour it can greatly
improve a software. Theming can be of great help for accessibility, and even the
jupyter team pay attention to make the default appearance accessibility aware
with sufficient contrast, theming may help in this regard. For users with a high
visual acuity you may also decide to increase the informations density.

Theming can also be a great way to improve communication by increasing or
decreasing emphasis of user interface, which can be of use for teaching, or
presentation. Theming may also help with security, bu for example having a clear
distinction between staging and production.

Finally Theming can be a great way to express oneself, by for example using
branded version of software that fit well in a context, or express ones artistic
preferences or opinions. 

In the following blog post(s), we will show you a step by step on how you can
develop a custom theme for JupyterLab, distribute it; and take the example of the
JupyterLab-winter-2020 theme we release today to celebrate the end of 2020.

<!-- TEASER_END -->

# JupyterLab and Themes

JupyterLab customisation can be done via what is called Extensions, all
behaviors and user interfaces elements of JupyterLab can be changed by providing
extensions; this is true for elements that are added to JupyterLab, but also for
the core component. A Theme is one of those extensions, and the light and dark
theme are always good example to look at if you want to understand how to build
a theme. 

Generally all informations about how extensions work in JupyterLab is applicable
to a themes, though there is a number of optional steps and behavior that is not
necessary for themes. A lot ob boilerplate can also be abstracted over which
make created most themes simpler that full-fledge extensions.

Let's first see what we are trying to accomplish in a screenshot, have the option to with to a "winter2020" theme in
the dropdown menu of JupyterLab:

DO Screenshot

To do so we'll need to:
 - install JupyterLab (dev editions )
 - Create a new them extensions
 - install this extensions
 - switch to our new theme
 - Progressively change the appearance of our jupyterLab components until the desired outcome. 


Optionally once you are happy with the result, or like to get feedback from the
community, publish the theme so that people can ~~complain~~ suggest improvement
and contribute. 

# installing jupyter lab

To get started you do [NOT?] need a developement version of JupyterLab this can
be achieved with:



# creating a theme extensions

Now is the hard part you have an idea, you need a name. Naming is one of the
two hard-things in data-science along with caching-results and off-by-one error, but is
critical to adoption and discoverability. We suggest starting with cookie-cutter

Cookie cutter ....


INSERT PSEUDO SNIPPET of interaction


# building and installing our extensions

....


# modifying some values



# Awesome ! 

Here is the final result, JupyterLab-winter-2020 provided by QuanSight, feel
free to modify it, and please suggest some themes you might like and share your
in the comments. For example we'd love to see a "summer 2020 theme" for our southern hemisphere friends. 
We will dive into how to distribute your themes and make it high quality in a later blog post.







