```python
    import ibis.omniscidb, dask, intake, sqlalchemy, pandas, pyarrow as arrow, altair, h5py as hdf5
```

<!-- END_TEASER -->

<!--    

 
-->

# `ibis` as a generalized query tool for different backends

In [our most recent `ibis` post] we look at querying & retrieving data using a familiar `pandas`-like interface.
This example focused on the fluent API that `ibis` provides to query structure from a SQLite database, a single backend.
In this post, we'll explore `ibis`'s ability to answer questions about data using two different `ibis` backends.

## `ibis` in the scientific Python ecosystem

Before we continue into the technical nitty-gritty of `ibis`, we'll consider `ibis` in the greater historical context of the scientific Python ecosystem.

The design of quite a few high-level tools in the scientific Python world can be tracked back to the holistic `blaze` ecosystem that offered ways _**store, describe, query, and process**_ data.
`blaze` had ambitious goals and is now defunct, but its influences resonate throughout
the scientific python community development in the success of projects the focus specific features of a data ecosystem like:

* `dask` processing data.
* `intake` for describing data.
* `ibis` for querying data.

Throughout the rest of this document we'll highlight the ability of `ibis` to generically prescribe
query expressions across different data storage systems.

### The design of [`ibis` backends][backends]

Currently, `ibis` supports __>10__ backends.

    >>> dir(ibis)
    [...HDFS...WebHDFS...bigquery...clickhouse...hdf5...impala...omniscidb...pandas...pyspark...spark...sql...sqlite...]

A backend takes an `ibis` query expression and applies computation, _and the query is independent of the computation_.
A backend implementation, that can be queried with `ibis`, has one of the three following architectures.

1. Direct execution backends - `pandas` and `hdf5`.
2. Expression generating backends that create `sqlalchemy` expressions - `ibis.sql`.
3. String generating backends - `ibis.bigquery` and `ibis.omniscidb`

In the next few sections we'll unravel some of the different capabilities of each approach.

## A data-driven history of `ibis` compatability

The table below looks at over 2000 issues in the ibis project.
It provides an annual summary of the issues tagged in `ibis`
for different backends over __6__ years.

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>omnisci</th>
      <th>spark</th>
      <th>postgres</th>
      <th>bigquery</th>
      <th>pandas</th>
      <th>sqlite</th>
      <th>impala</th>
      <th>kudu</th>
      <th>geospatial</th>
      <th>clickhouse</th>
      <th>mysql</th>
      <th>sqlalchemy</th>
    </tr>
    <tr>
      <th>year</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2015</th>
      <td></td>
      <td></td>
      <td>2</td>
      <td></td>
      <td>2</td>
      <td>25</td>
      <td>52</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>17</td>
    </tr>
    <tr>
      <th>2016</th>
      <td></td>
      <td></td>
      <td>3</td>
      <td></td>
      <td></td>
      <td>2</td>
      <td>4</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>3</td>
    </tr>
    <tr>
      <th>2017</th>
      <td></td>
      <td>1</td>
      <td>21</td>
      <td>15</td>
      <td>49</td>
      <td>10</td>
      <td>15</td>
      <td></td>
      <td></td>
      <td>8</td>
      <td></td>
      <td>10</td>
    </tr>
    <tr>
      <th>2018</th>
      <td>31</td>
      <td></td>
      <td>10</td>
      <td>71</td>
      <td>35</td>
      <td>8</td>
      <td>17</td>
      <td></td>
      <td></td>
      <td>9</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2019</th>
      <td>33</td>
      <td>22</td>
      <td>17</td>
      <td>12</td>
      <td>32</td>
      <td>1</td>
      <td>4</td>
      <td></td>
      <td>7</td>
      <td>1</td>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2020</th>
      <td>38</td>
      <td>3</td>
      <td>4</td>
      <td>2</td>
      <td>4</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>3</td>
      <td>4</td>
      <td>4</td>
      <td></td>
    </tr>
  </tbody>ibis direct execution backends like pandas and hdf5 operate on conventional in-memory python objects. pandas is the gold standard for structured data in python, and inspires the API for ibis.


</table>
</div>
<br>

> We note an early focus `ibis.sqlite, sqlalchemy and ibis.impala`. 
Later, work began on the `pandas` backend rounding out the three different types of backgrounds.
From this point, improvements were made to these key backends as `ibis.clickhouse`, `ibis.spark` and `ibis.postgres`. 
For the past 3 years, Quansight, in partnership with OmniSci, added the `ibis.omniscidb`
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

`pd` is an `ibis` backend based off `pandibis direct execution backends like pandas and hdf5 operate on conventional in-memory python objects. pandas is the gold standard for structured data in python, and inspires the API for ibis.

as.DataFrame` objects.

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
`sqlalchemy` is _The Database Toolkit for Python_, and `ibis` leverages it compatability
with traditional [SQL] databases.
    


## `ibis` string generating backends.

```bash
pip install --upgrade ibis-framework[omniscidb]
# ORx
conda install -c conda-forge ibis-framework # install all the backends!
```

String generating backends allow `ibis` to interface with big data systems that manage 
their own computation. For example, we may connect to an example `omnisci` database.
    

```python
    import ibis.omniscidb
    omnisci = ibis.omniscidb.connect(host='metis.omnisci.com', user='demouser', password='HyperInteractive', port=443, database='omnisci', protocol='https')
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

We'd like to thank the maintainers of the `ibis` for
their and effort in supporting the `ibis` community.


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
[blaze]: #
[sqlalchemy]: #
[backends]: #
[intake]: #
[arrow]: #
[labs-post]: https://labs.quansight.org/blog/2019/07/ibis-python-data-analysis-productivity-framework/
[geo-tutorial]: https://github.com/ibis-project/ibis/pull/1991
[geo-closed]: https://github.com/ibis-project/ibis/issues?q=label%3Ageospatial+is%3Aclosed
[sql-server]: https://github.com/ibis-project/ibis/pull/1997
[omnisci-pr]: https://github.com/ibis-project/ibis/pull/1419
[test-hdf5]: https://github.com/ibis-project/ibis/blob/master/ibis/file/tests/test_hdf5.py
[@xmnlab]: https://github.com/xmnlab
