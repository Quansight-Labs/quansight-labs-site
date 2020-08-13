<!--
.. title: Introducing Versioned HDF5
.. slug: introducing-versioned-hdf5
.. date: 2020-08-12 14:37:29 UTC-05:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
-->


The problem of storing and manipulating large amounts of data is a challenge in many scientific computing and industry applications. One of the standard data models for this is [HDF5](https://support.hdfgroup.org/HDF5/whatishdf5.html), an open technology that implements a hierarchical structure (similar to a file-system structure) for storing large amounts of possibly heterogeneous data within a single file. Data in an HDF5 file is organized into *groups* and *datasets*; you can think about these as the folders and files in your local file system, respectively. You can also optionally store metadata associated with each item in a file, which makes this a self-describing and powerful data storage model.

![Hierarchical Data Format (HDF5) Dataset (From https://www.neonscience.org/about-hdf5)](https://www.neonscience.org/sites/default/files/images/HDF5/hdf5_structure4.jpg)

Since reading and writing operations in these large data files must be fast, the HDF5 model includes data compression and *chunking*. This technique allows the data to be retrieved in subsets that fit the computer's memory or RAM, which means that it doesn't require the entire file contents to be loaded into memory at once. All this makes HDF5 a popular format in several domains, and with [h5py](https://www.h5py.org) it is possible to use a Pythonic interface to read and write data to a HDF5 file. 

Now, let's say you have an HDF5 file with contents that change over time. You may want to add or remove datasets, change the contents of the data or the metadata, and keep a record of which changes occurred when, with a way to recover previous versions of this file. Since HDF5 is a binary file format, using regular version control tools (such as git) may prove difficult. 

Introducing the Versioned HDF5 library 
--------------------------------------

The Versioned HDF5 library is a versioned abstraction on top of h5py. Because of the flexibility of the HDF5 data model, all versioning data is stored in the file itself, which means that different versions of the same data (including version metadata) can be stored in a single HDF5 file. 

To see how this works in practice, let's say we create a regular HDF5 file with h5py called `mydata.h5`.

```py
    >>> import h5py
    >>> fileobject = h5py.File('mydata.h5', 'w')
```

Now, you can create a `VersionedHDF5file` object:

```py
    >>> from versioned_hdf5 import VersionedHDF5File
    >>> versioned_file = VersionedHDF5File(fileobject)
```

This file still doesn't have any data or versions stored in it. To create a new version, you can use a context manager:

```py
    >>> with versioned_file.stage_version('version1') as group:
    ...     group['mydataset'] = np.ones(10000)
```

The context manager returns a h5py group object, which should be modified in-place to build the new version. When the context manager exits, the version will be written to the file. This creates a `_version_data` group containing metadata associated with versions in the file:

```py
    >>> fileobject.keys()
    <KeysViewHDF5 ['_version_data']>
```

Now, the `versioned_file` object can be used to expose versioned data by version name:

```py
    >>> v1 = versioned_file['version1']
    >>> v1
    <Committed InMemoryGroup "/_version_data/versions/version1">
    >>> v1['mydataset']
    <InMemoryArrayDataset "mydataset": shape (10000,), type "<f8">
```

To access the actual data stored in version `version1`, we use the same syntax as h5py:

```py
    >>> dataset = v1['mydataset']
    >>> dataset[()]
    array([1., 1., 1., ..., 1., 1., 1.])
```

Current status
--------------

`versioned-hdf5 1.0` has recently been released, and is available on PyPI and conda-forge. You can install it with

```py
conda install -c conda-forge versioned-hdf5
```

The development is on [GitHub](https://github.com/deshaw/versioned-hdf5). Currently, the library supports basic use cases, but there is still a lot to do. We welcome community contributions to the library, including any issues or feature requests. 

For now, you can check out the [documentation](https://deshaw.github.io/versioned-hdf5/) for more details on what is supported and how the library is built.

Next steps
----------

This is the first post in a series about the Versioned HDF5 library. Next, we'll discuss the performance of Versioned HDF5 files, and the design of the library.

The Versioned HDF5 library was created by the [D. E. Shaw group](https://www.deshaw.com/) in conjunction with [Quansight](https://www.quansight.com/).

![https://www.deshaw.com](https://www.deshaw.com/assets/logos/black_logo_417x125.png)

