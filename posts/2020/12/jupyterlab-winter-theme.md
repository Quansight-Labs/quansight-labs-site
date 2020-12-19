<!--
.. title: JupyterLab Winter Theme
.. slug: jupyterlab-winter-theme
.. date: 2020-12-01 09:00:00 UTC-00:00
.. author: Matthias Bussonnier, Isabela Presedo Floyd, Eric Charles, Eric Kelly, Tony Fast
.. tags: Labs, Jupyter, Theme, JupyterLab, JupyterTutorials
.. category:
.. link:
.. description:
.. type: text
-->

JupyterLab 3.0 is about to be release/ has been released, it provides many 
improvements to the extension system and, in particular, theming. 

While theming is often disregarded as purely cosmetic endeavour it can greatly
improve software. Theming can be great help for accessibility, and even the
Jupyter team pays attention to making the default appearance accessibility aware by using
sufficient contrast.  For users with a high visual acuity you may also choose 
to increase the information density.

Theming can also be a great way to improve communication by increasing or
decreasing emphasis of the user interface, which can be of use for teaching, or
presentation. Theming may also help with security, for example, by having a clear
distinction between staging and production.

Finally Theming can be a great way to express oneself, for example, by using
a branded version of software that fits well into a context, or expressing one's artistic
preferences or opinions. 

In the following blog post(s), we will show you step-by-step how you can
develop a custom theme for JupyterLab, distribute it, and take the example of the
JupyterLab-winter-2020 theme we release today to celebrate the end of 2020.

<!-- TEASER_END -->

# JupyterLab and Themes

JupyterLab customisation can be done via what are called Extensions.  All
behaviors and user interface elements of JupyterLab can be changed by providing
extensions; this is true for elements that are added to JupyterLab, but also for
the core components. A Theme is one of those extensions.  The default light and dark
themes are always good examples to look at if you want to understand how to build
a theme. 

Generally all information about how extensions work in JupyterLab is applicable
to a theme, though there are a number of optional steps and behaviors that are not
necessary for themes. A lot of boilerplate can also be extracted, which
makes creating most themes simpler that full-fledged extensions.

Let's first see what we are trying to accomplish in a screenshot of the "winter 2020" theme.
You will have the option to choose this theme in the dropdown menu of JupyterLab:

[ ![Screenshot of JupyterLab Winter Theme](/images/jupyterlab-theme-winter.png) ](/images/jupyterlab-theme-winter.png)

To do so we'll need to:

- Install JupyterLab (dev edition)
- Create a new theme extension
- Install this extension
- Switch to our new theme
- Progressively change the appearance of our JupyterLab components until we get
  the desired outcome

Optionally, once you are happy with the result, or would like to get feedback from the
community, you can publish the theme so that people can ~~complain~~ suggest improvements
and contribute. 

# Installing JupyterLab

To get started you do [NOT?] need a development version of JupyterLab.  This can
be achieved with:

```bash
$ conda install jupyterlab
``` 
[The bullet list above states "dev edition".  Is this the correct install command?]

While we are at it we will need to install nodejs, as nodejs is _not_ a python
package you will need to use conda or another package manager. 

```bash
$ conda install nodejs
```

# Creating a theme extension

Now is the hard part: you have an idea, you need a name. Naming is one of the
two hardest things in data science [I like this joke, but do you mean 'development'?  I don't consider theming to be data science] 
along with caching-results and off-by-one error, but it is
critical to adoption and discoverability. 

Now that you have your perfect name, create your project.  We suggest using cookiecutter:

```bash
$ pip install cookiecutter

$ cookiecutter https://github.com/jupyterlab/theme-cookiecutter
author_name []: Quansight Labs
author_email []: contact@quansight.com
extension_name [mytheme]: jupyterlab-theme-winter
org_name [myorg]: quansight
homepage []:
project_short_description [A JupyterLab theme extension.]: A winter theme for jupyterlab
```

This has created the jupyterlab-winter-2020 directory [do you mean 'jupyterlab-theme-winter' directory?].  We can go to the directory and
immediately turn it into a git repository.

```bash
$ cd jupyterlab-winter-2020/
$ git init
$ git add .
$ git commit -am 'initial commit'
```

# Building and installing our extensions

The readme of our new theme already contains some information on how to
install this theme:

```bash
npm install
jupyter labextension link .
```

You only need to do this one [once?]. 

In a separate terminal you can now open JupyterLab and will see the theme available from the menu. 

You can switch themes; but as you will see; the current theme is identical to
the light-theme. Now is time to modify some values. 

## Design considerations 
In the words of Jurassic Park’s Dr. Ian Malcolm, “Your scientists were so preoccupied with whether they could, 
they didn't stop to think if they should.” And now that you can modify JupyterLab’s theme to your heart’s content, 
here is some design advice to help keep you from accidentally creating a theme that visually destroys your 
workspace like a rampaging tyrannosaurus rex.

### JupyterLab Design System
When making a theme, it’s likely you’ll want to change things that already exist in JupyterLab. Much of the UI relies 
on relevant CSS variables with naming conventions (`--jp-ui-font-color3 ` or `--jp-elevation-z0`) to help you find 
what you need. I think of the system like this:`--jp-region-contenttype-unit1`

- The `--jp` prefix is a constant. 
- The middle holds various details like what type of UI element it is for, if it is standard (no tag) or if 
it has a specific use. 
- `region` is for variables that are only be used in a certain area of the UI .
- The content type is something like `font` or `border`. It describes the variable based on its use. 
- The `unit` is the smallest unit of the variable like a color, shadow, or spacing. It is labeled by a number when 
there is more than one of that unit; `0`s are almost never used, and `1`s are some of the most frequently used. 
- Whenever a variable name does not have one of these sections, that means it doesn’t have specific rules about 
its use in that area.

Common labels you might want to know:
- `layout` is used for large areas of the interface, especially backgrounds. 
- `inverse`  indicates the opposite color scale of the rest of the UI. For example in light mode, inverse `0` and `1` 
are dark instead of light.
- `elevation` and `z` is for shadows. While these might not be the main things you want to change, their unfamiliar 
name might make them harder to find.
- `font` is for variables tied to text. These have forms for color, size, and spacing of text. There are also variables 
specific to different types of text and display modes, so you could have a theme that looks like the standard light 
theme until you enter Presentation mode.

### Color
Less is more. Choosing a color palette of three or fewer hues can be easier to manage and make the whole interface 
more cohesive since those colors will likely be repeated across the UI. Try it out; it might be surprising how just 
changing a few color variables can create a very different JupyterLab.

A color's value—or how light or dark it is—also determines contrast. Contrast is key to legibility and creating an 
experience that includes low-vision users. [WCAG color contrast guidelines](https://developer.mozilla.org/en-US/docs/Web/Accessibility/Understanding_WCAG/Perceivable/Color_contrast) 
apply to text and graphic interactive 
elements. There are many tools available, including [downloadable contrast checkers](https://www.paciellogroup.com/color-contrast-checker/) 
and [web app versions](https://userway.org/contrast/000000/ffffff).

### Text
JupyterLab is full of text, so this can be a place for major changes with very little code. You can easily change font, 
color, spacing, and size. It's a good idea not have text below 10pt in size, or smaller than the default 
[`--jp-ui-font-size0`](https://github.com/jupyterlab/jupyterlab/blob/083c65d92686d23b813f0242fca5be3d8b6fae37/packages/theme-light-extension/style/variables.css#L107) 
(and it's an accessibility recommendation).

### Icons
JupyterLab's icons live in the [packages directory](https://github.com/jupyterlab/jupyterlab/tree/083c65d92686d23b813f0242fca5be3d8b6fae37/packages/theme-light-extension/style/icons) 
and are part of or based on [Material Icons](https://material.io/resources/icons/?search=clos&icon=warning&style=round). 
If you want to change or add icons and keep them matching, finding one from this system will fit best. The [Material Design system](https://material.io/design/iconography/system-icons.html) 
also points out some of their icon design principles which are good to follow if you need to make custom icons that 
match with the rest. Use SVGs, not PNGs, and remember to give it a [tooltip](https://en.wikipedia.org/wiki/Tooltip). 
Most of all, make sure to give it an ARIA label (like [this recommendation](https://gomakethings.com/icon-accessibility-and-aria-label/)).

# Modifying some values

After each modification you will need to build the extension with 

```bash
npm run build; jupyter lab build
```

No need to stop and restart JupyterLab server; simply refresh the page.
Now we are going to modify some values in the file `varaibles.css` in our
project. This file controls many of the colors of Jupyterlab, and is a nice place
to start to change the overall color scheme before doing more detailed
customisation.

We'll try to update the current theme from orange/blue to more blue-ish tones, 
which tend to remind me of the holiday
season.  Afterward, in the `diff`, see how we changed some of the colors:

```diff
diff --git a/style/variables.css b/style/variables.css
index f8c738f..9f39f14 100644
--- a/style/variables.css
+++ b/style/variables.css
@@ -87,9 +87,9 @@ all of MD as it is not optimized for dense, information rich UIs.
    */

   --jp-border-width: 1px;
-  --jp-border-color0: var(--md-grey-400);
-  --jp-border-color1: var(--md-grey-400);
-  --jp-border-color2: var(--md-grey-300);
+  --jp-border-color0: #168EA8;
+  --jp-border-color1: #168EA8;
+  --jp-border-color2: #93D3E1;
   --jp-border-color3: var(--md-grey-200);
   --jp-border-radius: 2px;

@@ -118,10 +118,10 @@ all of MD as it is not optimized for dense, information rich UIs.
```

I'd like the "running notebook" dot in the filesystem browser to be a
snowman instead of a blue dot. Using the browser inspector, I can look a the CSS
doing this and override it in my theme:

[Is the dot in the second line on the right side of this code block intentional?]
```diff
@@ -368,0 +369,26 @@                                                                 .
+
+.jp-DirListing-item.jp-mod-running .jp-DirListing-itemIcon:before {
+    content: '\2603'; /* snowman */
+    font-size: 10px;
+    position: absolute;
+    left: -8px;
+}
```

We can also add backgrounds to many of the panels.  By adding a file `snowflakepatterns.svg` to our style directory,
we can now refer to it from our file and add the following CSS to include snow flakes in the background of 
our directory listing.

```css
/* DirListing */

body[data-jp-theme-name="JupyterLab Winter"] .jp-DirListing-content {
  background-image: url('./snowflakepattern.svg');
 }
```

# Awesome ! 

Here is the final result, JupyterLab-winter-2020 theme provided by QuanSight.  Feel
free to modify it, and please suggest some themes you might like and share
in the comments. For example we'd love to see a "summer 2020 theme" for our southern hemisphere friends. 
We will dive into how to distribute your themes and make them high quality in a later blog post.

[![Screenshot of JupyterLab Winter Theme](/images/jupyterlab-theme-winter.png)](https://github.com/Quansight-Labs/jupyterlab-theme-winter)

And as a bonus, a Christmas theme with more green-ish color and some lights shining [Are they really shining/sparkling or are they from a static image?] 
at the bottom of your notebooks!

[![Screenshot of JupyterLab Christmas Theme](/images/jupyterlab-theme-christmas.png)](https://github.com/Quansight-Labs/jupyterlab-theme-christmas)
---
*This is part of a series of Jupyter tutorials. Find more [tutorials here](https://labs.quansight.org/categories/JupyterTutorials).*


