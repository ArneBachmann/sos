#!/bin/bash
sos diff --classic --only "$1" | colordiff ; echo Hit Enter to finish. ; read -n 1 -s