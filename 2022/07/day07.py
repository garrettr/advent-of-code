#!/usr/bin/env python3
import os
import sys


def print_fs(fs, depth=0):
    for name, node in fs.items():
        indent = ' ' * depth * 2
        if isinstance(node, dict):
            print(f"{indent}- {name} (dir)")
            print_fs(node, depth + 1)
        else:
            print(f"{indent}- {name} (file, size={node})")


def size_dirs(sizes, node, name="/"):
    if isinstance(node, dict):
        size = sum([size_dirs(sizes, child, "/".join([name, child_name])) for child_name, child in node.items()])
        sizes[name] = size
        return size
    else:
        return node


def part1(input_file):
    # represent filesystem tree
    # { name (dir or file) : { names (if dir) }, or size if file}
    root = {"/": {}}
    # stack representing history of directory traversal and current working directory
    dirs = [root['/']]

    # parse terminal output
    for line in input_file:
        cwd = dirs[-1]

        if line.startswith("$"):
            _, cmd, *args = line.split()
            if cmd == "cd":
                dirname = args[0]
                if dirname == "/":
                    del dirs[1:]
                elif dirname == "..":
                    dirs.pop()
                else:
                    dirs.append(cwd[dirname])
        else:
            desc, name = line.split()
            if desc == "dir":
                cwd[name] = {}
            else:
                cwd[name] = int(desc) # size

    #print_fs(root)

    # determine the total size of each directory
    sizes = {}
    size_dirs(sizes, root["/"])

    # find directories with total size at most 100000
    selected_dirs = {name: size for name, size in sizes.items() if size <= 100000}
    return sum(selected_dirs.values())

    
if __name__ == "__main__":
    input_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(os.path.dirname(__file__), "input.txt")
    )
    with open(input_path) as input_file:
        print(part1(input_file))
