<!--
.. title: JupyterLab Collaboration
.. slug: jupyterlab-collaboration
.. date: 2020-04-01 07:25:55 UTC-05:00
.. author: Saul Shanabrook
.. tags: Labs, JupyterLab
.. category: 
.. link: 
.. description: 
.. type: text
-->


## Rought stream of thoughts:

Over the past couple of months, Quansight has gotten funding to contribute to JupyterLab. This week, I am helping to make
a minor release of JupyterLab that enables the extension manager by default, funded by Kite, and a number of fixes needed
by DE Shaw:

<picture of extension manager>

These include by de shaw:

* performance testing
* right click context menu
* list all other DE Shaw sponosored work JLab
* jupyterlab git many things!
* juptyerlab git adding contributors to readme

Kite:

* extension manager by default
* icons
* blacklist whitelist


While these features are useful, the interesting part here I think is more around the process than the end product.
But I do want to to thank everyone who has been a part of these changes. TODO: Link to all their work

* Athan jlab git
* Max jlab git
* Eric blacklist whitelist
* Mars UI for blacklist whitelist
* Time UI for blacklist whitelist
* Ralf for Managing kite
* Dharhas for managing de shaw
* Anthony for managing de shaw
* Marc at DE Shaw for helping us solve these issues
* Team at kite for being game to work on all these jupyterlab things and invest there
* The rest of the JupyterLab team for their reviews, maintaince, and continued investment in the project and community

It's quite amazing how many different stakeholders and people are involved in moving something from an idea to showing up
in the end product you download.

### Questions

What are we really doing though in this process? One of the open questions I have about this process and community is what
are we building? What values are we moving from? Why are we putting in effort on the things we do?

#### Money

The easy out is money as an organizing principle. You could rely on some kind of reductionist rational-capitilist analysis
and say "Well it's a mutally beneficial relationship! Everyone benefits (monetarily)!" This is one of the angles we sell
to clients, saying "hey this isn't charity work you are sponsoring, it's in your best fiduciary interest to support these
projects by funding us to work on them!" What's the rationale here?

What are the reasons kite can say that this work is good for their bottom line?  Well they can say that this work is
neccesary to increase outreach for their completer extension they are developing. Also that by investing in JupyterLab
as a whole, they can increase the reach of their extension as more users come on board.

Similar for DE Shaw. They are using JupyterLab internally and getting things fixed upstream is cheaper for them
then maintaing a parallel fork, because of all the other work being done.

What's interesting is that open source takes instutitions that have no common financial interests, and binds
them together through their shared use of some software. Quansight itself has a fiduciary interest in JupyterLab
as well, since if it tanked then we would be left with no one willing us to pay for work on it.


This financial lense is deffinately useful, in that since we live in a mostly capitlist economy, it's an easy on ramp
to understanding what open source can mean for you. You get bound up in common interest with other folks, and it incentivizes
all of you to work together to raise the boat for everyone.

#### People

Open source is a messy business. It's disorganized, mostly unstructured, often opaque, provincial, and petty. But there is a
spark in it that provides some modicum of intention and desire. I am continually thankful for the people I get to work with,
accross the world, accross industry, accross occupation.

What I see in it is a space to collaborate, but almost in some combination of modernist vision of planning combined with a
postmodern continual destruction and rebirth of the contours of what we are building. 

For example, take [this recent comment](https://github.com/jupyterlab/jupyterlab/issues/7574#issuecomment-606091453) by an author
of a UI framework library on a JupyterLab issue about our components. Regardless of the technical discussion, you can sense
this yearning for joining, for unification. Although again, we could make self interested financial arguments here 
(if you are the author of a framework, the more user and publicity it gets, the more power and clout you have that
you could leverage into paid work), we can also speak to the human desire for connection and collaboration. It's fun
to work as a group towards a shared goal! And there is safety in a group. Money is transitory but when times are tough,
human connections are what you can depend on.

So it's some sort of organizational problem. How can we *enable* people to be able to collaborate and work together? The
premise is that's what we would like to do, all things being equal, and open source is simply a collection of built up
structures and processes to facilitate that.

#### Our Contracts

OK back to our contracts. I think I should outline a few goals we had in our collaborations, process wise:

1. Keep as much as possible public. Open public issues, have discussions in public. 
2. Get explicit buy in from community stakeholders as early as possible and continue to get buy in as we progress.
   This is why it helps to have folks who are already active in projects. Unfortunately, most of the decision making
   processes are informal and person to person, so it helps to know who to talk to and how to navigate the process.

You can see with that last point, there is an issue, as projects get to a certain size, with informal relationships governing
how things move forward. It's where ideas like governance, democracy, or the state come into play. We are good at one-to-one
relationships, but as soon as you are trying to coordinate the resources and intentions of a larger group, you need some
structure to attempt to ensure fairness.

Because there are a lot of ways this process can go wrong. We have to be able to trust each other, that we are working
not only for the interests of who is paying our paychecks, but also for the larger project.

So what are some good ways to do this at a project level? What's our version of lobbying disclosure? It's even more than lobbying
because open source projects don't have taxes. So unless you are volunteering your time, to get paid to work on them you
usually have to employed by someone who has a vested interest in the project. This would be like if our senators were
literally on the payroll of the banks, because we couldn't figure out a way for the public to pay for them.

Talk about moral hazard! The advantage is that we aren't distributing resources in the same was as the federal government.
So what are we balancing, if not tax brackets?

1. Distribution access. For example, we didn't want to ship JupyterLab with
   Kite support built in. However, we did want to provide them with a way to ship easily to customers who user JupyterLab.
2. Marketing eyeballs. DE Shaw wanted to somehow broadcast that they are supporting the JupyterLab git work. So I worked on
   a way to show who was sponsoring work on that plugin in the README. It isn't perfect though! And we have no hard lines
   in terms of what lets you put your logo on their. 

I think at least what we can do is figure out ways to be transparent about these things, like with campaign contributions.
So if I am working on a feature in JupyterLab that benefits a particular party, I should say that directly. It's not
that this would be disqualifying at all, but it helps us all understand *why* people are suggesting certain things. Which
is helpful, so we can all make sure we are on the same page.

Because with a project like JupyterLab, the biggest task is articulating movement in a certain direction. Building enough
shared understanding to say "Let's move in this direction on this task" and then getting the funding and time to actually
achieve that.

And I think the biggest challenge we have as a project is making that process more open. If I want to contribute to JupyterLab
I should be able to see the large things that need to be done to move the project forward. Also, if I am a funder, I should
know what these are as well.
