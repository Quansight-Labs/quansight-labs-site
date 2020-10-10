<!--
.. title: Manylinux1 is obsolete, manylinux2010 is almost EOL, what is next?
.. slug: manylinux1-is-obsolete-manylinux2010-is-almost-eol-what-is-next
.. date: 2020-10-08 14:00:06 UTC-05:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->

The basic installation format for users who install packages via `pip` is
the wheel format. These wheels' name is composed of four parts: a
package-name-and-version tag (whihc can be further broken down), a python tag,
an ABI tag, and a platform tag. More information on the tags can be found in
[PEP 425](https://www.python.org/dev/peps/pep-0425).  So a package like NumPy
will be available on PyPI as `numpy-1.19.2-cp36-cp36m-win_amd64.whl` for 64-bit
windows and `numpy-1.19.2-cp36-cp36m-macosx_10_9_x86_64.whl` for macOS. Note
only the plaform tag differs. 

But what about linux? There is no vendor controlled "linux platform" (Ubuntu,
RedHat, Fedora, Debian, FreeBSD: did I leave out your favorite?). What most
linuxes (sp?) do have in common is the glibc runtime library, and a smattering
of various additional system libraries. So it is possible to define a least
common denominator (LCD) of software expected to be on a linux platform
(rounding some corners around non-glibc distributions).

The decision to converge on a LCD common platform gave birth to the
[manylinux1](https://www.python.org/dev/peps/pep-0513/) standard. Going back
to our example, numpy is available as
`numpy-1.19.2-cp36-cp36m-manylinux1_x86_64.whl`.

The first manylinux standard, manylinux1 was based on CentOS5 which has [been
obsolete](https://endoflife.software/operating-systems/linux/centos) since
March, 2017. The subesquent manylinux2010 standard, based on CentOS6, will hit
end-of-life in December 2020. The manylinux2014 standard still has some
breathing room, based on CentOS7 it will reach end-of-life in July 2024.

So what is next for `manylinux`, and what `manylinux` should users and package
maintainers use?

<!-- TEASER_END -->

## If `manylinux1` is obsolete, why are there still manylinux1 wheels?

Wheels are typically consumed by `pip` via `pip install`. Manylinux wheels are
typically used for projects that require compilation, otherwise they would ship
pure python wheels with the "none" platform tag, meaning they are compatible with
any platform. So say you are a library author and want to make it convenient
for users to install your package. If you ship a manylinux2014 wheel, but the
version of pip your users have is too old to support manylinux2014 wheels, pip
will happily download the source package and compile it for them. Havoc ensues:
windows users typically cannot compile, prerequisites will be missing.

Pip began supporting manylinux2010 wheels with [version
19.0](https://github.com/pypa/pip/blob/master/NEWS.rst#190-2019-01-22),
released in Jan 2019. The version of pip officially shipped with Python3.6, via
the [ensurepip](https://docs.python.org/3.6/library/ensurepip.html) module, is
version 18. Python3.7 ships pip 20. It is easy enough to upgrade, but to be on
the safe side, and prevent havoc, library authors will ship a manylinux1 wheel
for Python3.6 support.

## What happens now that Python3.6 is falling out of favor?
[Python 3.6 is no longer in active
development](https://www.python.org/dev/peps/pep-0494). In fact, the scientific
python data community has decided to stop actively supporting Python3.6 [from
July
2020](https://numpy.org/neps/nep-0029-deprecation_policy.html#support-table).
So I would expect to see projects begin to drop the older manylinux1 format,
and drop support for Python3.6 sooner rather than later.

## What about Conda packages?
Conda does not use the same kind of wheel format provided by PyPI and `pip`. Their
build system is internally consistent and they build a binary package for each
OS they support, thus they are not bound to the manylinux designation.
Conda does not have a declared policy around deprecating Python3.6.

## What comes after manylinux2014?
The glibc used in manylinux2014 is defined as the one used by CentOS7. This OS
was released in June 2014. This manylinux standard, for the first time,
declared support for non-x86 hardware systems like ARM64 (aarch64), Power
(ppc64) and S390X.  However the ARM platform has grown greatly since 2014, and
glibc has moved from version 2.17 to 2.31, fixing many bugs. Since the real
driver for platform compatibility is glibc, [PEP
600](https://www.python.org/dev/peps/pep-0600/) defined a "perenial manylinux
spec" that is based on the glibc version number. A lot of work has [already
taken place](https://github.com/pypa/manylinux/issues/542) to support the next
version. Now we need to take the dive: decide what the base OS for the next
manylinux tag will be, roll out a docker image and tooling around it, and
convince library packaging teams to adopt it.


## OK, so what is the bottom line?

- Use pip v20 or later to make it easier on libarary packagers: modern pip
  versions will take the latest manylinux package they can support and will be
  forward-compatible with the PEP 600 perenial manylinux standard.
- Manylinux1 and Python3.6 are going away. Update your systems.

Matti
