FROM ubuntu:22.04

RUN apt update
RUN apt install curl -y


RUN curl https://github.com/foss-for-synopsys-dwc-arc-processors/toolchain/releases/download/arc-2024.12-release/arc_gnu_2024.12_prebuilt_elf32_be_linux_install.tar.xz -L -o install.tar.xz

RUN apt install xz-utils

RUN tar -xf /install.tar.xz

COPY decoder.c /

RUN /arceb-multilib-elf32/bin/arceb-elf32-gcc -mA6 /decoder.c -o decoder