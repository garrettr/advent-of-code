#!/usr/bin/env python3
from dataclasses import dataclass, field
import os
import sys


@dataclass
class Dir:
    name: str
    size: int = 0
    contents: dict = field(default_factory=dict)


@dataclass
class File:
    name: str
    size: int


class Filesystem:
    def __init__(self, root: Dir):
        self.root = root

    @classmethod
    def from_file(cls, file):
        root = Dir("/")
        # stack representing history of directory traversal and current working directory
        dirs = []

        # parse terminal output
        for line in file:
            cwd = dirs[-1] if len(dirs) else None

            if line.startswith("$"):
                _, cmd, *args = line.split()
                if cmd == "cd":
                    dirname = args[0]
                    if dirname == "/":
                        dirs.clear()
                        dirs.append(root)
                    elif dirname == "..":
                        dirs.pop()
                    else:
                        dirs.append(cwd.contents[dirname])
            else:
                desc, name = line.split()
                if desc == "dir":
                    cwd.contents[name] = Dir(name)
                else:
                    cwd.contents[name] = File(name, int(desc))

        return cls(root)

    def __str__(self):
        lines = []

        def dfs(node, depth=0):
            indent = ' ' * depth * 2
            if isinstance(node, Dir):
                lines.append(f"{indent}- {node.name} (dir, size={node.size})")
                for child in node.contents.values():
                    dfs(child, depth + 1)
            else:
                lines.append(f"{indent}- {node.name} (file, size={node.size})")

        dfs(self.root)
        return '\n'.join(lines)

    def calculate_dir_sizes(self):
        def dfs(node):
            if isinstance(node, Dir):
                node.size = sum(dfs(child) for child in node.contents.values())
            return node.size

        return dfs(self.root)

    def dir_sizes(self):
        sizes = []

        def dfs(node):
            if isinstance(node, Dir):
                sizes.append(node.size)
                for child in node.contents.values():
                    dfs(child)

        dfs(self.root)
        return sizes


def part1(fs):
    # find directories with total size at most 100000
    sizes = [size for size in fs.dir_sizes() if size <= 100000]
    return sum(sizes)


if __name__ == "__main__":
    input_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.join(os.path.dirname(__file__), "input.txt")
    )

    with open(input_path) as input_file:
        fs = Filesystem.from_file(input_file)
        fs.calculate_dir_sizes()

        print(part1(fs))
