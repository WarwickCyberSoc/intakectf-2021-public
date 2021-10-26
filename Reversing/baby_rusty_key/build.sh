#!/bin/bash
export LITCRYPT_ENCRYPT_KEY=$(hexdump -n 32 -e '"%08X"' /dev/urandom) \
&& RUSTFLAGS='-C target-feature=+crt-static' cargo build --release --target x86_64-unknown-linux-gnu \
&& mkdir release 2>/dev/null \
&& cp target/x86_64-unknown-linux-gnu/release/baby_rusty_key release \
&& strip -w -K \!'*menu*' -K '*' release/baby_rusty_key \
&& strip -w -K \!'*litcrypt*' -K '*' release/baby_rusty_key \
&& echo 'DONE'