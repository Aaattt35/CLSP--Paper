## 📂 `src/` — Source Code Overview

The `src` directory contains all the source code used to build and execute the performance evaluation between different CLSP models. All code has been developed by the author within this project.


📂- CLSP--Paper/

├── 📂+ .github/workflows/

├── 📂+ instances/

├── 📂+ results/

├── 📂- src/

├── ├── ⚙️ ALCP_Algorithm.py

├── ├── ⚙️ build_AGG_model.py

├── ├── ⚙️ build_FAL_model.py

├── ├── ⚙️ build_SHP_model.py

├── ├── ⚙️ build_TPM_m_model.py

├── ├── ⚙️ build_TPM_model.py

├── ├── ⚙️ build_dp_solver.py

├── ├── ⚙️ build_envl_model.py

├── ├── ⚙️ build_weakenvl_model.py

├── ├── ⚙️ build_weakl_model.py

├── ├── ⚙️ build_weakenvl_model.py

├── ├── 📄 **readme.md**

├── ├── 💾 run_experiment.py

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


