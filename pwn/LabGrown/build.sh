#! /bin/sh
cd challenge
scuba build
tar -czvf ../dist.tar.gz chal labgrown.c Dockerfile 
