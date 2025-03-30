FROM gcr.io/kctf-docker/healthcheck@sha256:6709709a8cfd6e2d743c86d58398c00ca4eb26befd3b1a0a629ab35f91e98ef0


COPY healthcheck_loop.sh healthcheck.py healthz_webserver.py /home/user/
COPY chal /challenge/chal
COPY --from=ubuntu:20.04 /lib/x86_64-linux-gnu/libc.so.6 /challenge/libc.so.6


RUN apt-get update && apt-get install -y python3-pip && pip3 install pwntools


CMD kctf_drop_privs /home/user/healthcheck_loop.sh & /home/user/healthz_webserver.py

