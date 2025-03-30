#!/bin/sh

rm -rf _dist_
mkdir -p _dist_

cp -r challenge/* _dist_

perl -pi -e s/wctf{[^}]+}/wctf{redacted-flag}/g _dist_/0.js
perl -pi -e s/wctf{[^}]+}/wctf{redacted-flag}/g _dist_/1.js
perl -pi -e s/wctf{[^}]+}/wctf{redacted-flag}/g _dist_/2.js
perl -pi -e s/wctf{[^}]+}/wctf{redacted-flag}/g _dist_/3.js
perl -pi -e s/wctf{[^}]+}/wctf{redacted-flag}/g _dist_/4.js

rm 0.tar.gz 1.tar.gz 2.tar.gz 3.tar.gz 4.tar.gz

tar -czvf 0.tar.gz -C _dist_ 0.js wasm.js package.json
tar -czvf 1.tar.gz -C _dist_ 1.js wasm.js package.json
tar -czvf 2.tar.gz -C _dist_ 2.js wasm.js package.json
tar -czvf 3.tar.gz -C _dist_ 3.js wasm.js package.json
tar -czvf 4.tar.gz -C _dist_ 4.js wasm.js package.json

rm -rf _dist_
ls -la *.tar.gz

