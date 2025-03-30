#!/bin/bash
cd challenge
scuba build
cd ..
cp challenge/chal healthcheck/chal
tar -czf dist.tar.gz challenge/chal challenge/Dockerfile
