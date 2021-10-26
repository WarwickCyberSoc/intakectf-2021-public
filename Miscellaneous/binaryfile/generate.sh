#!/bin/bash

dd if=/dev/urandom bs=15302 > binary_data.txt
echo "WMG{BinArY_FilES_RuIn_TermINalS}" >> binary_data.txt
dd if=/dev/urandom bs=9602 >> binary_data.txt
