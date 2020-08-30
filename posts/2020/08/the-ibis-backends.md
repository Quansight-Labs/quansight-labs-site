<!--
.. title: Querying multiple backends with ibis
.. slug: the-ibis-backends
.. date: 2020-08-30
.. author: Tony Fast, Kim Pevey
.. tags: Ibis, omnisci, sql, pandas
.. category: 
.. link: 
.. description: 
.. type: text
-->


# `ibis` as a generalized query tool for different backends

In [our most recent `ibis` post] we look at querying & retrieving data using a familiar `pandas`-like interface.
This example focused on the fluent API that `ibis` provides to query structure from a SQLite database, a single backend.
In this post, we'll explore `ibis`'s ability to answer questions about data using two different `ibis` backends.

```python
    import ibis.omniscidb, dask, intake, sqlalchemy, pandas, pyarrow as arrow, altair, h5py as hdf5
```


## `ibis` in the scientific Python ecosystem

Before we continue into the technical nitty-gritty of `ibis`, we'll consider `ibis` in the greater historical context of the scientific Python ecosystem. It was started by Wes McKinney, the creator of pandas, as way to query information on
the [Hadoop distributed file system][hdfs] and [pyspark]. Later more backends were added as `ibis` became a general tool for querying data.  

Throughout the rest of this document we'll highlight the ability of `ibis` to generically prescribe
query expressions across different data storage systems.

### The design of [`ibis` backends][backends]

Currently, `ibis` supports __>10__ backends.

```
>>> dir(ibis)
[...HDFS...WebHDFS...bigquery...clickhouse...hdf5...impala...omniscidb...pandas...pyspark...spark...sql...sqlite...]
```

A backend takes an `ibis` query expression and applies computation, _and the query is independent of the computation_.
A backend implementation, that can be queried with `ibis`, has one of the three following architectures.

1. Direct execution backends - `pandas` and `hdf5`.
2. Expression generating backends that create `sqlalchemy` expressions - `ibis.sql`.
3. String generating backends - `ibis.bigquery` and `ibis.omniscidb`

In the next few sections we'll unravel some of the different capabilities of each approach.

## A data-driven history of `ibis` compatibility

The table below looks at over 2000 issues in the ibis project.
It provides an annual summary of the issues tagged in `ibis`
for different backends over __6__ years.

|            | 2015   | 2016   | 2017   | 2018   | 2019   | 2020   |
|:-----------|:-------|:-------|:-------|:-------|:-------|:-------|
| omnisci    |        |        |        | 31.0   | 33.0   | 38.0   |
| spark      |        |        | 1.0    |        | 22.0   | 3.0    |
| postgres   | 2      | 3      | 21     | 10     | 17     | 4      |
| bigquery   |        |        | 15.0   | 71.0   | 12.0   | 2.0    |
| pandas     | 2.0    |        | 49.0   | 35.0   | 32.0   | 4.0    |
| sqlite     | 25     | 2      | 10     | 8      | 1      | 1      |
| impala     | 52     | 4      | 15     | 17     | 4      | 2      |
| kudu       |        |        |        |        |        | 1.0    |
| geospatial |        |        |        |        | 7.0    | 3.0    |
| clickhouse |        |        | 8.0    | 9.0    | 1.0    | 4.0    |
| mysql      |        |        |        | 2.0    | 2.0    | 4.0    |
| sqlalchemy | 17.0   | 3.0    | 10.0   | 2.0    | 5.0    |        |


We note an early focus `ibis.sqlite`, `sqlalchemy` and `ibis.impala`. 
Later, work began on the `pandas` backend rounding out the three different types of backgrounds.
From this point, improvements were made to these key backends as `ibis.clickhouse`, `ibis.spark` and `ibis.postgres`. 
For the past 2 years, Quansight, in partnership with OmniSci, added the `ibis.omniscidb`
string generating backend. Further, our responsibilities have expanded
to support `ibis` as community maintainers through Quansight Labs. 
This collaboration introduced geospatial functionality to `ibis` for several backends.

### Currently, there is an ongoing effort to add sqlserver backends

There are on going efforts to introduce [SQL Server][sql-server] support.  
What other backends would you like to see for `ibis`?
Maybe our community could benefit from a `dask` backend or `altair` backend?

## `ibis` direct execution backends

`ibis` direct execution backends like `pandas` and `hdf5` operate on conventional in-memory python objects.
`pandas` is the gold standard for structured data in python, and inspires the API for `ibis`.


```python
pd = ibis.pandas.connect({'A': pandas.util.testing.makeDataFrame()})
```

`pd` is an `ibis` backend based off `pandas.DataFrame` objects.

```python
expression = pd.table('A').head()
```

`expression` is an `ibis` query, that has `expression.compile` and `expression.execute` methods.
We'll recognize the __execute__ method when we return `pandas.DataFrame`s from `ibis` expression.
The __compile__ method does not trigger any computation, rather it constructs an intermediate form
that is interpretted by a backend.

```python
    >>> assert isinstance(expression.compile(), ibis.expr.types.TableExpr)
```

In the case of direction execution backends, the `expression` compiles to an the original `ibis` 
expression.  And the computation is carried out based on a set of recipes defined in `ibis`.

In general, we would typically do this work directly in `pandas`, however this work is
practical in mocking tests for expressions independent of backends.

> Learn more about the [HDF5 direct execution backend in the `ibis` tests][test-hdf5].

## `ibis` expression generating backends.

```python
db = ibis.sqlite.connect('lahmansbaseballdb.sqlite')
expression = db.table('halloffame').head()
```

Expression generating backends operate on [SQL] databases that interoperate with `sqlalchemy`.

```python
>>> assert isinstance(expression.compile(), sqlalchemy.sql.Select)
```

In the case of expression generating backends, the intermediate representation is a `sqlalchemy` object.
`sqlalchemy` is _The Database Toolkit for Python_, and `ibis` leverages it compatibility
with traditional [SQL] databases.
    


## `ibis` string generating backends.

There are two options for downloading `ibis`

1. Using `pip` we'll need to request the extra backends from `ibis`.

    ```bash
    pip install --upgrade ibis-framework[omniscidb] ibis-framework[sqlite]
    ```

2. `conda` will download all of the supported [backends] meaning you'll have the packages
required to work across sql, pandas, [bigquery], or [Omnisci].

    ```bash
    conda install -c conda-forge ibis-framework # install all the backends!
    ```

String generating backends allow `ibis` to interface with big data systems that manage 
their own computation. For example, we may connect to an example `omnisci` database.
    

```python
import ibis.omniscidb
omnisci = ibis.omniscidb.connect(host='metis.omnisci.com', 
                                user='demouser', 
                                password='HyperInteractive', 
                                port=443, 
                                database='omnisci', 
                                protocol='https')
```
    
`omnisci` is described as a string generating backend because the intermediate representation of the
query is a flavor of SQL.


```python
expression = omnisci.table('upstream_reservoir').head()
```

    
A string generating expression compiles to `ibis.omniscidb` flavored [SQL], while `ibis.bigquery` may have a different string representation.


```python
>>> expression.compile()
'SELECT *\nFROM upstream_reservoir\nLIMIT 5'
```
    

> Major credit goes to [@xmnlab] in his heroic PR to introduce `ibis.omniscidb` into `ibis`. You can watch
the drama play out in this [Github Issue][omnisci-pr]. If you'd like to learn more about [OmniSci] and
`ibis.omniscidb` checkout the following links.
> * [OmniSci][omnisci]
> * [Quansight Labs- Ibis: Python data analysis productivity framework][labs-post]

## Conclusion

We'd like to thank the maintainers of the Ibis for
their and effort in supporting the Ibis community.


[our most recent `ibis` post]: https://labs.quansight.org/blog/2020/06/ibis-an-idiomatic-flavor-of-sql-for-python-programmers/
[ibis]: https://www.ibis-project.org/
[SQL]: https://en.wikipedia.org/wiki/SQL
[Python]: https://en.wikipedia.org/wiki/Python_(programming_language)
[flavor of sql]: https://stackoverflow.com/questions/1326318/difference-between-different-types-of-sql
[design]: https://docs.ibis-project.org/design.html
[sqlite]: https://www.sqlite.org/index.html
[pandas]: http://pandas.pydata.org/
[omnisci]: https://www.omnisci.com/
[glue]: https://docs.scipy.org/doc/numpy/user/c-info.python-as-glue.html
[dask]: https://dask.org/
[flavor of sql]: https://stackoverflow.com/questions/1326318/difference-between-different-types-of-sql
[dag]: https://en.wikipedia.org/wiki/Directed_acyclic_graph
[data]: http://www.seanlahman.com/baseball-archive/statistics/    
[database connection]: https://en.wikipedia.org/wiki/Database_connection
[tidy data]: https://vita.had.co.nz/papers/tidy-data.pdf
[openteams]: https://openteams.com/
[contributing]: https://docs.ibis-project.org/contributing.html
[qs]: https://www.quansight.com/
[graphviz]: https://graphviz.org
[materialized view]: https://en.wikipedia.org/wiki/Materialized_view
[blaze]: https://blaze.pydata.org/
[sqlalchemy]: https://www.sqlalchemy.org/
[backends]: https://ibis-project.org/docs/backends/index.html
[intake]: https://intake.readthedocs.io/en/latest/
[arrow]: https://arrow.apache.org/docs/python/
[labs-post]: https://labs.quansight.org/blog/2019/07/ibis-python-data-analysis-productivity-framework/
[geo-tutorial]: https://github.com/ibis-project/ibis/pull/1991
[geo-closed]: https://github.com/ibis-project/ibis/issues?q=label%3Ageospatial+is%3Aclosed
[sql-server]: https://github.com/ibis-project/ibis/pull/1997
[omnisci-pr]: https://github.com/ibis-project/ibis/pull/1419
[test-hdf5]: https://github.com/ibis-project/ibis/blob/master/ibis/file/tests/test_hdf5.py
[@xmnlab]: https://github.com/xmnlab
[hdfs]: https://en.wikipedia.org/wiki/Apache_Hadoop#HDFS
[pyspark]: https://pypi.org/project/pyspark/
[bigquery]: https://cloud.google.com/bigquery/