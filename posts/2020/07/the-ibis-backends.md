<!-- END_TEASER -->

<!--    

 
-->

# `ibis` as a generalized query tool for different backends.

In [our most recent `ibis` post] we look at querying & retrieving data using a familiar `pandas`-like interface.
This example focused on the fluent API that `ibis` provides to query structure from a SQLite database, a single backend.
In this post, we'll explore `ibis`'s ability to answer questions about data using two different `ibis` backends.

## `ibis` in the scientific Python ecosystem.

Before we continue into the technical nitty-gritty of `ibis`, we'll consider `ibis` in the greater historical context of the scientific Python ecosystem.

The design of quite a few high-level tools in the scientific Python world can be tracked back to the holistic `blaze` ecosystem that offered ways _**store, describe, query, and process**_ data.
`blaze` had ambitious goals and is now defunct, but its influences resonate throughout
the scientific python community development in the success of projects the focus specific features of a data ecosystem like:

* `dask` processing data.
* `intake` for describing data.
* `ibis` for querying data.

Throughout the rest of this document we'll highlight the ability of `ibis` to generically prescribe
query expressions across different data storage systems.

### The design of [`ibis` backends][backends].

Currently, `ibis` supports __>10__ backends.
    
    >>> dir(ibis)
    [...HDFS...WebHDFS...bigquery...clickhouse...hdf5...impala...omniscidb...pandas...pyspark...spark...sql...sqlite...]
    
A backend takes an `ibis` query expression and applies computation, _and the query is independent of the computation_.
A backend implementation, that can be queried with `ibis`, has one of the three following architectures.

1. Direct execution backends - `pandas and hdf5`. 
2. Expression generating backends that create `sqlalchemy` expressions - `ibis.sql`.
3. String generating backends - `ibis.bigquery and ibis.omniscidb`

In the next few sections we'll unravel some of the different capabilities of each approach.


## A data-driven history of `ibis` compatability.

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
  </tbody>
</table>
</div>


> We note an early focus `ibis.sqlite, sqlalchemy and ibis.impala`. 
Later, work began on the `pandas` backend rounding out the three different types of backgrounds.
From this point, improvements were made to these key backends as `ibis.clickhouse`, `ibis.spark` and `ibis.postgres`. 
For the past 3 years, Quansight, in partnership with OmniSci, added the `ibis.omniscidb`
string generating backend. Since Quansight Labs has taken on a role as a community maintainer 
for `ibis`. This collaboration introduced geospatial functionality to `ibis`, and we 
have on going efforts to introduce [SQL Server][sql-server] support

### Currently, there is an ongoing effort to add sqlserver backends. 

Leave a comment the backends what you like to see? `dask`? `altair`?

## `ibis` direct execution.

`ibis` direct execution backends like `pandas and hdf5` operate on conventional in-memory python objects.
`pandas` is the gold standard for structured data in python, and inspires the api for `ibis`.

`pd` is an `ibis` backend based off `pandas.DataFrame` objects.

`expression` is an `ibis` query, that has `expression.compile` and `expression.execute` methods.
We'll recognize the __execute__ method when we return `pandas.DataFrame`s from `ibis` expression.
The __compile__ method does not trigger any computation, rather it constructs an intermediate form
that is interpretted by a backend.

In the case of direction execution backends, the `expression` compiles to an the original `ibis` 
expression.  And the computation is carried out based on a set of recipes defined in `ibis`.

In general, we would typically do this work directly in `pandas`, however this work is
practical in mocking tests for expressions independent of backends.

> Learn more about the [HDF5 direct execution backend in the `ibis` tests][test-hdf5].

## `ibis` expression generating backends.

Expression generating backends operate on [SQL] databases that interoperator with `sqlalchemy`.

    
In the case of expression generating backends, the intermediate representation is a `sqlalchemy` object.
`sqlalchemy` is _The Database Toolkit for Python_, and `ibis` leverages it compatability
with traditional [SQL] databases.
    


## `ibis` string generating backends.

```bash
pip install --upgrade ibis-framework[omniscidb]
```

String generating backends allow `ibis` to interface with big data systems that manage 
their own computation. For example, we may connect to an example `omnisci` database.
    

    
`omnisci` is described as a string generating backend because the intermediate representation of the
query is a flavor of SQL.

    
A string generating expression compiles to `ibis.omniscidb` flavored [SQL], while `ibis.bigquery` may have a different string representatin.




    'SELECT *\nFROM upstream_reservoir\nLIMIT 5'



> Major credit goes to [@xmnlab] in his heroic PR to introduce `ibis.omniscidb` into `ibis`. You can watch
the drama play out in this [Github Issue][omnisci-pr]. If you'd like to learn more about [OmniSci] and
`ibis.omniscidb` checkout the following links.
> * [OmniSci][omnisci]
> * [Quansight Labs- Ibis: Python data analysis productivity framework][labs-post]

## Conclusion

We'd like to thank the maintainers of the `ibis` for
their and effort in supporting the `ibis` community.

<!--

    [NbConvertApp] WARNING | pattern 'pythonic-queries-in-ibis.ipynb' matched no files
    This application is used to convert notebook files (*.ipynb) to various other
    formats.
    
    WARNING: THE COMMANDLINE INTERFACE MAY CHANGE IN FUTURE RELEASES.
    
    Options
    -------
    
    Arguments that take values are actually convenience aliases to full
    Configurables, whose aliases are listed on the help line. For more information
    on full configurables, see '--help-all'.
    
    --debug
        set log level to logging.DEBUG (maximize logging output)
    --generate-config
        generate default config file
    -y
        Answer yes to any questions instead of prompting.
    --execute
        Execute the notebook prior to export.
    --allow-errors
        Continue notebook execution even if one of the cells throws an error and include the error message in the cell output (the default behaviour is to abort conversion). This flag is only relevant if '--execute' was specified, too.
    --stdin
        read a single notebook file from stdin. Write the resulting notebook with default basename 'notebook.*'
    --stdout
        Write notebook output to stdout instead of files.
    --inplace
        Run nbconvert in place, overwriting the existing notebook (only 
        relevant when converting to notebook format)
    --clear-output
        Clear output of current file and save in place, 
        overwriting the existing notebook.
    --no-prompt
        Exclude input and output prompts from converted document.
    --no-input
        Exclude input cells and output prompts from converted document. 
        This mode is ideal for generating code-free reports.
    --log-level=<Enum> (Application.log_level)
        Default: 30
        Choices: (0, 10, 20, 30, 40, 50, 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL')
        Set the log level by value or name.
    --config=<Unicode> (JupyterApp.config_file)
        Default: ''
        Full path of a config file.
    --to=<Unicode> (NbConvertApp.export_format)
        Default: 'html'
        The export format to be used, either one of the built-in formats
        ['asciidoc', 'custom', 'html', 'latex', 'markdown', 'notebook', 'pdf',
        'python', 'rst', 'script', 'slides'] or a dotted object name that represents
        the import path for an `Exporter` class
    --template=<Unicode> (TemplateExporter.template_file)
        Default: ''
        Name of the template file to use
    --writer=<DottedObjectName> (NbConvertApp.writer_class)
        Default: 'FilesWriter'
        Writer class used to write the  results of the conversion
    --post=<DottedOrNone> (NbConvertApp.postprocessor_class)
        Default: ''
        PostProcessor class used to write the results of the conversion
    --output=<Unicode> (NbConvertApp.output_base)
        Default: ''
        overwrite base name use for output files. can only be used when converting
        one notebook at a time.
    --output-dir=<Unicode> (FilesWriter.build_directory)
        Default: ''
        Directory to write output(s) to. Defaults to output to the directory of each
        notebook. To recover previous default behaviour (outputting to the current
        working directory) use . as the flag value.
    --reveal-prefix=<Unicode> (SlidesExporter.reveal_url_prefix)
        Default: ''
        The URL prefix for reveal.js (version 3.x). This defaults to the reveal CDN,
        but can be any url pointing to a copy  of reveal.js.
        For speaker notes to work, this must be a relative path to a local  copy of
        reveal.js: e.g., "reveal.js".
        If a relative path is given, it must be a subdirectory of the current
        directory (from which the server is run).
        See the usage documentation
        (https://nbconvert.readthedocs.io/en/latest/usage.html#reveal-js-html-
        slideshow) for more details.
    --nbformat=<Enum> (NotebookExporter.nbformat_version)
        Default: 4
        Choices: [1, 2, 3, 4]
        The nbformat version to write. Use this to downgrade notebooks.
    
    To see all available configurables, use `--help-all`
    
    Examples
    --------
    
        The simplest way to use nbconvert is
        
        > jupyter nbconvert mynotebook.ipynb
        
        which will convert mynotebook.ipynb to the default format (probably HTML).
        
        You can specify the export format with `--to`.
        Options include ['asciidoc', 'custom', 'html', 'latex', 'markdown', 'notebook', 'pdf', 'python', 'rst', 'script', 'slides'].
        
        > jupyter nbconvert --to latex mynotebook.ipynb
        
        Both HTML and LaTeX support multiple output templates. LaTeX includes
        'base', 'article' and 'report'.  HTML includes 'basic' and 'full'. You
        can specify the flavor of the format used.
        
        > jupyter nbconvert --to html --template basic mynotebook.ipynb
        
        You can also pipe the output to stdout, rather than a file
        
        > jupyter nbconvert mynotebook.ipynb --stdout
        
        PDF is generated via latex
        
        > jupyter nbconvert mynotebook.ipynb --to pdf
        
        You can get (and serve) a Reveal.js-powered slideshow
        
        > jupyter nbconvert myslides.ipynb --to slides --post serve
        
        Multiple notebooks can be given at the command line in a couple of 
        different ways:
        
        > jupyter nbconvert notebook*.ipynb
        > jupyter nbconvert notebook1.ipynb notebook2.ipynb
        
        or you can specify the notebooks list in a config file, containing::
        
            c.NbConvertApp.notebooks = ["my_notebook.ipynb"]
        
        > jupyter nbconvert --config mycfg.py
    


-->
