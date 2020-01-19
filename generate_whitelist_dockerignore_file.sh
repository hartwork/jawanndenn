#! /bin/bash
# Copyright (C) 2020 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU GPL v3 or later

cat <<EOF
##################################################################################
## THIS FILE WAS GENERATED -- DO NOT EDIT!
##
## In order to get .dockerignore back in sync, run:
##   ./generate_whitelist_dockerignore_file.sh > .dockerignore
##################################################################################

# Ignore everything
*

# Unignore files based on "git ls-files"
EOF

git ls-files \
        | sed -r \
            -e 's,(^|/)[^.][^/]*(\.[^/]+)$,\1*\2,' \
            -e '/(^|\/)\./d' \
        | sort -u -V \
        | sort -V -f \
        | sed 's,^,!,'
