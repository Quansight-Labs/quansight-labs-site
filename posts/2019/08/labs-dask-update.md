<!--
.. title: Labs Dask Update
.. slug: labs-dask-update
.. date: 2019-08-19
.. author: James Bourbeau
.. tags: Labs, Dask 
.. category: 
.. link: 
.. description: 
.. type: text
-->

This post provides an update on some recent [Dask](https://dask.org/)-related activities at Quansight.

Through a community work order (CWO) for Dask development, the Quansight Labs team has been able to dedicate developer hours towards bug fixes and feature requests for Dask. These have touched on several portions of the Dask codebase, but generally have centered around bug fixes for Dask Arrays which enable larger-than-memory, distributed array computations. This work not only benefits the organization funding the development, but helps the entire project at large. To learn more about funding open source projects through CWOs, check out [this post](http://labs.quansight.org/blog/2019/05/community-driven-opensource-funded-development/) by Ralf Gommers which discusses the CWO model.

<!-- TEASER_END -->

In addition to working on Dask directly, we've also been engaging the broader scientific Python community through attending conferences. In particular, developers at Quansight, Anaconda, and NVIDIA organized a Dask sprint at the SciPy 2019 conference. Throughout the two-day sprint, core developers were able to help sprint attendees become more familiar with the Dask codebase, set up local development environments, and even get new pull requests from sprinters submitted, reviewed, and merged into Dask! I personally had a great time at SciPy and hope to see lots of familiar faces again next year. Likewise, in July I gave a talk on Dask at the Data-Driven Wisconsin 2019 conference (materials presented at the talk can be found [here](https://github.com/jrbourbeau/ddw-dask)). Following my talk, I had several engaging discussions with other conference attendees and it was really gratifying to see all the enthusiasm surrounding Dask.

Finally, there's been a push for a more coordinated effort towards project maintenance and development by core Dask developers at Quansight, Anaconda, and NVIDIA. As part of this effort, we're able to spend a portion of our work week on day-to-day project maintenance tasks (e.g. fixing CI systems, responding to issues, reviewing pull requests, etc.) as well as working on contributions that require significant amounts of time or expertise to implement (e.g. large-scale refactoring, adding new features, writing new portions of documentation, etc.). Today, Dask users typically get a faster response when opening an issue or pull request and the project is overall better maintained as a result of these efforts.
