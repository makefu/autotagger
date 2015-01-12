#!/bin/sh
# simple e2e test of single_tag

cd "$(dirname "$(readlink -f "$0")")"/..
tmpdb=$(mktemp)

trap "rm -f $tmpdb" INT TERM EXIT

#python autotagger/recurse_autotag.py -t tmsu --db "$tmpdb" 
python autotagger/single_tag.py -t tmsu --db "$tmpdb" tests/tagfiles/this-file-does-not-exist
if tmsu -D "$tmpdb" tags tests/tagfiles/this-file-does-not-exist \
  | grep -q  poor-bastard ;then
  echo "success"
  exit 0
else
  echo "fail"
  exit 0
fi

