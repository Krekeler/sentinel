#!/bin/bash
set -evx

mkdir ~/.dmscore

# safety check
if [ ! -f ~/.dmscore/.dms.conf ]; then
  cp share/dms.conf.example ~/.dmscore/dms.conf
fi
