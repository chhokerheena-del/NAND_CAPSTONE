#!/usr/bin/env python3
"""
Hack assembler (Nand to Tetris) - Roll 2501730399, K = 99
K mod 3 = 0  ->  extra feature: write all labels & variables with addresses to symbols.txt

Usage:  python assembler.py Prog.asm        (creates Prog.hack and symbols.txt)
"""
import sys

DEST = {"": "000", "M": "001", "D": "010", "MD": "011", "A": "100",
        "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100",
    "A": "0110000", "!D": "0001101", "!A": "0110001", "-D": "0001111",
    "-A": "0110011", "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011", "A-D": "0000111",
    "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011", "M+1": "1110111",
    "M-1": "1110010", "D+M": "1000010", "D-M": "1010011", "M-D": "1000111",
    "D&M": "1000000", "D|M": "1010101",
}


def predefined():
    t = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
         "SCREEN": 16384, "KBD": 24576}
    for i in range(16):
        t["R%d" % i] = i
    return t


def clean(line):
    """Remove comments and all whitespace."""
    return line.split("//")[0].replace(" ", "").replace("\t", "").strip()


def first_pass(lines, symbols):
    """Record label addresses; return list of instruction lines."""
    code, rom = [], 0
    for raw in lines:
        line = clean(raw)
        if not line:
            continue
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if label in symbols:
                print("Warning: label '%s' defined more than once" % label)
            symbols[label] = rom
        else:
            code.append(line)
            rom += 1
    return code


def translate_c(line):
    dest, jump = "", ""
    if "=" in line:
        dest, line = line.split("=", 1)
    if ";" in line:
        line, jump = line.split(";", 1)
    return "111" + COMP[line] + DEST[dest] + JUMP[jump]


def second_pass(code, symbols, user_symbols):
    out, next_var = [], 16
    for line in code:
        if line.startswith("@"):
            s = line[1:]
            if s.isdigit():
                n = int(s)
            else:
                if s not in symbols:
                    symbols[s] = next_var
                    user_symbols[s] = next_var
                    next_var += 1
                n = symbols[s]
            out.append(format(n, "016b"))
        else:
            out.append(translate_c(line))
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python assembler.py Prog.asm")
    path = sys.argv[1]
    with open(path) as f:
        lines = f.readlines()

    symbols = predefined()
    code = first_pass(lines, symbols)
    labels = {k: v for k, v in symbols.items()
              if k not in predefined()}          # labels found in pass 1
    variables = {}
    binary = second_pass(code, symbols, variables)

    out_path = path.rsplit(".", 1)[0] + ".hack"
    with open(out_path, "w") as f:
        f.write("\n".join(binary) + "\n")

    # --- Extra feature (K mod 3 == 0): symbols.txt ---
    with open("symbols.txt", "w") as f:
        f.write("# Labels (ROM addresses)\n")
        for k, v in labels.items():
            f.write("%s = %d\n" % (k, v))
        f.write("# Variables (RAM addresses)\n")
        for k, v in variables.items():
            f.write("%s = %d\n" % (k, v))
    print("Wrote %s (%d instructions) and symbols.txt" % (out_path, len(binary)))


if __name__ == "__main__":
    main()
