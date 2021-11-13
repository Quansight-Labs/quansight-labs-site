<!--
.. title: A vision for extensibility to GPU & distributed support for SciPy, scikit-learn, scikit-image and beyond
.. slug: pydata-extensibility-vision
.. date: 2021-11-15 10:00:00 UTC-07:00
.. author: Ivan Yashchuk, Ralf Gommers
.. tags: SciPy, NumPy, CuPy, scikit-learn, scikit-image, uarray, Array API
.. category:
.. link:
.. description:
.. type: text
.. previewimage: /images/2021/11/nep-0047-library-dependencies.png
-->


Quansight Labs is partnering with AMD to develop a new extensibility system for
the PyData stack. This work will enable the PyData libraries to be executed on a
GPU, as well as running in distributed mode across multiple GPUs. In this blog
post, we talk about the motivation behind the proposal and describe our vision
for making array libraries more interoperable.

With the proposed dispatch layers, the downstream libraries would be enabled to
use multiple kinds of arrays, without having to have a hard dependency on all of
those array libraries. We want to have a unified design using the same tools
applicable across SciPy, scikit-learn, scikit-image and other libraries. In this
situation, it's best to have a discussion spanning multiple projects.
<!-- This post is the invitation to discuss the idea on this forum https://discuss.scientific-python.org/ -->


<p align="center">
    <img
     alt="A diagram showing possible interconnections that would be enabled by Array API."
     src="/images/2021/11/nep-0047-library-dependencies.png">
    <i><br>Possible interconnections that Array API enables.</i>
</p>

<!-- TEASER_END -->

Over the years array computing in Python has evolved to support distributed
arrays, GPU arrays, and other various kinds of arrays that work with specialized
hardware, or carry additional metadata, or use different internal memory
representations. The foundational library for array computing in the PyData
ecosystem is NumPy. But NumPy alone is a CPU-only library - and a
single-threaded one at that - and in a world where it's possible to get a GPU or
a CPU with a large core count in the cloud cheaply or even for free in a matter
of seconds, that may not seem enough. For the past couple of years, a lot of
thought and effort has been spent on devising mechanisms to tackle this problem,
and evolve the ecosystem in a gradual way. We feel like a shared vision has
emerged, in bits and pieces. In this post, we aim to articulate that vision and
suggest a path to making it concrete, focusing on three libraries at the core of
the PyData ecosystem: SciPy, scikit-learn and scikit-image.

Today, SciPy, scikit-learn and scikit-image only work with NumPy arrays. SciPy
has had "support for distributed and GPU arrays" [on its
roadmap](http://scipy.github.io/devdocs/dev/roadmap.html) for a couple of years.
Parallel execution and GPU support were two of the top three priorities named by
the 1000+ users in [the 2020 NumPy user
survey](https://numpy.org/user-survey-2020/). The scikit-learn technical
committee listed "evaluate interoperability with other types of arrays that are
compatible with the NumPy API" as one of its 2020-2021 priorities. And
scikit-image included exploring multi-threading and GPU acceleration in its
(successful) [CZI grant
proposal](https://chanzuckerberg.com/eoss/proposals/gpu-acceleration-rapid-releases-and-biomedical-examples-for-scikit-image/).

Despite NumPy being a CPU-only library, it still can be used with alternative
arrays due to its dispatch mechanism allowing users and library authors to write
backend and hardware agnostic code using the NumPy API. When passing as input an
alternative array (say from CuPy or Dask) to such generic code, the
hardware-specific implementation is invoked instead of the internal to NumPy
implementation. The NumPy API is a powerful tool for writing generic code and it
is followed by several array libraries. Some libraries, like JAX and CuPy, had
NumPy compatibility from the start, while other libraries, like PyTorch, are
gradually moving towards it.

One of the problems of using the NumPy API as a reference standard is that it
wasn't designed with different types of hardware in mind and has a number of inconsistencies that make it difficult for other libraries to re-implement its API. [Array API
project](https://data-apis.org/array-api/latest/index.html) solves this problem
by standardizing functionality across most array libraries. NumPy and CuPy have
already adopted the Array API standard together with the new
`__array_namespace__` dispatch mechanism. The common architecture of SciPy,
scikit-learn, and scikit-image is that they use NumPy for array operations, and
critical-to-performance parts are written using compiled code extensions.
Unfortunately, compiled extensions rely on NumPy's internal memory
representation and are restricted to CPU computations. For these reasons, Python
code with compiled extensions is not compatible with NumPy's dispatching
capabilities; it would not know how to deal with a GPU array. It's also very
challenging to rewrite the libraries to use pure NumPy without sacrificing
performance. To solve the problem we should introduce a dispatching mechanism (similar to NumPy's) that would be used for the modules that rely on compiled
extensions.

Let's imagine some SciPy module that equally depends on compiled code and NumPy
functions. Removing all forced conversions to NumPy arrays inside the module
would open the "Dispatcher" path, but only half of the SciPy module's
functionality would work for generic arrays. In the diagram, the NumPy
Dispatcher is an abstract mechanism, concretely it could be an
`__array_function/ufunc__`-based one for older versions of NumPy or
`__array_namespace__` - for NumPy 1.22+.

<p align="center">
    <img
     alt="A schema using NumPy dispatcher."
     src="/images/2021/11/scipy-numpy-dispatch.png">
    <i><br>A SciPy module with NumPy "Dispatcher".</i>
</p>

<!-- ![numpy dispatch schema](https://drive.google.com/uc?export=view&id=1-PySRskT3-76r_KiiKGfkC485dT6uKoV) -->

For SciPy and similar libraries, we need to follow NumPy's example and add our
own dispatching layer for the API to allow users to develop generic code that
works with arrays from different libraries. Then it would be possible to
directly reroute to specific array implementations bypassing compiled code
paths.

<p align="center">
    <img
     alt="A schema using SciPy dispatcher."
     src="/images/2021/11/scipy-ndimage-dispatcher.png">
    <i><br>A SciPy module with its own "Dispatcher".</i>
</p>

<!-- ![scipy.ndimage dispatch schema](https://drive.google.com/uc?export=view&id=1-ZoVxenDufJuUwcONV_mFY0NFNY3wOCq) -->

## Goals, wishes, and constraints

Goal: separate the interface from the implementation and let the dispatching
system help users and library authors write generic code that works with
different kinds of arrays.

The new dispatching system implemented for SciPy and scikits should:

* make the API extendable and add the possibility to support alternative array
  libraries, not just NumPy
* provide a way to select backend for the same array type (example: `scipy.fft`
  + alternative CPU FFT libraries, scikit-learn + [Intel optimized
  implementation](https://github.com/intel/scikit-learn-intelex))
* be able to extend function signature in a backward-compatible way on the base
  library side (all alternative implementations should not break after the
  change)
* have as low overhead as possible.

When designing API override systems, there are many possible design choices.
Three major axes of design decisions in the context of NumPy API overrides are
outlined in [the appendix of NumPy Enhancement Proposal (NEP)
37](https://numpy.org/neps/nep-0037-array-module.html#appendix-design-choices-for-api-overrides);
they are also applicable outside of NumPy:

* Opt-in vs. opt-out for users
* Explicit vs. implicit choice of implementation
* Local vs. non-local vs. global control.

## A concrete design proposal

In the figure below, we highlight the parts of the design for implementing the
CuPy backend in SciPy, scikit-learn, scikit-image and other core projects which
now rely only on NumPy. We are going to use two dispatching mechanisms: one for
the modules with compiled code portions, and one for the pure Python functions.
The first dispatching mechanism is based on the [`uarray`
project](https://uarray.org/), which is a backend dispatcher that allows us to
choose the relevant function implementation at runtime. The second dispatching
mechanism is based on the ``__array_namespace__`` method from the Array API
standard, which is a method that allows us to get the Array API implementation
module specific to CuPy (or any other array library) at runtime. The
``__array_namespace__`` will be available in NumPy 1.22 and CuPy v10.0.

The dispatch using ``__array_namespace__`` method is:

* opt-in for users  
  The new dispatching works only when users choose to use the new Array API
  compatible modules.
* explicit  
  The dispatched functions are determined via the method of the array object
  user creates.
* with local control  
  Which implementation to use is determined by calling methods on the direct
  arguments of a function.

And the `uarray` dispatcher is:

* opt-out for users
* can be implemented to be explicit or implicit
* can be implemented to have local, non-local or global control


<p align="center">
    <img
     alt="A diagram outlining CuPy support for SciPy and scikits."
     src="/images/2021/11/CuPy_support_scipy_scikits_with_details.png">
    <i>
    <br>Proposed dispatch mechanism layers for enabling CuPy and Dask support.
    <br>This will also support any other array library with the same Array API standard support and `uarray` backends.
    </i>
</p>

## Array API dispatching system

Array API is a standard specification of functionality that array libraries need
to implement. There is a [dedicated test
suite](https://github.com/data-apis/array-api-tests) to verify the compliance of
specific implementations with the standard, so it's easy to check all libraries
adopting the standard to have a unified behavior. NEP 47 has a couple of
examples on [usage of the Array API
namespace](https://numpy.org/neps/nep-0047-array-api-standard.html#adoption-in-downstream-libraries).

`__array_namespace__` is a central piece of the Array API dispatch method. It is
a method of an array object that returns an object that has all the array API
functions on it. In the case of NumPy calling `__array_namespace__() ` would
return `numpy.array_api` module. The `__array_namespace__` method attached to
the array object enables downstream libraries to consume multiple kinds of
arrays, without having to have a hard dependency on any of those array
libraries. The pattern to support multiple array libraries is intended to be
similar to the following code snippet:

```python
def somefunc(x, y):
    # Retrieves standard namespace.
    # Raises if x and y have different namespaces.
    xp = get_namespace(x, y)
    out = xp.mean(x, axis=0) + 2*xp.std(y, axis=0)
    return out
```

Notice that to make the above code valid, we don't need to import the package
that implements mean and std functions explicitly; the required module is stored
in x and y variables.

For several concrete use cases of the Array API check out [the dedicated
page](https://data-apis.org/array-api/latest/use_cases.html) of the standard.
Anirudh Dagar also [wrote a great
demo](https://quansight-labs.github.io/array-api-demo/GW_Demo_Array_API.html)
recreating gravitational waves tutorial and showcasing what it would take to
support PyTorch tensors for a subset of SciPy API using `__array_namespace__`.

## PyData dispatching system

In the future, we'd like to pass alternative arrays to SciPy and scikits
functions and get the results without transforming internally to NumPy arrays.
Instead, it would automatically handle dispatching to the appropriate
implementation, for example, `cupyx.scipy` for GPU-accelerated SciPy functions,
scikit-learn-intelex for Intel optimized version of scikit-learn, or cuCIM for
GPU-accelerated scikit-image. Usually in statically typed languages function
overloading is used to implement a function with the same name but arguments of
different types. How can we implement something similar to functions overloading
but in Python? Well, we could implement one central function checking the types
of the arguments using `isinstance()`, or `issubclass()` and calling appropriate
implementations based on these checks. This approach doesn't scale well with the
number of inputs of different types and is not extendable by third-party
implementers without modifying the source code. Another approach is to use
_multiple dispatch_, where each function has multiple variants that are chosen
based on dynamically determined types. Unfortunately, the multiple dispatch
feature is not built-in for Python, but there's a simpler version - _single
dispatch_. For a demo, let's begin with a tool from the Python standard library:
`functools.singledispatch`.

```python
from functools import singledispatch
import scipy.ndimage as _scipy_ndimage

@singledispatch
def laplace(input, output=None, mode="reflect", cval=0.0):
    return _scipy_ndimage.laplace(input, output=output, mode=mode, cval=cval)

# export `laplace` as `scipy.ndimage.laplace`

# In CuPy codebase
# from scipy.ndimage import laplace
import cupyx.scipy.ndimage as _cupyx_ndimage

@laplace.register(cupy.ndarray)
def cupy_laplace(input, output=None, mode="reflect", cval=0.0):
    return _cupyx_ndimage.laplace(input, output=output, mode=mode, cval=cval)

# run registration code when CuPy is imported
```

We begin by defining the base `laplace` function, it is a fallback
implementation that is going to be called for non-registered types of `input`.
Next `laplace.register` is used to connect the implementation that is specific
to `cupy.ndarray` with the base `laplace` function. We get a function in the
`scipy.ndimage` module that is now compatible with CuPy arrays. Similarly, it
can be extended to work with Dask arrays.

```python
from scipy.ndimage import laplace
import numpy as np
import cupy as cp

numpy_img = np.random.normal(size=(256, 256))
cupy_img = cp.array(numpy_img)

print(type(laplace(numpy_img)))
# <class 'numpy.ndarray'>

print(type(laplace(cupy_img)))
# <class 'cupy._core.core.ndarray'>
```

Since Python doesn't provide standard tools for using multiple dispatch there
are several dedicated libraries:

* _multimethod_ - pure Python implementation of multiple dispatch with caching
  of argument types
* _plum-dispatch_ - implementation of multiple dispatch that follows the ideas
  from Julia
* _uarray_ is a generic backend/multiple dispatch library similar to NumPy's dispatch functionality
  except that the implementation doesn't need to be baked into the array type.

The first two options are very similar in functionality and usability. But the last
option, in addition to multiple dispatch, offers granular control using context
managers and provides a way to switch backends for the same array type. It's
also possible to make the `uarray` dispatcher work without a context manager
making the mechanism implicit and similar to other dispatch libraries. Whether
we should encourage the implicit registration of backends or not is an open
design issue and there's previous discussion on the topic in [SciPy
#14266](https://github.com/scipy/scipy/issues/14266). Hameer Abbasi, one of the
`uarray` authors, wrote [a blog
post](https://labs.quansight.org/blog/2019/07/uarray-update-api-changes-overhead-and-comparison-to-__array_function__/)
about the motivation for `uarray` and how it compares to NumPy's
`__array_function__` dispatch mechanism.

## It's already happening

SciPy has GPU and distributed arrays support [on the
roadmap](http://scipy.github.io/devdocs/dev/roadmap.html), but adding this
support directly to the library would inflate the scope and increase the
maintenance burden significantly. scikit-learn has [explicitly
stated](https://scikit-learn.org/stable/faq.html#will-you-add-gpu-support) that
they cannot afford GPU-specific code in their codebase. A dispatching system is
a low-maintenance solution for extending the functionality of the API.

In 2019, Peter Bell added support for backend switching to the `scipy.fft` module
([PR #10383](https://github.com/scipy/scipy/pull/10383)) using `uarray`. Now
it's possible to tell SciPy to use, for example, CuPy backend, for computing FFT
when CuPy's array is passed to functions from `scipy.fft`.

In a recent blog post titled [Array Libraries
Interoperability](https://labs.quansight.org/blog/2021/10/array-libraries-interoperability/),
Anirudh Dagar explores array interoperability protocols: `__array_function__`
(NEP 18), `__array_namespace__` (NEP 47) and `uarray`. The blog post includes a
[section comparing the Array API and
`uarray`](https://labs.quansight.org/blog/2021/10/array-libraries-interoperability/#protocol_differences)
approaches for interoperability.

## Acknowledgment

Adding dispatch support will take significant effort to get implemented across
different projects. Fortunately, AMD recognizes the problem and is willing to
help to fix it by funding Quansight developers to do the initial work.

AMD's vision for the developer community is open, portable tools that enable the
same source code to run on different hardware platforms. ROCm is an example of
this, supporting both OpenMP and HIP on multiple architectures. "AMD and
Quansight are aligned in this direction. We believe that by working together and
working with the Python community, we can achieve an open, portable solution for
all Python developers," says Terry Deem, AMD Product Manager for ROCm.

<p align="left">
    <img
     alt="AMD logo."
     src="/images/sponsors/AMD_E_Blk_RGB.png">
    <i></i>
</p>
