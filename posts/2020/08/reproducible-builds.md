<!--
.. title: IPython reproducible build
.. slug: ipython-reproducible-builds
.. date: 2020-08-05 22:00:00 UTC-00:00
.. author: Matthias Bussonnier
.. tags: Labs, IPython, reproducible-builds, packaging
.. category:
.. link:
.. description:
.. type: text
-->

Starting with IPython 7.16.1 (released in June 2020), you _should_ be able to recreate the sdist (`.tar.gz`) and wheel
(`.whl`), and get bytes for bytes identical result to the ones publish on PyPI. This is a critical step toward being able
to _trust_ your computing platforms, and a key component to improve efficiency of build and packaging platform, with
potentially impacts on fast conda environment creation for users. The following goes into some reason of why you should care.

<!-- TEASER_END -->

Since the cornerstone Paper [Refections on trusting Trust][1], there are always been advocate of reproducible builds, in
todays highly interconnected world, and with the speed at which new software is released and deployed, being able to confirm
the provenance and verify that supply chain has not been affected by malicious actor is often critical. To help in this
endeavour, the movement of [reproducible builds][2], attempt to push software toward a deterministic and reproducible
build process.

[2]: https://reproducible-builds.org/
[1]: https://www.cs.cmu.edu/~rdriley/487/papers/Thompson_1984_ReflectionsonTrustingTrust.pdf

While security is one of the earliest concepts that advocated for reproducible build, there are a number of other
advantages to ensure the same artifacts can be reproduced identically.

For the users of the Scientific Python ecosystem, the notion of reproducibility/replicability is not new, and is one of
the critical idea behind the scientific process. Given some instructions from an author, you should be able to perform some
experiments or proof, and reach the same conclusion. When the contrary then your instructions or hypothesis are missing
some variable elements and your model is incomplete; having a complete model, reproductible, is one of the necessary
component to be able to trust the results and build upon it. We are not going to enter into the exact distinction
between reproducible and replicable, both have their goal and uses.

# Aren't computer reproducible by design ? 

One of the requisite for reproducibility is to have a deterministic process, and while we tend to think about computers
as deterministic things, they often are not, and on purpose. Mainly driven by security concern, a number of processes in
a computer use pseudo-randomness to prevent an attacker from gaining control over a system. Thus by default, many of the
typical actions you may do in a software (iterating over a dictionary in Python), with have _some_ randomness in them,
which impact the determinism of a process.

There are of course a number of source of involuntary randomness doe to the practicality of computer systems. Among
other, the current date and time, your user name and uid, hostname, order of files on your hard drive, and in which
order they may be listed...

To obtain a reproducible results, one thus often need to make sure each step is deterministic, and that all the variable
influencing that process are either controlled, or recorded.

# Reproducible artifact build

In IPython 7.16.1 we have tried to removed all sources of variability, by controlling the order in which the files are
generated, archived in the sdists, their metadata, timestamp... etc. Thus should be able to go from the commit in the
source repository to the sdist/wheel and obtain an identical result. This should help you to trust that no backdoor has
been introduced in the released packages, though this is also critically useful for efficiency in package managers.

Of course you have to trust that the IPython source itself, and its dependencies are devoid of backdoors, but let's move
one step at a time. Reproducible build artifacts can also have impact on the build and installation process of packages.

# Efficient dependencies rebuild. 

Currently IPython depends on many packages: prompt_toolkit, traitlets, setuptools, ...etc, and we have a number of
dependees, ipykernel, then jupyter notebook... When dependencies tree is rebuilt for a reason or another, a change of a
single bit could trigger the rebuild of the all chain. When package like IPython are not reproducible, this mean  a
rebuild of IPython – whether it has changed or not – could trigger a rebuild of all downstream elements.

With reproducible build, you can trust that the artifact will not change after a rebuild. For the functional programmer
around you it indicate that the process of building from the source is a pure function. Therefore it can safely be part
of a distributed system (rebuilding on two different places will give the same result, so you can avoid costly data
movement), and we can also do caching of results, so for identical input we know the output will be identical.

This can allow break rebuild chains and stop as soon as soon as a dependency rebuild has no effect.

This has the opportunity to massively decrease the time spend by platform like conda-forge on rebuilding the ecosystem
on new version of Python; making new packages available faster. 

# Deduplication

One rarely mentioned advantage is de-duplication. In many cases there are no reasons why artifacts produce by a build
step would depends on all their input. For example IPython has currently no reason to build differently on Python 3.7,
3.8, and soon to be release 3.9, linux/macOS/ of windows. Nevertheless Conda provides no less than 10 downloads for each
release of IPython. 

```bash
$ diff -U0  <(cd ipython-7.17.0-py37hc6149b9_0/ ; fd -tf --full-path  | xargs -L1 md5)  <(cd ipython-7.17.0-py38h1cdfbd6_0/ ; fd --full-path  -t f | xargs -L1 md5)
--- /dev/fd/63	2020-08-05 15:15:47.000000000 -0700
+++ /dev/fd/62	2020-08-05 15:15:47.000000000 -0700
@@ -316 +316 @@
-MD5 (Lib/site-packages/ipython-7.17.0.dist-info/RECORD) = 0ebe6e43ae9dcfc29b86338605fc9065
+MD5 (Lib/site-packages/ipython-7.17.0.dist-info/RECORD) = 16f820e051e75462d970be438fbd2b0a
@@ -319 +319 @@
-MD5 (Lib/site-packages/ipython-7.17.0.dist-info/direct_url.json) = 2c37570ef1bd3eadd669649da321b69f
+MD5 (Lib/site-packages/ipython-7.17.0.dist-info/direct_url.json) = b55d0dcd87b11218d41c34d8ee0a5016
@@ -331 +331 @@
-MD5 (info/files) = d24cc180f95193be847116340f1af63a
+MD5 (info/files) = 0161e68902cb78c6b1aec564c0a9e808
@@ -333,2 +333,2 @@
-MD5 (info/hash_input.json) = d25b93fadc7421a297daf02f9a04584f
-MD5 (info/index.json) = 0fb13436b493433c08c9b29c23b76180
+MD5 (info/hash_input.json) = b7c843bd4a6cef64080e893a939e95bd
+MD5 (info/index.json) = 6283e83efc554f9f5b4d4e2330d8ec4e
@@ -336,3 +336,3 @@
-MD5 (info/paths.json) = 06e6ba2378d6eecdfcf08e1c602d392b
-MD5 (info/recipe/conda_build_config.yaml) = 1a98301b552bde7a25c99a39711c9fe2
-MD5 (info/recipe/meta.yaml) = 1a823d7c8c2dac394617482c596f26f0
+MD5 (info/paths.json) = 0a82a812984f98660fbf0244eddeed38
+MD5 (info/recipe/conda_build_config.yaml) = e1c3ae7827bd7003e9034720c7b0f76c
+MD5 (info/recipe/meta.yaml) = 08d5f54df6083bfb834b24b9ae4c4e0f
@@ -342 +342 @@
-MD5 (info/test/test_time_dependencies.json) = a66ce3a62bd757ceede3ad5ef4c2c4b6
+MD5 (info/test/test_time_dependencies.json) = ca1e35258bf3ce4719b090a90f886cd6
```

I'm sure _some_ of these changes are necessary as the refer to which Python version the package refers to ; but let's
look in more detail at one of those:

```bash
$ fd test_time_dependencies.json | xargs diff -U2
--- ipython-7.17.0-py37hc6149b9_0/info/test/test_time_dependencies.json	2020-07-31 21:41:11.000000000 -0700
+++ ipython-7.17.0-py38h1cdfbd6_0/info/test/test_time_dependencies.json	2020-07-31 21:40:53.000000000 -0700
@@ -1 +1 @@
-["matplotlib", "nbformat", "pygments", "ipykernel", "nose >=0.10.1", "trio", "numpy", "pip", "testpath", "requests"]
+["requests", "numpy", "matplotlib", "trio", "testpath", "pip", "pygments", "nbformat", "ipykernel", "nose >=0.10.1"]
```

Here the changes are minor; and completely inconsequential for the use of the package, and woudl prevent us from
detecting that two build are actually identical.

This could allow to decrease precious disk space, bandwidth, and time spend waiting for software to install. 

I would recommend Go talk as well to some [Nix][Nix] Users to see how a purely functional package manager works and
which other advantage this brings.

But in the meantime, please go track the various source of randomness in your favorite library or build system, and
let works together to change things so that that things never changes.





[Nix]: https://nixos.org/

