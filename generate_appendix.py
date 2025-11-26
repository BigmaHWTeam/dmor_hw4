import glob
import re

def generate_latex():
    output = []

    # Find all node files in problem4_python directory
    mod_files = glob.glob('problem4_python/node*.mod')

    # Extract node numbers
    node_numbers = []
    for f in mod_files:
        match = re.search(r'node(\d+)\.mod', f)
        if match:
            node_numbers.append(int(match.group(1)))

    # Sort the numbers to ensure correct order
    node_numbers.sort()

    # Generate for found nodes
    for i in node_numbers:
        node_num = "%02d" % i
        short_num = "%d" % i

        entry = "  \\begin{tcolorbox}\n"
        entry += (
            "    \\lstinputlisting[language=Python, numbers=left, numberstyle=\\tiny,\n"
        )
        entry += "      stepnumber=2, numbersep=5pt,\n"
        entry += (
            "      basicstyle=\\small\\fontencoding{T1}\\selectfont, label={lst:appendn"
            + short_num
            + "mod},\n"
        )
        entry += (
            "      caption={Node "
            + short_num
            + " Model}]{problem4_python/node"
            + node_num
            + ".mod}\n"
        )
        entry += "  \\end{tcolorbox}\n"
        entry += "  \\begin{tcolorbox}\n"
        entry += (
            "    \\lstinputlisting[language=Python, numbers=left, numberstyle=\\tiny,\n"
        )
        entry += "      stepnumber=2, numbersep=5pt,\n"
        entry += (
            "      basicstyle=\\small\\fontencoding{T1}\\selectfont, label={lst:appendn"
            + short_num
            + "out},\n"
        )
        entry += (
            "      caption={Node "
            + short_num
            + " Output}]{ampl/branchbound/node"
            + node_num
            + ".amplout}\n"
        )
        entry += "  \\end{tcolorbox}"
        output.append(entry)

    return "\n".join(output)


if __name__ == "__main__":
    print(generate_latex())
