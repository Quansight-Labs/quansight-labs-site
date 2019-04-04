# Quansight Labs Site

## Build information

- Built with [Lektor](https://www.getlektor.com)
- Theme based on https://github.com/Andrew-Shay/lektor-theme-simple-strap
- For blog posts from Jupyter notebooks: https://github.com/baldwint/lektor-jupyter

Lektor installs its own Python, pip and all its dependencies in a virtualenv in
a non-standard location:
```
$ cat `which lektor`
#!/usr/local/lib/lektor/bin/python
...
```

So to install dependencies that are needed, such as `nbconvert`, use
`/usr/local/lib/lektor/bin/python -m pip`.

## Deployment

`lektor build && lektor deploy` will push the static site to the `gh-pages` branch
of https://github.com/Quansight-Labs/quansight-labs-site. Note, this requires
Lektor to be installed.  **TODO**: hook this up to TravisCI, so a commit to master
deploys a new version automatically.