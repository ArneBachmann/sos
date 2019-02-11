#!/bin/bash
sos offline --strict --progress && sos config useChangesCommand on --quiet ; echo Hit Enter to finish. ; read -n 1 -s