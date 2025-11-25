# Makefile for Homework 4

# The main LaTeX file
MAIN = hw4

# The LaTeX compiler
LATEXMK = latexmk

# All tex files
TEX_FILES = $(wildcard *.tex)

# Appendix generation
APPENDIX_GEN_SCRIPT = generate_appendix.py
APPENDIX_NODES_TEX = appendix_nodes.tex

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

# --- Problem 3 ---
PROBLEM3_DIR = problem3_python
PROBLEM3_SCRIPT = $(PROBLEM3_DIR)/problem3_1.py $(PROBLEM3_DIR)/problem3_2.py
PROBLEM3_AMPLOUT = $(AMPL_OUTPUT_DIR)/problem3_1.amplout $(AMPL_OUTPUT_DIR)/problem3_2.amplout

# --- Problem 4 ---
PROBLEM4_DIR = problem4_python
PROBLEM4_SCRIPT = $(PROBLEM4_DIR)/problem4.py
PROBLEM4_NODE_MODS = $(wildcard $(PROBLEM4_DIR)/node*.mod)
AMPL_BRANCHBOUND_DIR = $(AMPL_OUTPUT_DIR)/branchbound
PROBLEM4_NODE_AMPLOUTS = $(patsubst $(PROBLEM4_DIR)/%.mod, $(AMPL_BRANCHBOUND_DIR)/%.amplout, $(PROBLEM4_NODE_MODS))
PROBLEM4_AMPLOUT = $(AMPL_OUTPUT_DIR)/integer.amplout $(AMPL_OUTPUT_DIR)/relaxation.amplout $(PROBLEM4_NODE_AMPLOUTS)

PROBLEM4_VISUALIZE_SCRIPT = $(PROBLEM4_DIR)/visualize_tree.py
PROBLEM4_TREE_PDF = $(IMAGES_DIR)/binary_search_tree.pdf

# Images directory
IMAGES_DIR = images

# The default target
all: $(MAIN).pdf $(PROBLEM2_PDFS) $(PROBLEM4_TREE_PDF)

# Target to run all python scripts
python_scripts: $(PROBLEM1_AMPLOUT) $(PROBLEM2_AMPLOUT) $(PROBLEM3_AMPLOUT) $(PROBLEM2_PDFS) $(PROBLEM4_AMPLOUT) $(PROBLEM4_TREE_PDF) $(APPENDIX_NODES_TEX)

# Rule to build the PDF
$(MAIN).pdf: $(TEX_FILES) $(PROBLEM1_AMPLOUT) $(PROBLEM2_AMPLOUT) $(PROBLEM3_AMPLOUT) $(PROBLEM4_AMPLOUT) $(PROBLEM4_TREE_PDF) $(APPENDIX_NODES_TEX)
	$(LATEXMK) -pdf $(MAIN)

# Rule to generate appendix_nodes.tex
$(APPENDIX_NODES_TEX): $(APPENDIX_GEN_SCRIPT)
	@echo "Generating appendix_nodes.tex"
	python3 $(APPENDIX_GEN_SCRIPT) > $(APPENDIX_NODES_TEX)

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

# Rule to generate problem3.amplout
$(PROBLEM3_AMPLOUT): $(PROBLEM3_SCRIPT) | $(AMPL_OUTPUT_DIR)
	@echo "Running scripts to generate AMPL output for problem 3"
	$(foreach script,$(PROBLEM3_SCRIPT), \
		(cd $(PROBLEM3_DIR) && AMPLHW_OUTPUT=true python $(notdir $(script))); \
	)
	@mv $(PROBLEM3_DIR)/*.amplout $(AMPL_OUTPUT_DIR)

# Rule to generate problem4.amplout
$(PROBLEM4_AMPLOUT): $(PROBLEM4_SCRIPT) | $(AMPL_OUTPUT_DIR) $(AMPL_BRANCHBOUND_DIR)
	@echo "Running script to generate AMPL output for problem 4"
	cd $(PROBLEM4_DIR) && AMPLHW_OUTPUT=true python $(notdir $(PROBLEM4_SCRIPT))
	@mv $(PROBLEM4_DIR)/integer.amplout $(AMPL_OUTPUT_DIR)
	@mv $(PROBLEM4_DIR)/relaxation.amplout $(AMPL_OUTPUT_DIR)
	@if ls $(PROBLEM4_DIR)/node*.amplout 1> /dev/null 2>&1; then mv $(PROBLEM4_DIR)/node*.amplout $(AMPL_BRANCHBOUND_DIR); fi

# Rule to generate problem4 tree PDF
$(PROBLEM4_TREE_PDF): $(PROBLEM4_VISUALIZE_SCRIPT) | $(IMAGES_DIR)
	@echo "Generating branch and bound tree visualization for problem 4"
	cd $(PROBLEM4_DIR) && python $(notdir $(PROBLEM4_VISUALIZE_SCRIPT))
	@mv $(PROBLEM4_DIR)/binary_search_tree.pdf $(IMAGES_DIR)

# Create ampl output directory if it doesn't exist
$(AMPL_OUTPUT_DIR):
	@mkdir -p $(AMPL_OUTPUT_DIR)

# Create ampl/branchbound directory
$(AMPL_BRANCHBOUND_DIR):
	@mkdir -p $(AMPL_BRANCHBOUND_DIR)

# Create images directory if it doesn't exist
$(IMAGES_DIR):
	@mkdir -p $(IMAGES_DIR)

# Clean up generated files
clean:
	rm -rf build $(AMPL_OUTPUT_DIR) $(IMAGES_DIR)
	rm -f *.aux *.bbl *.bcf *.blg *.dvi *.fdb_latexmk *.fls *.log *.out *.pdf *.ps *.run.xml
	rm -f $(PROBLEM1_AMPLOUT)
	rm -f $(PROBLEM2_AMPLOUT)
	rm -f $(PROBLEM3_AMPLOUT)
	rm -f $(PROBLEM4_AMPLOUT) $(PROBLEM4_TREE_PDF) $(APPENDIX_NODES_TEX)

.PHONY: all clean

