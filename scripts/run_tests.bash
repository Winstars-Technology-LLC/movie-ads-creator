#!/usr/bin/env bash

cd "${0%/*}/.." || exit
cd ..

echo "Running tests"
echo "............................"
echo "Failed!" && exit 1
