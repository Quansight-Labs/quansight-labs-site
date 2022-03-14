<!--
.. title: Making GPUs accessible to PyData Ecosystem via Array API
.. slug: making-gpus-accessible-to-pydata-ecosystem-via-array-api
.. date: 2022-02-01 21:07:02 UTC-06:00
.. author: Amit Kumar
.. tags: GPU, SciPy, NumPy, CuPy, scikit-learn, scikit-image, Array API
.. category: 
.. link: 
.. description: 
.. type: text
.. previewimage: /images/2022/02/array_api_workflow.svg
-->



GPUs have become an essential part of the scientific computing stack and with
the advancement in the technology around GPUs and the ease of accessing a GPU
on cloud or on-prem, it is in the best interest of the PyData community to spend
time and effort to make GPUs accessible for the users of PyData libraries. A
typical user in the PyData ecosystem is quite familiar with the APIs of libraries
like scipy, scikit-learn, scikit-image and at the moment all these
libraries only support single core operations on CPU. In this blog post will
talk about how we can use Array API with the fundamental libraries in the PyData
ecosystem along with cupy for making GPUs accessible to the users of these libraries.
With the introduction of the [Python Array API Standard](https://data-apis.org/array-api/latest/)
by the [Consortium for Python Data API Standards](https://data-apis.org/) and it’s
adoption mechanism in the [NEP 47](https://numpy.org/neps/nep-0047-array-api-standard.html)
it is now possible to write code that is portable between NumPy and other array/tensor
libraries that adopt the Array API Standard. We will also discuss the workflow and
challenges for achieving the same.

<!-- TEASER_END -->

## Motivation and Goal

The motivation for this exercise comes from the fact that having GPU-specific code
in SciPy and scikits will be too-specialized and very hard to maintain. The ultimate
goal is to have GPU support in SciPy, scikit-learn and scikit-image using CuPy. Since
CuPy has support for NVIDIA GPUs as well as AMD’s ROCm GPU platform, this demo will
work on either of those GPUs.

### A primer on Array API Standard

![Data APIs logo](/images/2022/02/data-apis-logo.png)

As of today, NumPy with over 100 millions monthly downloads (combined from conda
and PyPi) is the fundamental library of choice for array computing. In the past
decade a plethora of array libraries have evolved, which more or less derives
from NumPy’s API and it’s API is not very well defined. This is due to the fact
that NumPy is a CPU-only library and today these dependent libraries are built
for a variety of exotic hardware. As a consequence the APIs of these libraries
have diverged a lot, So much so that it’s quite difficult to write code that
works with multiple (or all) of these libraries. The Array API standard aims
to address this issue, by specifying an API for the most common ways arrays
are constructed and used. At the time of writing this, NumPy (>=1.22.0) and
CuPy (>=10.0.0) have adopted the Array API Standard.


##### Note about using Array API Standard

The definition of Array API Standard and it’s usage may evolve over time and
this blog post is just an example of how we can use it to make GPUs accessible
to the users of libraries like scipy and scikits and it doesn’t not necessarily
define the best practices around adopting the standard. The best practices for
adopting Array API is still a work very much in progress and will evolve drastically.


## Demonstration Example

The example we have chosen to demonstrate adopting the Array API standard to make
GPUs accessible in SciPy and scikits is the one taken from scikit-learn’s
documentation: Segmenting the picture of greek coins in regions. This example
uses Spectral clustering on a graph created from voxel-to-voxel difference on
an image to break this image into multiple partly-homogeneous regions (or say clusters).
In essence spectral clustering is about finding the clusters in a graph i.e.
finding the mostly connected subgraph and thereby identifying the clusters alternatively
it can be described as finding subgraphs having maximum number of within cluster connections
and minimum number of between cluster connections.

### Dataset

<p align="center">
    <img
     alt="Greek coins from Pompeii"
     src="/images/2022/02/greek_coins_original.jpeg">
</p>
<p align="center">
<i>Greek coins from Pompeii ("British Museum, London, England")</i>
</p>

The dataset we are using for this demonstration is of greek coins from Pompeii
(from skimage.data.coins module). This is a data of image of several coins outlined
against a gray background.

We convert the data of the coins into a graph object and then apply spectral
clustering to it for segmenting coins.

Source: [https://www.brooklynmuseum.org/opencollection/archives/image/51611](https://www.brooklynmuseum.org/opencollection/archives/image/51611)

## Process

#### `get_namespace` - getting the array API module

The [NEP 47](https://numpy.org/neps/nep-0047-array-api-standard.html) (Adopting
the array API standard) outlines a basic workflow for adopting array API
standards for array provider and consumer libraries. Now we will describe
in detail about how we went through the process of implementing this.

The Array API defines a method named `__array_namespace__` which returns
the array API module with all the array API methods accessible from it.
It has a couple of key benefits:

- for the array consumer libraries to be able to check if the incoming array
  supports Array API standard.
- to get all the methods for the array object without having the need to import
  the Array API module explicitly.

The NEP 47 recommends defining a utility function named `get_namespace` to check
for such an attribute.

An example of potential implementation of `get_namespace` function is defined as follows:

```python
import numpy as np


def get_namespace(*xs):
    # `xs` contains one or more arrays, or possibly Python
    # scalars (accepting those is a matter of taste, but
    # doesn't seem unreasonable).
    namespaces = {
        x.__array_namespace__() 
        if hasattr(x, '__array_namespace__') else None
        for x in xs if not isinstance(x, (bool, int, float, complex))
    }

    if not namespaces:
        # one could special-case np.ndarray above or use np.asarray here
        # if older numpy versions need to be supported.
        raise ValueError("Unrecognized array input")

    if len(namespaces) != 1:
        raise ValueError(f"Multiple namespaces for array "
         "inputs: {namespaces}")

    xp, = namespaces
    if xp is None:
        # Use numpy as default
        return np, False
    return xp, True
```

#### Workflow - for using `get_namespace`

Now let's walk through an example to see how this works in practice. Consider
the following function from SciPy:

```python
def getdata(obj, dtype=None, copy=False):
    """
    This is a wrapper of `np.array(obj, dtype=dtype, copy=copy)`
    that will generate a warning if the result is an object array.
    """
    data = np.array(obj, dtype=dtype, copy=copy)
    # Defer to getdtype for checking that the dtype is OK.
    # This is called for the validation only; we don't need
    # the return value.
    getdtype(data.dtype)
```

This function is taken from `scipy/sparse/_sputils.py`. We can see that this
function explicitly calls `np.array` on the given array object: `obj`, without
realising the type of `obj`. This implementation is obviously not generic to
support any array library other than numpy. We'll now apply the Array API's
`get_namespace` magic to make it generic, by adding a couple of lines to the code above:

```python
def getdata(obj, dtype=None, copy=False):
    """
    This is a wrapper of `np.array(obj, dtype=dtype, copy=copy)`
    that will generate a warning if the result is an object array.
    """
    xp, _ = get_namespace(obj)
    data = xp.asarray(obj, dtype=dtype)
    # Defer to getdtype for checking that the dtype is OK.
    # This is called for the validation only; we don't need
    # the return value.
    getdtype(data.dtype)
```

Now you can see that `get_namespace` finds the `array_api` module for the given
object and calls `.asarray` on it instead of `np.array` hence making it generic for
any array provider library that supports Array API standard

<p align="center">
    <img
     alt="Array API Workflow"
     src="/images/2022/02/array_api_workflow.svg">
    <i>Workflow for using Array API for writing code that works with multiple libraries</i>
</p>

#### Applying it on our demo example

Now let's take a look at the code for our demo example (segmentation of the
picture of greek coins in regions) to understand what it takes to make it run on GPU(s).

```python
# Author: Gael Varoquaux <gael.varoquaux@normalesup.org>, Brian Cheung
# License: BSD 3 clause

import time

import numpy as np
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt
import skimage
from skimage.data import coins
from skimage.transform import rescale

from sklearn.feature_extraction import image
from sklearn.cluster import spectral_clustering
from sklearn.utils.fixes import parse_version

# these were introduced in skimage-0.14
if parse_version(skimage.__version__) >= parse_version("0.14"):
    rescale_params = {"anti_aliasing": False, "multichannel": False}
else:
    rescale_params = {}

# load the coins as a numpy array
orig_coins = coins()

# Resize it to 20% of the original size to speed up the processing
# Applying a Gaussian filter for smoothing prior to down-scaling
# reduces aliasing artifacts.
smoothened_coins = gaussian_filter(orig_coins, sigma=2)
rescaled_coins = rescale(smoothened_coins, 0.2, mode="reflect", **rescale_params)

# Convert the image into a graph with the value of the gradient on the
# edges.
graph = image.img_to_graph(rescaled_coins)

# Take a decreasing function of the gradient: an exponential
# The smaller beta is, the more independent the segmentation is of the
# actual image. For beta=1, the segmentation is close to a voronoi
beta = 10
eps = 1e-6
graph.data = np.exp(-beta * graph.data / graph.data.std()) + eps

# Apply spectral clustering (this step goes much faster if you have pyamg
# installed)
N_REGIONS = 25

# Plotting
for assign_labels in ("kmeans", "discretize"):
    t0 = time.time()
    labels = spectral_clustering(
        graph, n_clusters=N_REGIONS, assign_labels=assign_labels, random_state=42
    )
    t1 = time.time()
    labels = labels.reshape(rescaled_coins.shape)

    plt.figure(figsize=(5, 5))
    plt.imshow(rescaled_coins, cmap=plt.cm.gray)
    for l in range(N_REGIONS):
        plt.contour(labels == l, colors=[plt.cm.nipy_spectral(l / float(N_REGIONS))])
    plt.xticks(())
    plt.yticks(())
    title = "Spectral clustering: %s, %.2fs" % (assign_labels, (t1 - t0))
    print(title)
    plt.title(title)
plt.show()
```

Let's walk through the code above to get a sense of what we're trying to achieve here.

- We have a dataset of greek coins from pompeii (imported from `skimage.data.coins`)
- We resize the image to 20% to speed up processing
- Convert the image to graph data structure
- Apply spectral clustering on the graph (via `kmeans` and `discretize` labelling).
- Plot the resulting clustering

Now to make it run on GPU we need to do bunch of minor changes in the code. Firstly
we need to use a different array input for GPU array. Since NumPy is a CPU only library
we'll use CuPy, which is a NumPy/SciPy-compatible array library for GPU-accelerated
computing with Python.

#### Changes to SciPy, scikit-learn, scikit-image, CuPy

Since SciPy, scikit-learn, scikit-image are designed mainly for NumPy, we need to use Array API
to dispatch to CuPy or NumPy based on the input. We do that by changing all the functions
that are called in the above demo to use `get_namespace` to replace all the instances of
`np.` (or `numpy.`) to properly dispatch to the appropriate array library. This is straightforward
at times and not so trivial at many. We'll see that in the challenges in next section.

The final code for the demo can be see [here](https://github.com/Quansight-Labs/amd-demo/blob/master/plot_coin_segmentation.ipynb).

## Challenges and Workarounds

At the moment Array API implements plenty of the commonly used functions from the NumPy API,
which makes it easier to replace the NumPy API functions with those, although there are a
bunch of rough edges, which makes the process a bit harder. These are the three main issues, we faced
in the process:

#### 1. Compiled code

There is a lot of functionality in SciPy and Scikits that is not pure
  Python, critical to performance parts are written using compiled code extensions. These parts
  are dependent on NumPy's internal memory representation, which makes them CPU only. This
  restricts the usage Array API to dispatch such code. There is another project `uarray`
  for dispatching compiled code, which needs to be used along with Array API dispatching to make
  it fully generic.

See for instance following piece of code:

```python
from scipy import sparse

graph = sparse.coo_matrix(<input_arrays>)
```

Here the `sparse.coo_matrix` is a compiled code extension in the `scipy.sparse` module. We need the 
dispatch to `cupyx.scipy.sparse.coo_matrix` for cupy arrays and `scipy.sparse.coo_matrix` for numpy
arrays. This is not possible with the Array API's dispatching via `get_namespace`. For this demo we have
added a workaround, until we have implemented the support for `uarray` based backed in SciPy. The
workaround looks something like this for cupy:

```python
xp, _ = get_namespace(<input_arrays>)

if xp.__name__ == 'cupy.array_api':
  from cupyx.scipy import sparse as cupy_sparse
  coo_matrix =  cupy_sparse.coo_matrix
else:
  coo_matrix = scipy.sparse.coo_matrix

graph = coo_matrix(<input_arrays>)
```

Note that, this workaround is only valid for NumPy/CuPy arrays.


#### 2. Not implemented functions

There are still a bunch of functions in the NumPy API which don't
have a direct equivalent in the Array API, either due to the fact that those functions are not
generic enough to be defined in the Array API or we haven't got around implementing those.

Some examples of unimplemented functions that we encountered during this excercise:


* `np.atleast_3d`
* `np.strides`
* `np.real`
* `np.clip`

#### 3. Inconsistencies with the NumPy API and Array API

Although the Array API has managed to
  get good coverage of the NumPy API, there are places where there are inconsistencies between
  the two, it could be either with the function parameters or behaviour or the function or name
  of the function like `concat` and `concatenate`.

* Naming inconsistency between NumPy API and Array API

```ipython

In [1]: import numpy as np
In [2]: import numpy.array_api as npx

# Numpy API
In [3]: np.concatenate
Out[3]: <function numpy.concatenate>

# Array API
In [4]: npx.concat
Out[4]: <function numpy.array_api._manipulation_functions.concat...>
```

* Indexing inconsistency between NumPy API and Array API

```ipython
In [1]: import numpy as np
In [2]: import numpy.array_api as npx

# Works with NumPy API
In [3]: x = np.arange(10)
In [4]: x[np.arange(2)]
Out[4]: array([0, 1])


# Doesn't Works with Array API
In [5]: z = npx.arange(10)
In [6]: z[npx.arange(2)]
-----------------------------------------------------------------
...
IndexError: Non-zero dimensional integer array indices are not allowed in the array API namespace
```

## Results

Here we will talk about about the performance of spectral clustering on GPU vs CPU

We ran this on AMD as well as NVIDIA GPUs and here is a plot of the performance.
The x-axis of the plot is the image dimension, i.e the dimension of the original
image after rescaling it to a certain proportion, for this demo rescaled the image
to 0.1, 0.2, 0.4, 0.6, 0.8 and 1x.


#### On AMD GPU:

![NumPy cs CuPy AMD](/images/2022/02/numpy_vs_cupy_amd.png)

The plot for AMD GPU is not what you would expect, the computation is faster
with numpy (i.e. on CPU) compared to cupy (i.e. on GPU) for all
image sizes, this is due to the slow device synchronization issue on AMD GPUs.


#### On NVIDIA GPU:

![NumPy cs CuPy NVIDIA](/images/2022/02/numpy_vs_cupy_nvidia.png)

This was ran on NVIDIA TITAN RTX. The plot for NVIDIA GPU is what you would
expect, the computation is faster with cupy (i.e. on GPU) compared to numpy
(i.e. on CPU) for non-trivial image size. This result is what you would expect.
The computation on GPU is slow for the image size less than **61 x 77**, this
is due to the overhead of moving things to the device (gpu) is significant
compared to the time taken for actual computation.

We expect the AMD result to be on similar lines to NVIDIA one, as soon as
the device synchronization issue is fixed.


### Running the analysis

The code and instructions to run the analysis above can be found in this repository:
[Quansight-Labs/array-api-gpu-demo](https://github.com/Quansight-Labs/array-api-gpu-demo).

The above analysis required changes in the following libraries:

- `cupy`
- `scipy`
- `scikit-learn`
- `scikit-image`

The changes are present in the `array-api-gpu-demo` branch of [@aktech](https://github.com/aktech)'s fork
of the above projects.

In the above mentioned repo, there is a docker image created for both platforms
NVIDIA & AMD. Running the demo is as simple as running

```bash
python segmentation_performance.py
```

Inside the docker container, which can be ran by:

```bash
docker run -it --device=/dev/kfd --device=/dev/dri --security-opt seccomp=unconfined --group-add video ghcr.io/quansight-labs/array-api-gpu-demo-rocm:latest bash
```


## Next Steps

At the moment we have only modified a bunch of functions to be able to run the
above mentioned demo on GPU. There is a whole bunch of functionality that can
eventually be ported to support Array API, which would make array provider
libraries like SciPy, scikit-learn, scikit-image fully compatible with multiple
array libraries.

## Acknowledgment

This project is part of a larger goal to make array consumer libraries to consume
more than just NumPy. In this excersise we have just tested the water, the accomplishment
of the larger goal would take significant effort and this would not have been possible
without the funding from Advanced Micro Devices, Inc. (AMD) and Quansight. Special thanks to
[Ivan Yashchuk](https://github.com/IvanYashchuk) and [Ralf Gommers](https://github.com/rgommers)
for their guidance throughout the project.

<p align="left">
    <img
     alt="AMD logo."
     src="/images/sponsors/AMD_E_Blk_RGB.png"
     width="250">
    <i></i>
</p>
