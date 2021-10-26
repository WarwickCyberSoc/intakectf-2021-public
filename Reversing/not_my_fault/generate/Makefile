debug:
	python3 structure.py --debug
	nasm -f elf64 -g -F dwarf main.asm
	ld -o main main.o

release:
	python3 structure.py
	nasm -f elf64 main.asm
	ld -s -o main main.o

clean:
	rm main.o structure.asm structure_code.asm
