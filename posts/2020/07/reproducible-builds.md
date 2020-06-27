<!--
.. title: IPython reproducible build
.. slug: ipython-reproducible-builds
.. date: 2020-07-XX 01:00:00 UTC-00:00
.. author: Matthias Bussonnier
.. tags: Labs, IPython
.. category:
.. link:
.. description:
.. type: text
-->

Starting with IPython 7.16.1, you _should_ be able to recreate the sdist (.tar.gz) and wheel (.whl), and get bytes for
bytes identical result to the ones publish on PyPI. This is a critical step toward being able to _trust_ your computing
platforms, and a key component to improve efficiency of build platform.

<!-- TEASER_END -->

Since the cornerstone Paper [Refections on trusting Trust][1], there are always been advocate of reproducible builds, in
todays highly interconnected worlds, and the speed at which new software is released and deployed, being able to confirm
the provenance and verify that supply chain has not been affected by malicious actor is often critical.  To help in this
endeavour, the movement of [reproducible builds][2], attempt to push software toward a deterministic and reproducible
build process.


For the users of the Scientific Python ecosystem, the notion of reproducibility/replicability is not new, and is one of
the key idea behind the scientific process. Given some instructions from an author, you should be able to perform some
experiments or proof, and reach the same conclusion. When the contrary then your instructions or hypothesis are missing
some variable elements and your model is incomplete; having a complete model, reproducible, is one of the necessary
component to be able to trust the results and build upon it. 

# Aren't computer reproducible by design ? 

One of the requisite for reproducibility is to have a deterministic process, and while we tend to think about computers
as deterministic things, they often are not, and on purpose. Mainly driven by security concern, a number of processes in
a computer use pseudo-randomness to prevent an attacker from gaining control over a system. Thus by default, many of the
typical actions you may do in a software (iterating over a dictionary in Python), with have _some_ randomness in them,
which impact the determinism of a process. 

To obtain a reproducible results, one thus often need to make sure each step is deterministic, and that all the variable
influencing that process are either controlled, or recorded.

# Reproducible artifact build

In IPython 7.16.1 we have tried to removed all sources of variability, by controlling the order in which the files are
generated, archived in the sdists, their metadata, timestamp... etc. Thus should be able to go from the commit in the
source repository to the sdist/wheel and obtain an identical result. This should help you to trust that no backdoor has
been introduced in the released packages, though this is also critically useful for efficiency in package managers.

# Efficient dependencies rebuild. 

Currently IPython depends on many packages: `prompt_toolkit`, traitlets, setuptools, ...etc, and we have a number of
dependees, ipykernel, then jupyter notebook... When dependencies tree is rebuilt for a reason or another, a change of a
single bit could trigger the rebuild of the all chain. When package like IPython are not reproducible, this mean that a
rebuild of IPython – whether it has changed or not – could trigger a rebuild of all downstream elements. With
reproducible build, you can break this rebuild chain and stop as soon as a dependency has not changed.

This has the opportunity to massively decrease the time spend by platform like conda-forge on rebuilding the ecosystem
on new version of Python; decrease the bandwidth and disk space usage for end users as when versions are identical they
do not need to be re-downloaded. 







2: https://reproducible-builds.org/
1: https://www.cs.cmu.edu/~rdriley/487/papers/Thompson_1984_ReflectionsonTrustingTrust.pdf
