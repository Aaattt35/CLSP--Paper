**Exact Optimal Solution for the Single-Item CLSP: A New Mathematical Model**

This repository contains the implementation, benchmark instances, and computational results for the paper:



The goal of this repository is to provide full reproducibility for reviewers and readers, including:
- source code
- benchmark instances
- computational experiments
- results used in the manuscript

---

## Repository Structure
src/ Implementation of the optimization model and experiments

instances/ Benchmark instances used in the paper

results/ Computational results reported in the manuscript

text

---

## Installation and Setup

### 1. Clone the repository

If you want to run the code locally:
```bash
git clone https://github.com/USER_NAME/REPO_NAME.git
cd REPO_NAME
(If you downloaded the ZIP file from GitHub, simply extract it and continue.)

2. (Optional) Create and activate a Python environment
Using venv:

bash
python -m venv venv
source venv/bin/activate    # Linux / macOS
venv\Scripts\activate       # Windows
3. Install required Python packages
All Python dependencies are listed in requirements.txt.

Install them using:

bash
pip install -r requirements.txt
4. CPLEX installation
This project requires:

IBM ILOG CPLEX Optimizer
CPLEX Python API
Please follow IBM’s installation guidelines.

The Python API must be accessible in your active Python environment.

Running the Test Instance (For Reviewers)
A small test instance is provided for quick verification of the implementation:

bash
python src/run_experiment.py instances/test_instance.txt
The expected output is available in:

text
results/test_instance_output.csv
Reproducing Computational Results
All computational results reported in the paper are available in:

text
results/paper_results.csv
The benchmark instances used in the experiments are located in:

text
instances/
To fully reproduce the results, run the model on all benchmark instances and aggregate the outcomes into a CSV file following the same structure as paper_results.csv.

File Description
src/
Contains:

model.py — mathematical model implementation
solver.py — solver wrapper (CPLEX)
run_experiment.py — script for running instances individually or in batch
instances/
Contains:

test_instance.txt — small sample instance for reviewers
benchmark_instances.zip — full experimental dataset
README.md — description of instance format
results/
Contains:

paper_results.csv — results from the manuscript
test_instance_output.csv — output of the provided test instance
README.md — explanation of result file formats
License
Code
The source code is licensed under the MIT License.

See the LICENSE file for details.

Data (benchmark instances)
Benchmark instances are released under CC BY 4.0 (Attribution Required).

Please cite the paper when using these instances.

Citation
If you use this code or instances in academic work, please cite:

text
[Full citation of the paper will be added after publication]
Contact
For questions, reproducibility concerns, or dataset clarifications, please contact:

AATT(will be available after publishing)

Email: email@example.com
