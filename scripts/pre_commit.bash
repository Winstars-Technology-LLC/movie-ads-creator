#!/usr/bin/env bash

./scripts/run_tests.bash

if [ $? -ne 0 ]; then
 echo "Tests must pass before commit!"
 exit 1
fi