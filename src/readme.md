## 📂 `src/` — Source Code Overview

The `src` directory contains all the source code used to build and execute the performance evaluation between different CLSP models. All code has been developed by the author within this project in python.


📂- CLSP--Paper/

├── 📂+ .github/workflows/

├── 📂+ instances/

├── 📂+ results/

├── 📂- src/

├── ├── ⚙️ 1-ALCP_Algorithm.py  `: developed to Establishe an Upper Bound on the Parameter m used in the TPM‑m Model.`

├── ├── ⚙️ 2-build_AGG_model.py  `:is recognized as the predominant modeling framework for CLSP.`

├── ├── ⚙️ 3-build_FAL_model.py  `: is another well‑known formulation used in the literature to model the CLSP.`

├── ├── ⚙️ 4-build_SHP_model.py  `: is also cited in the literature as a notable MIL formulation for the CLSP.`

├── ├── ⚙️ 5-build_TPM_m_model.py  `: is a modified version of TPM that incorporates the output of ALCP in code segment 1.`

├── ├── ⚙️ 6-build_TPM_model.py  `: is an original and efficient model developed in this study to exactly solve the CLSP.`

├── ├── ⚙️ 7-build_dp_solver.py  `: represents a prominent framework for addressing the CLSP in its general form.`

├── ├── ⚙️ 8-build_envl_model.py  `: the first efficient model developed by Hartman et al., is used for comprehensive evaluation.`  

├── ├── ⚙️ 9-build_weakenvl_model.py  `: the third efficient model developed by Hartman et al.`

├── ├── ⚙️ 10-build_weakl_model.py  `: the second efficient model developed by Hartman et al.`

├── ├── 📄 **readme.md**

├── └── 💾 11-run_experiment.py  `: The main code calls and runs all models, recording their solving times for evaluation.`

├── 🧾 LICENSE

├── 📄 README.md

└── 📄 requirements.txt

The central script is:

- **`run_experiment.py`**  
  Main entry point for running experiments. It loads problem instances, builds the relevant models, solves them using the selected solver, and saves the outputs in the `results/` directory.

---

## 🔧 Solver Usage

During development, **CPLEX** was used locally for testing due to its robustness and speed.  
However, in the public GitHub version, the solver is switched to **HiGHS**, which is free and open‑source — allowing anyone to run the code without a commercial license.

---

## Requirements

- Python **3.10+**
- Packages listed in:
requirements.txt


- If you wnat to use a commercial solver (e.g., **CPLEX**): must be pre-installed and Python‑accessible. The solver should be replaced with highs in the main body code:


      run_experiment.py


---


## ▶️ Running the Experiment with a test instance
**1. Install dependencies**

    pip install -r requirements.txt
   
Ensure that pyomo and highspy (or highs through conda) are installed.

**2.Check the defult test sample or load your intended test sample in.”**

    CLSP--Paper/instances/test_instance.txt


**3. Run an experiment**

Navigate to the project root and execute:

    python src/run_experiment.py

**4. View the test results and outputs**

(logs, objective values, models) will be saved automatically under:

    CLSP--Paper/results/test_instance_output.csv


🔁 To run the model **automatically**, navigate to the Actions tab in GitHub and choose `Run Optimization Model`to execute the workflow via CI/CD.


---

## Downloading the Example Output (Artifact)

1. Go to the **Actions** tab  
2. Open **Run Python Experiment**  
3. Select the latest run  
4. Scroll to **Artifacts**  
5. Download:
test-instance-results


Extract the ZIP and you will find:

      test_instance_output.csv


---


