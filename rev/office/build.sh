#! /bin/bash
cd challenge
scuba build
cp chal ../healthcheck/
cp flag.txt ../healthcheck
tar -czvf ../dist.tar.gz chal

