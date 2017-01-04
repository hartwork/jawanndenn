What is jawanndenn?
===================

.. figure:: https://raw.githubusercontent.com/hartwork/jawanndenn/master/jawanndenn-setup.png
   :alt: Screenshot of poll creation in jawanndenn

*jawanndenn* is a simple web application to schedule meetings and run
polls, a libre alternative to Doodle. It is written in Python and
JavaScript using

-  `bottle`_ with `Paste`_ for a default backend
-  `jQuery`_ 
-  `jQuery noty`_
-  `Materialize`_ Material Design CSS/JS

*jawanndenn* is `libre software`_ developed by `Sebastian Pipping`_. The
server code is licensed under the `GNU Affero GPL license`_ version 3
or later whereas the client code is licensed under the `GNU GPL
license`_ version 3 or later.

Please `report bugs`_ and let me know if you `like`_ it.


Installation
============

To install the latest release without cloning the Git repository:

::

    # pip install jawanndenn

To install from a Git clone:

::

    # python setup.py install --user


Deployment with Apache mod\_wsgi
================================

To use *jawanndenn* with ``mod_wsgi``, there is file
``jawanndenn/app.wsgi`` For how to integrate ``jawanndenn/app.wsgi``
with the Apache configuration, please check the `the related
documentation of bottle`_.

Feel free to `file a support ticket`_ or `drop me a mail`_, if you
cannot get it to work.


Command line usage
==================

When installed, invocation is as simple as

::

    # jawanndenn

During development, you may want to run *jawanndenn* from the Git clone
using

::

    # PYTHONPATH=. python jawanndenn/main.py --debug

Currently supported arguments are:

::

    # jawanndenn --help
    usage: jawanndenn [-h] [--debug] [--host HOST] [--port PORT]
                      [--server BACKEND] [--max-polls COUNT]
                      [--max-votes-per-poll COUNT]

    optional arguments:
      -h, --help            show this help message and exit
      --debug               Enable debug mode (default: disabled)
      --host HOST           Hostname or IP address to listen at (default:
                            127.0.0.1)
      --port PORT           Port to listen at (default: 8080)
      --server BACKEND      bottle backend to use (default: paste); as of this
                            writing bottle supports: auto, bjoern, cgi, cherrypy,
                            diesel, eventlet, fapws3, flup, gae, gevent, gunicorn,
                            meinheld, rocket, tornado, twisted, waitress, wsgiref.
                            For the most current list, please check the
                            documentation of bottle.

    limit configuration:
      --max-polls COUNT     Maximum number of polls total (default: 100)
      --max-votes-per-poll COUNT
                            Maximum number of votes per poll (default: 40)


Goals
=====

-  Libre software to host yourself, unlike Doodle
-  More simple, sexy and fun than `libre alternatives`_:

   -  `Pleft`_
   -  `Framadata`_ (`Sources`_, ex. OpenSondage, ex. STUdS)
   -  `Foodle`_ (`on GitHub`_, ex. `DFN scheduler`_, ex. `DFN Terminplaner+`_)
   -  `Dudle`_
   -  `Nuages`_
   -  `RDVz`_
   -  (`Drupal Date picker formatter`_)
   -  `Noodle`_

-  Keep things simple, usable, maintainable
-  Support invocation from the command line, e.g. for spontaneous polls in a LAN
-  Have security in mind

Please check out the `list of upcoming features`_.


Non-goals
=========

-  Use of heavy frameworks: building blocks only
-  Read availability from calendars

.. _bottle: http://bottlepy.org/docs/dev/
.. _Paste: http://pythonpaste.org/
.. _jQuery: http://jquery.com/
.. _jQuery noty: http://ned.im/noty/#/about
.. _Materialize: http://materializecss.com/
.. _libre software: https://www.gnu.org/philosophy/free-sw.en.html
.. _Sebastian Pipping: https://blog.hartwork.org/
.. _GNU Affero GPL license: https://www.gnu.org/licenses/agpl.en.html
.. _GNU GPL license: https://www.gnu.org/licenses/gpl.html
.. _report bugs: https://github.com/hartwork/jawanndenn/issues
.. _like: mailto:sebastian@pipping.org
.. _the related documentation of bottle: https://bottlepy.org/docs/dev/deployment.html#apache-mod-wsgi
.. _file a support ticket: https://github.com/hartwork/jawanndenn/issues/new
.. _drop me a mail: mailto:sebastian@pipping.org
.. _libre alternatives: http://alternativeto.net/software/doodle/?license=opensource
.. _Pleft: https://github.com/sander/pleft
.. _Framadata: https://framadate.org/
.. _Sources: https://git.framasoft.org/framasoft/framadate
.. _Foodle: https://foodl.org/
.. _on GitHub: https://github.com/UNINETT/Foodle
.. _DFN scheduler: https://terminplaner.dfn.de/
.. _DFN Terminplaner+: https://terminplaner2.dfn.de/
.. _Dudle: https://dudle.inf.tu-dresden.de/
.. _Nuages: https://nuages.domainepublic.net/
.. _RDVz: https://sourceforge.net/projects/rdvz/
.. _Drupal Date picker formatter: http://alternativeto.net/software/date-picker-formatter-dudel-for-drupal/?license=opensource
.. _Noodle: https://github.com/kmerz/noodle
.. _list of upcoming features: https://github.com/hartwork/jawanndenn/issues/created_by/hartwork
