import os
import re

def transpile(code: str) -> str:
    rules = {
        r'#include\s*"fmt"': 'import "fmt"',
        r'\bfunction\b': 'func',
        r'while\s*\(1\)': 'for',
    }

    for pattern, repl in rules.items():
        code = re.sub(pattern, repl, code)

    code = code.replace(";", "")

    if "package main" not in code:
        code = "package main\n\n" + code

    return code


def read_godfile(folder):
    godfile_path = os.path.join(folder, "godfile")

    if not os.path.exists(godfile_path):
        print("❌ This directory is not have a 'godfile' file!")
        return []

    with open(godfile_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # boş satır ve yorumları temizle
    files = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            files.append(line)

    return files


def process_file(base_dir, rel_path, output_dir):
    input_path = os.path.join(base_dir, rel_path)

    if not os.path.exists(input_path):
        print(f"[HATA] Dosya yok: {rel_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        source = f.read()

    output = transpile(source)

    filename = os.path.basename(rel_path)
    new_name = os.path.splitext(filename)[0] + ".go"
    output_path = os.path.join(output_dir, new_name)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"[OK] {rel_path} → {new_name}")


def main():
    print("godf build system 😎")

    folder = input("Project directory, please. (empty = current directory):\n> ").strip()
    if not folder:
        folder = os.getcwd()

    if not os.path.exists(folder):
        print("❌ There is no such directory!")
        return

    files = read_godfile(folder)
    if not files:
        return

    output_dir = os.path.join(folder, "out_go")
    os.makedirs(output_dir, exist_ok=True)

    for file in files:
        if file.endswith(".gor"):
            process_file(folder, file, output_dir)
        else:
            print(f"[UYARI] Skipped! (not gor): {file}")

    print("\n🚀 Build complete. Output generated at ./out_go")


if __name__ == "__main__":
    main()