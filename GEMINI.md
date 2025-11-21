# GEMINI.md: Project Overview

This document provides a comprehensive overview of the `hw4` project, its structure, and how to work with it.

## Project Overview

This project is a university homework assignment for a class on Deterministic Models of Operations Research (DMOR). It is built using a combination of LaTeX for the report and Python for solving optimization problems.

The core of the project involves:
1.  **LaTeX Report:** The final output is a PDF document generated from `.tex` files. The structure is modular, with a main file (`hw4.tex`) that includes preamble, formatting, header, and problem-specific content files.
2.  **Python/AMPL for Optimization:** Python scripts are used to solve mathematical optimization problems. These scripts leverage the `amplpy` library to interact with the AMPL modeling language. Optimization models are defined in `.mod` files, and data is provided in `.dat` files. The Python scripts execute the models, solve them using an appropriate solver (e.g., Gurobi), and format the results.
3.  **Build Automation:** A `Makefile` automates the entire process. It first runs the Python scripts to generate result files (`.amplout`) and then compiles the LaTeX document, ensuring that the latest results are included in the PDF.
4.  **Reproducible Environment:** The project uses `flake.nix` and `.envrc` with `direnv` to provide a reproducible development environment with all the necessary dependencies.
5.  **Continuous Integration:** A GitHub Actions workflow is set up in `.github/workflows/build.yml` to automatically build the PDF on every push. When a git tag is pushed, it creates a GitHub release and attaches the compiled PDF.

## Building and Running

### Building the PDF

The primary way to build the project is by using the `Makefile`.

*   **To build the PDF:**
    ```bash
    make
    ```
    This command will:
    1.  Run the Python script in `problem1_python/` to generate the `problem1.amplout` file in the `ampl/` directory.
    2.  Compile `hw4.tex` into `hw4.pdf` using `latexmk`.

*   **To clean up generated files:**
    ```bash
    make clean
    ```

### Testing Changes

When making changes to the Python scripts, the preferred method for testing is to rebuild the entire PDF document to ensure that the generated outputs are correctly integrated into the final report.

You can do this by running:
```bash
make
```

This ensures that any visual outputs, such as Gantt charts, are regenerated and correctly embedded in the LaTeX document.

## Key Files

*   `hw4.tex`: The main LaTeX file that brings all the other parts of the document together.
*   `Makefile`: The build script that automates the generation of the PDF.
*   `problem1.tex`: A LaTeX file containing the write-up for Problem 1.
*   `problem1_python/problem1.py`: The Python script that solves the optimization model for Problem 1.
*   `problem1_python/problem1.mod`: The AMPL model file for Problem 1.
*   `problem1_python/problem1.dat`: The AMPL data file for Problem 1. Note: `.dat` files cannot be read using the `read_file` tool; use `cat` to display their contents.
*   `ampl/problem1.amplout`: The output from the Python script, which is included in the LaTeX document.
*   `requirements.txt`: Lists the Python dependencies for the project, notably `amplpy` and various solvers.
*   `.github/workflows/build.yml`: The GitHub Actions workflow for continuous integration.
*   `flake.nix`: Defines the Nix flake for a reproducible environment.

## Development Conventions

*   **Modular LaTeX:** The LaTeX document is split into multiple files for better organization (`preamble.tex`, `format.tex`, `header.tex`, and problem-specific files).
*   **Problem-Specific Directories:** Code for each problem is contained within its own directory (e.g., `problem1_python/`).
*   **Separation of Concerns:** The optimization model (`.mod`), data (`.dat`), and solving logic (`.py`) are kept in separate files.
*   **Automated Builds:** All build steps are codified in the `Makefile` to ensure a consistent and reliable build process.
*   **Styling:** Visual elements, such as charts and graphs, should adhere to the University of Florida's brand guidelines. The official color palette can be found at the [UF Brand Center](https://brandcenter.ufl.edu/colors/#gradients).
