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

To get started you do [NOT?] need a development version of JupyterLab this can
be achieved with:

$ conda install jupyterlab

While we are at it we eill need to install nodejs, as nodejs is _not_ a python
package you will need to use conda or another package manager. 

$ conda install nodejs

# creating a theme extensions

Now is the hard part you have an idea, you need a name. Naming is one of the
two hard-things in data-science along with caching-results and off-by-one error, but is
critical to adoption and discoverability. We suggest starting with cookie-cutter

$ pip install cookie cutter

$ cookiecutter https://github.com/jupyterlab/theme-cookiecutter
author_name []: QUansight Labs
author_email []: contact@quansight.com
extension_name [mytheme]: jupyterlab-winter-2020
org_name [myorg]: quansight
homepage []:
project_short_description [A JupyterLab theme extension.]: A winter theme for jupyterlab

This as created the jupyterlab-winter-2020 directory in which we can move, and
will immediately turn into a git repository

$ cd jupyterlab-winter-2020/
$ git init
$ git add .
$ git commit -am 'initial commit'





# building and installing our extensions

THe readme of our new theme does already containsome information on how to
install this theme:

```bash
npm install
jupyter labextension link .
```

You only need to do this one. 

In a separate terminal you can now open jupyterlab, and will see the theme available from the menu. 

You can switch themes; but as you will see; the current theme is identical to
the light-theme. Now is time to modify some values. 


# modifying some values

After each modification you will need to build the extension with 

```bash
npm run build; jupyter lab build
```

No need to stop and restart JupyterLab server; simply refresh the page.
Now we are going to modify some values in the file `varaibles.css` in our
project. This file control many of the color of Jupyterlab, and is a nice place
to start to change the overall color scheme before doing more detailed
customisation.

We'll try to update the current theme from orange/blue to a more red/green which
tend to remind me of the holiday season, in the diff afer see how I change the
brands colors from blue to red:

```diff
--- a/style/variables.css
+++ b/style/variables.css
@@ -168 +168 @@                                                                  
-  --jp-content-link-color: var(--md-blue-700);
+  --jp-content-link-color: var(--md-red-700);
@@ -220,4 +220,4 @@                                                                  
-  --jp-brand-color0: var(--md-blue-700);
-  --jp-brand-color1: var(--md-blue-500);
-  --jp-brand-color2: var(--md-blue-300);
-  --jp-brand-color3: var(--md-blue-100);
+  --jp-brand-color0: var(--md-red-700);
+  --jp-brand-color1: var(--md-red-500);
+  --jp-brand-color2: var(--md-red-300);
+  --jp-brand-color3: var(--md-red-100);
```

This will affect most of the links ad many icons already. The input prompt in a
notebook are still blue. Using my browser inspector I can find that this is
controlled by the following which I change to red using one of the above
variable.

```
@@ -274 +274 @@                                                                 .
-  --jp-cell-inprompt-font-color: #307fc1;
+  --jp-cell-inprompt-font-color: var(--jp-brand-color1);
```

I'd like the "running notebook" dot in the filesystem browser to now be a
snowman instead of a blue dot. Again using the inspector I can look a the css
doing this and override it in my theme:


```
@@ -368,0 +369,26 @@                                                                 .
+
+.jp-DirListing-item.jp-mod-running .jp-DirListing-itemIcon:before {
+    content: '\2603'; /* snowman */
+    font-size: 10px;
+    position: absolute;
+    left: -8px;
+}
```

I also want the "notebook" and "json" file icons to be green, and the "shutdown
kernel" button to be red:

```
+g.jp-icon-warn0.jp-icon-selectable, g.jp-icon-warn1.jp-icon-selectable {
+    fill: var(--md-green-700);
+
+}
+
+button.jp-RunningSessions-itemShutdown.jp-mod-styled {
+    fill: var(--md-red-700);
+
+}
```

Let me also put images in the bottom left corner of many panels, I use a
transparent white layer (FFFC gradient) on top of an image I do not forget to
put in the `style/` directory, I can reference it from my css file:

RIGHT NOW QS LOGO, BUT MAYBE USE A TREE, REINDEER...

```
+.jp-Notebook, .jp-Launcher-body, .jp-DirListing-content {
+    background-image: linear-gradient(#FFFC,#FFFC),url(./logo.jpg);
+    background-repeat: no-repeat;
+    background-size: 120px 120px;
+    background-position: bottom left;
+}
```




# Awesome ! 

Here is the final result, JupyterLab-winter-2020 provided by QuanSight, feel
free to modify it, and please suggest some themes you might like and share your
in the comments. For example we'd love to see a "summer 2020 theme" for our southern hemisphere friends. 
We will dive into how to distribute your themes and make it high quality in a later blog post.







