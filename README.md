This repository provides the full implementation, benchmark instances, and computational results accompanying the manuscript **:**

## *Exact Optimal Solution for the Single-Item Capacitated Lot-Sizing Problem A New Mathematical Model*

The purpose of this repository is to ensure complete computational reproducibility for reviewers and readers, including access to the source code, datasets, and numerical results used in the preparation of the manuscript.

---

## 1. Repository Structure

📂- CLSP--Paper

├── 📂+ .github/workflows/

├── 📂+ instances/

├── 📂+ results/

├── 📂+ src/

├── 🧾 LICENSE

├── 📄 README.md

└── 📄 requirements.txt

- **src/**:        Source code for the mathematical model and experimental framework
- **instances/**:  Benchmark instances used for evaluation + a test instance used to run the experiment
- **results/**:    Computational Results reported in the manuscript + Test Instance Outputs 

---

## 2. Obtaining the Repository

The repository may be downloaded as a ZIP file directly from [GitHub](https://github.com/Aaattt35/CLSP--Paper) or cloned via:

    git clone https://github.com/Aaattt35/CLSP--Paper

---


## 3. Test Instance


A small test instance is available for verification. Alternatively, you can change it to your intended instance here:

        instances/test_instance.txt

The corresponding expected output is included in:

        results/test_instance_output.csv

This allows reviewers to execute the code with no installation or further setup required.

---

## 4. Reproducing the Computational Study

The full set of benchmark instances is located in:

    instances/Generated_instances/

The numerical results reported in the manuscript are available in:

    results/paper_results.csv

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

[Author]  
[affil]  
Email: [email@example.com]

---
