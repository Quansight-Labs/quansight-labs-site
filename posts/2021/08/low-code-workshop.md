<!--
.. title: Low-code contributions through github
.. slug: low-code-contributions-through-github
.. date: 2021-08-10 18:00:00 UTC-00:00
.. author: Isabela Presedo-Floyd, Mars Lee, Melissa Weber Mendonça, Tony Fast
.. tags: Jupyter, NumPy, Accessibility
.. category:
.. link:
.. description:
.. type: text
-->


# Low-code contributions through github

Healthy, inclusive communities are critical to impactful open source projects. 
A challenge for established projects is that the history and implicit technical debt increase the barrier to contribute to significant portions of code base.
The literacy of large code bases happens over time through incremental contributions, and we'll discuss a format that can begin this journey.

At quansight labs, we are motivated to provide opportunities for new contributor's to experience open source community work regardless of their software literacy. 
Community workshops are a common format for onboarding, but sometimes the outcome can be less than satisfactory for participants and organizers. 
In these workshops, there are implicit challenges that need to be overcome to contribute to projects revision history like `git` or setting up development environments. 

Our goal with the following low-code workshop is to offer a way for folks to join a projects contributors list without the technical overhead. 
To acheive this we'll discuss a format that relies solely on the github web interface.

## Case study - collaboratively improving the accessibility of images in documentation

Our successful experiments are based on having new and seasoned contributors work together to add alternative text representations to images in project documentation. 
Each event lasts an hour with the following format:

1. pre-meeting preparation with a project contributor and meeting facilitator
2. a crash course in the specific topic - eg alt text for images
3. an introduction to a collaborative pull request created by a project contributor
4. group working session to suggest changes to specific files assigned in the pull request
5. a short review of the submissions by the core contributor
6. final review by the core contributor to submit a final pull request

Accessibility is a focus for many members of quansight labs team so we've chosen this prompt to begin testing these workshops. 
We'd love to hear about other prompts that may be good for low-code contributions.

### Pre-meeting preparation

Each event relies on a single pull request managed by a project contributor. 
We recommend using a fork to reduce noise to other contributors because we gonna be loud for an hour. 

Before the event the contributor makes a pull request identifying files that need changes related to the prompt, some projects may have rendered documentation that would also help guide the contributions. 
The attendees will use these files to recommend changes to the code landing their aliases in the github history. 
The facilitator will add an agenda for the event with learning materials that will prepare folks for the event.

### The crash course

The crash course is a short lightning talk style introduction to support the prompt folks will address during the hour. 
This short talk is important to prepare folks for the topic, to support contributors we want to remove the technical roadblocks that distract them from the community.

### Introduction to the pull request 

To kick off the work, the core developer walks us through the pull request they've prepared and introduce to the different files. 
For reinforcement, the facilitator will share their screen to demonstrate the process of recommending changes to files in a pull request.

### Group work

Together the new and old contributors work together to make changes to relevant files to improve their quality. 
These changes are made using github's suggest changes feature that allows authors to make single line changes to code; a workflow perfect for alt text.

### group review

Over 40 minutes several contributors can make quite a few commits. 
The project contributor shares their screen to review the suggestions made over the course of the event. 
This portion becomes a critique to review the different contributions made.

### Bringing everything home

All of the work we talked about happened on a contributors fork. 
They now have a pull request will a gaggle of contributors. 
Their last job is to submit the pull request to the mainline project and see the work accepted into the code base.

## Success stories

Everyone loves an underdog story. 
What follows are there triumphs of some open source allies who thought they could run an hour sprint that allowed multiple folks to contribute to an open source project. 
Believe it or not, we weren't lying to ourselves and others. Below we highlight our successes with running low-code sprints in `jupyter` and `numpy`.

### Jupyter accessibility group

There is a small group of the jupyter community focused on the improving the accessibility of jupyterlab and orbitting projects. 
We meet every other work to add small patches and fixes. currently, we're in the process of organizing workshops to advocate for accessibility and improve the quality of the entire jupyter experience for disabled scientists.

On an off week, between our normal syncs, we tested a low-code format for folks to participate in the jupyter project. 
During an hour, four people included in the project by suggesting changes to alt text for images in the `jupyterlab` documentation (https://github.com/isabela-pf/jupyterlab/pull/1), 
resulting in a collaborative commit to mainline with the help of @krassowski and @isabela-pf as champions for the shared work.(https://github.com/jupyterlab/jupyterlab/pull/10670)

We consider this event a success because we were able to remove `git` as a technical barrier to entry and support changes from multiple authors.


### [NumPy documentation](https://numpy.org/doc/stable/) new comers meeting

Our fledgling experience in one event made us *sort of* confident this could work for other projects. 
So we contacted our NumPy accessibility allies @melissawm and @marsbarlee to test this
hypothesis at the NumPy new comer's meeting, which [happens every other
Thursday](http://numpy-discussion.10968.n7.nabble.com/Newcomer-s-Hour-td49226.html).

During the meeting, @marsbarlee provided a valuable [slideshow on how to write alt-text for
scientific diagrams](https://docs.google.com/presentation/d/150vhbpGrtAc3ALhrS1a07lhEKCgevAY3ITh-4eCndDk/edit?usp=sharing). 
This involves looking at examples and looking at the image context.

The progress from the `numpy` new comer's meeting can be seen in this issue https://github.com/melissawm/numpy/pull/27 .

A highlight, to us, is that we provided opportunities for both long time `numpy` fans and high school students a chance to see themselves in history of such a foundational tool like `numpy`. 
Moreover, attendees were still adding alt text contributions after the event concluded.


## Conclusion

Using Github's suggested change system is a way to support low-code, single-line contributions to different open source code bases. 
The event's collaborative hands-on format offers time for the community to interact in a meaningful way and see the fruits of their labor immediately.

Please reach out to us if you or your project are interested in running event like this. 
We'd love to hear about how this process can work for your events and project's perspective.
