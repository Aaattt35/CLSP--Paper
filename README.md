---

# Exact Optimal Solution for the Single-Item CLSP  
## A New Mathematical Model

This repository provides the full implementation, benchmark instances, and computational results accompanying the manuscript:

**Exact Optimal Solution for the Single-Item Capacitated Lot-Sizing Problem: A New Mathematical Model**

The purpose of this repository is to ensure complete computational reproducibility for reviewers and readers, including access to the source code, datasets, and numerical results used in the preparation of the manuscript.

---

## 1. Repository Structure

    src/        Source code for the mathematical model and experimental framework
    instances/  Benchmark instances used for evaluation
    results/    Computational results reported in the manuscript

---

## 2. Installation Instructions

### 2.1. Obtaining the Repository

The repository may be downloaded as a ZIP file directly from GitHub or cloned via:

    git clone https://github.com/USER_NAME/REPO_NAME.git
    cd REPO_NAME

---

### 2.2. Python Environment (Recommended)

A dedicated Python environment is recommended:

    python -m venv venv
    source venv/bin/activate        # Linux/macOS
    venv\Scripts\activate           # Windows

---

### 2.3. Required Python Packages

All required packages are listed in `requirements.txt` and may be installed as:

    pip install -r requirements.txt

---

### 2.4. CPLEX Requirements

The implementation requires:

- IBM ILOG CPLEX Optimizer  
- CPLEX Python API  

Please ensure that CPLEX is installed and that the Python API is available within the active environment. Refer to IBM’s official documentation for installation procedures.

---

## 3. Running the Implementation

### 3.1. Test Instance

A small test instance is provided for verification. The following command executes the model on this instance:

    python src/run_experiment.py instances/test_instance.txt

The corresponding expected output is included in:

    results/test_instance_output.csv

This allows reviewers to confirm correctness without executing the full experimental study.

---

## 4. Reproducing the Computational Study

The full set of benchmark instances is located in:

    instances/

The numerical results reported in the manuscript are available in:

    results/paper_results.csv

To reproduce the complete computational study:

1. Execute the solver on all benchmark instances.  
2. Record objective values, solution times, and solver status.  
3. Aggregate results following the schema of `paper_results.csv`.  

This ensures full reproducibility of the experiments contained in the manuscript.

---

## 5. File Descriptions

### 5.1. Source Code (src/)

- model.py – Implementation of the mathematical formulation.  
- solver.py – Wrapper for interaction with the CPLEX solver.  
- run_experiment.py – Script for executing individual or batch experiments.  

### 5.2. Instances (instances/)

- test_instance.txt – Minimal example instance for verification.  
- benchmark_instances.zip – Full dataset used in the computational study.  
- README.md – Description of instance format and parameters.  

### 5.3. Results (results/)

- paper_results.csv – Numerical results reported in the manuscript.  
- test_instance_output.csv – Output corresponding to the provided test instance.  
- README.md – Explanation of metrics and file structure.  

---

## 6. Licensing

### 6.1. Code License  

The source code is distributed under the terms of the MIT License.  
See the file LICENSE for details.

### 6.2. Data License  

Benchmark instances are distributed under the CC BY 4.0 (Creative Commons Attribution 4.0 International License).  
Users are required to cite the associated manuscript when using these datasets.

---

## 7. Citation

If you use this code or dataset in academic work, please cite the manuscript as:

    [Full bibliographic citation will be inserted upon publication]

---

## 8. Contact

For questions regarding reproducibility, implementation details, or numerical experiments, please contact the corresponding author:

[Author Name]  
[Institution / Department]  
Email: [your_email@example.com]

---
