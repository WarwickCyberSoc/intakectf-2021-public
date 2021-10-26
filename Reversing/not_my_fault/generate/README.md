# Requirements

Installing on Ubuntu:

```bash
sudo apt update
sudo apt install make python3 python3-pip nasm binutils
pip3 install pwntools
```

# Building

- Modify `flag` in `structure.py` (the value must be 32 bytes).
- Run `make release`.
- Distribute `main`.