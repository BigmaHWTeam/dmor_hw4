# LaTeX Homework Template

This repository provides a LaTeX template for creating homework assignments.

## Overview

This template is designed to be easily configurable for various assignments. The main file can be renamed to reflect the specific assignment you are working on. The template is structured to separate content, formatting, and preamble, making it easy to manage your work.

## File Structure

- `assignment.tex`: The main LaTeX file. **You should rename this file.**
- `preamble.tex`: Contains all the `\usepackage` commands and document setup.
- `format.tex`: Defines the visual formatting of the document, including theorem and problem environments.
- `header.tex`: Defines the header of the document, including name, class, and assignment details.
- `problem1.tex`: An example file for writing a problem and its solution. You can create more `problemX.tex` files and include them in your main `.tex` file.
- `.latexmkrc`: Configuration file for `latexmk`.
- `.github/workflows/build.yml`: GitHub Actions workflow for automatically building the PDF.

## How to Use

1.  **Rename `assignment.tex`**:
    Rename `assignment.tex` to a name that is representative of your project (e.g., `homework1.tex`).

2.  **Update `.github/workflows/build.yml`**:
    Open the `.github/workflows/build.yml` file and find the `BUILD_FILE` environment variable. Change `assignment` to your new filename without the `.tex` extension. For example:
    ```yaml
    env:
      BUILD_FILE: homework1
    ```

## Building the PDF

To compile the LaTeX project and generate a PDF, you can use `latexmk`. You will need to specify the root `.tex` file. For example:

```bash
latexmk homework1.tex
```

This will generate a PDF with the same name as your main `.tex` file.

## CI/CD

This repository includes a GitHub Actions workflow in `.github/workflows/build.yml` that automatically builds the PDF of your assignment. The workflow is triggered on pushes and pull requests to the `main` branch, and also when a new tag is created.

When a tag is pushed, the workflow will create a new release and upload the compiled PDF as a release artifact.

> **Important:** For the CI/CD workflow to function correctly, you must enable "Read and Write permissions" for workflows in your GitHub repository settings. You can find this setting under `Settings > Actions > General > Workflow permissions`.