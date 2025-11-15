# Makefile for LaTeX project

# The main LaTeX file. This can be overridden from the command line.
# Example: make all MAIN_FILE=homework1
# Automatically detect MAIN_FILE if not specified
ifeq ($(origin MAIN_FILE), undefined)
    # Try assignment.tex first
    _DETECTED_MAIN_FILE := $(basename $(wildcard assignment.tex))

    # If not found, try hw*.tex
    ifeq ($(_DETECTED_MAIN_FILE),)
        _DETECTED_MAIN_FILE := $(basename $(firstword $(wildcard hw*.tex)))
    endif

    # If not found, try *-hw*.tex
    ifeq ($(_DETECTED_MAIN_FILE),)
        _DETECTED_MAIN_FILE := $(basename $(firstword $(wildcard *-hw*.tex)))
    endif

    # Fallback if no specific file is found
    ifeq ($(_DETECTED_MAIN_FILE),)
        MAIN_FILE := assignment
    else
        MAIN_FILE := $(_DETECTED_MAIN_FILE)
    endif
endif

# The LaTeX compiler
LATEXMK = latexmk

# All tex files
TEX_FILES = $(wildcard *.tex)

# The default target
all: $(MAIN_FILE).pdf

# Rule to build the PDF
$(MAIN_FILE).pdf: $(TEX_FILES)
	$(LATEXMK) $(MAIN_FILE)

# Clean up generated files
clean:
	rm -rf build *.aux *.bbl *.bcf *.blg *.dvi *.fdb_latexmk *.fls *.log *.out *.pdf *.ps *.run.xml

.PHONY: all clean
