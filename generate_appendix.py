
def generate_latex():
    output = []
    
    # Generate for node01 to node34
    for i in range(1, 35):
        node_num = "%02d" % i
        short_num = "%d" % i
        
        entry = "  \\begin{tcolorbox}\n"
        entry += "    \\lstinputlisting[language=Python, numbers=left, numberstyle=\\tiny,\n"
        entry += "      stepnumber=2, numbersep=5pt,\n"
        entry += "      basicstyle=\\small\\fontencoding{T1}\\selectfont, label={lst:appendn" + short_num + "mod},\n"
        entry += "      caption={Node " + short_num + " Model}]{problem4_python/node" + node_num + ".mod}\n"
        entry += "  \\end{tcolorbox}\n"
        entry += "  \\begin{tcolorbox}\n"
        entry += "    \\lstinputlisting[language=Python, numbers=left, numberstyle=\\tiny,\n"
        entry += "      stepnumber=2, numbersep=5pt,\n"
        entry += "      basicstyle=\\small\\fontencoding{T1}\\selectfont, label={lst:appendn" + short_num + "out},\n"
        entry += "      caption={Node " + short_num + " Output}]{ampl/branchbound/node" + node_num + ".amplout}\n"
        entry += "  \\end{tcolorbox}"
        output.append(entry)
        
    return "\n".join(output)

if __name__ == "__main__":
    print(generate_latex())
