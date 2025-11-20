# Makefile for Homework 4

# The main LaTeX file
MAIN = hw4

# The LaTeX compiler
LATEXMK = latexmk

# All tex files
TEX_FILES = $(wildcard *.tex)

# --- Problem 1 ---
PROBLEM1_DIR = problem1_python
PROBLEM1_SCRIPT = $(PROBLEM1_DIR)/problem1.py
AMPL_OUTPUT_DIR = ampl
PROBLEM1_AMPLOUT = $(AMPL_OUTPUT_DIR)/problem1.amplout

# The default target
all: $(MAIN).pdf

# Rule to build the PDF
$(MAIN).pdf: $(TEX_FILES) $(PROBLEM1_AMPLOUT)
	$(LATEXMK) -pdf $(MAIN)

# Rule to generate problem1.amplout
$(PROBLEM1_AMPLOUT): $(PROBLEM1_SCRIPT) | $(AMPL_OUTPUT_DIR)
	@echo "Running script to generate AMPL output for problem 1"
	cd $(PROBLEM1_DIR) && AMPLHW_OUTPUT=true python $(notdir $(PROBLEM1_SCRIPT))
	@mv $(PROBLEM1_DIR)/*.amplout $(AMPL_OUTPUT_DIR)

# Create ampl output directory if it doesn't exist
$(AMPL_OUTPUT_DIR):
	@mkdir -p $(AMPL_OUTPUT_DIR)

# Clean up generated files
clean:
	rm -rf build ampl
	rm -f *.aux *.bbl *.bcf *.blg *.dvi *.fdb_latexmk *.fls *.log *.out *.pdf *.ps *.run.xml
	rm -f $(PROBLEM1_AMPLOUT)

.PHONY: all clean
