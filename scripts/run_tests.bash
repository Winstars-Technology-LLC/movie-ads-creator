#!/usr/bin/env bash

cd "${0%/*}/.." || exit
cd ..

python test_movie_creator.py

