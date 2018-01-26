#!/bin/bash
set -evx

mkdir ~/.advanceprotocol

# safety check
if [ ! -f ~/.advanceprotocol/.advance.conf ]; then
  cp share/advance.conf.example ~/.advanceprotocol/advance.conf
fi
