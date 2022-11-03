import os


def copy_file(source, destination):
    os.popen("cp %s %s" % (source, destination))


def copy_nontex_files(directory, output_dir, ignore):
    for dirname, dirnames, filenames in os.walk(directory):
        # print path to all subdirectories first.
        # for subdirname in dirnames:
        #     print(os.path.join(dirname, subdirname))

        # print path to all filenames.
        for filename in filenames:
            if not filename.endswith((".tex", ".sty")) and filename[0] != ".":
                copy_file(os.path.join(dirname, filename), os.path.join(output_dir, filename))
            elif filename.endswith(".sty"):
                res = parse_file(filename, dirname, output_dir)
                with open(os.path.join(output_dir, filename), "w") as f:
                    f.write(res)
            # print(os.path.join(dirname, filename))

        # Advanced usage:
        # editing the 'dirnames' list will stop os.walk() from recursing into there.
        if '.git' in dirnames:
            # don't go into any .git directories.
            dirnames.remove('.git')
        if ignore in dirnames:
            dirnames.remove(ignore)
        for d in dirnames:
            if d[0] == ".":
                dirnames.remove(d)


def parse_inputs(line, input_type):
    k = line.index(input_type)
    before = line[:k]
    line = line[k:]
    if input_type in ("\\input", "\\include"):
        i = line.index("{")
        j = line.index("}")
        return before, line[i+1:j] + ".tex", line[j+1:]
    elif input_type in ("\\import", "\\subimport"):
        i = line.index("{")
        j = line.index("}")
        folder = line[i+1:j]
        line = line[j+1:]
        i = line.index("{")
        j = line.index("}")
        return before, folder, line[i+1:j] + ".tex", line[j+1:]


def parse_file(filename, directory, output_dir):
    final = ""
    with open(os.path.join(directory, filename)) as f:
        for line in f:
            output_line = parse_line(line, directory, output_dir)
            if output_line is not None:
                final += output_line
    return final


def parse_line(line, directory, output_dir):
    """
    For now this assumes only one includegraphics per line. Same with addplot
    """
    if not line.strip():
        return line
    elif line.strip()[0] == "%":
        return None
    elif "%" in line:
        line = line[:line.index("%")] + "\n"

    if "\\input{" in line or "\\include{" in line:
        before, path, after = parse_inputs(line, "\\input" if "\\input" in line else "\\include")
        line = (
            parse_line(before, directory, output_dir)
            + parse_file(path, directory, output_dir)
            + parse_line(after, directory, output_dir)
        )

    elif "\\import{" in line or "\\subimport{" in line:
        before, path, filename, after = parse_inputs(line, "\\import" if "\\import" in line else "\\subimport")
        line = (
            parse_line(before, directory, output_dir)
            + parse_file(filename, os.path.join(directory, path), output_dir)
            + parse_line(after, directory, output_dir)
        )

    elif "\\includegraphics" in line or "\\addplot" in line:
        command = line[line.index("\\addplot" if "\\addplot" in line else "\\includegraphics"):]
        command = command[:command.index("}")]
        filename = command[command.index("{")+1:]
        if filename.endswith((".pdf", ".dat", ".txt", ".png", ".jpg", ".jpeg")):
            folder, name = os.path.split(filename)
            line = line.replace(filename, name)

    return line



def squash(directory, main="main", output="squashed_output"):
    output_dir = os.path.join(directory, output)
    os.mkdir(output_dir)
    copy_nontex_files(directory, output_dir, output)
    output_filename = os.path.join(output_dir, main + ".tex")
    input_filename = os.path.join(directory, main + ".tex")

    new = parse_file(main+".tex", directory, output_dir)

    with open(output_filename, "w") as output_file:
        output_file.write(new)



if __name__ == "__main__":
    from sys import argv
    squash(*argv[1:])

