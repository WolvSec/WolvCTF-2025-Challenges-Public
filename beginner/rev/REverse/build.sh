#! /bin/sh
gcc reverse.c -o reverse
tar -czvf dist.tar.gz reverse out.txt
