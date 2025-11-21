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

# --- Problem 2 ---
PROBLEM2_DIR = problem2_python
PROBLEM2_SCRIPT = $(PROBLEM2_DIR)/problem2.py
PROBLEM2_AMPLOUT = $(AMPL_OUTPUT_DIR)/problem2.amplout
PROBLEM2_PDFS = $(IMAGES_DIR)/problem2_optimal_gantt.pdf \
				$(IMAGES_DIR)/problem2_greedy_gantt.pdf \
				$(IMAGES_DIR)/problem2_commercial_first_gantt.pdf

# Images directory
IMAGES_DIR = images

# The default target
all: $(MAIN).pdf $(PROBLEM2_PDFS)

# Rule to build the PDF
$(MAIN).pdf: $(TEX_FILES) $(PROBLEM1_AMPLOUT) $(PROBLEM2_AMPLOUT)
	$(LATEXMK) -pdf $(MAIN)

# Rule to generate problem1.amplout
$(PROBLEM1_AMPLOUT): $(PROBLEM1_SCRIPT) | $(AMPL_OUTPUT_DIR)
	@echo "Running script to generate AMPL output for problem 1"
	cd $(PROBLEM1_DIR) && AMPLHW_OUTPUT=true python $(notdir $(PROBLEM1_SCRIPT))
	@mv $(PROBLEM1_DIR)/*.amplout $(AMPL_OUTPUT_DIR)

# Rule to generate problem2.amplout and PDFs
$(PROBLEM2_AMPLOUT) $(PROBLEM2_PDFS): $(PROBLEM2_SCRIPT) | $(AMPL_OUTPUT_DIR) $(IMAGES_DIR)
	@echo "Running script to generate AMPL output and PDFs for problem 2"
	cd $(PROBLEM2_DIR) && AMPLHW_OUTPUT=true python $(notdir $(PROBLEM2_SCRIPT))
	@mv $(PROBLEM2_DIR)/problem2.amplout $(AMPL_OUTPUT_DIR)
	@mv $(PROBLEM2_DIR)/problem2_*.pdf $(IMAGES_DIR)

# Create ampl output directory if it doesn't exist
$(AMPL_OUTPUT_DIR):
	@mkdir -p $(AMPL_OUTPUT_DIR)

# Create images directory if it doesn't exist
$(IMAGES_DIR):
	@mkdir -p $(IMAGES_DIR)

# Clean up generated files
clean:
	rm -rf build $(AMPL_OUTPUT_DIR) $(IMAGES_DIR)
	rm -f *.aux *.bbl *.bcf *.blg *.dvi *.fdb_latexmk *.fls *.log *.out *.pdf *.ps *.run.xml
	rm -f $(PROBLEM1_AMPLOUT)
	rm -f $(PROBLEM2_AMPLOUT)

.PHONY: all clean

