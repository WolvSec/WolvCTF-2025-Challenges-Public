#!/bin/bash
cd challenge
cd build_container
docker build -t gcc-libseccomp .
scuba build 
docker image rm gcc-libseccomp
cp chal ../ 
cd ../../ 
cp challenge/chal healthcheck/chal 
tar -czf dist.tar.gz challenge/chal challenge/Dockerfile
