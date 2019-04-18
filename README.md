# Quansight Labs Site

## Build information

To set up a development environment: in a new conda env or virtualenv:
```
$ pip install nikola
$ nikola theme -i maupassant
```

Configuration file for the site is ``conf.py``.

To build the site::

    nikola build

To see it::

    nikola serve -b

To check all available commands::

    nikola help

## Deployment

Submit pull requests first, those get run on CircleCI where the new site can be checked (stored in `Artifacts`). On merge the site will get deployed to labs.quansight.org