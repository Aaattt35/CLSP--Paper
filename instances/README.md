# Benchmark Instances for Computational Experiments

This Folder contains the **benchmark instances** used in the computational experiments presented in the paper.

---

## Contents

### `generator.py`
Script used to generate the problem instances.  
It can be executed to reproduce or extend the dataset used in the experiments.

### `test_instance.txt`
A small test instance provided for reviewers and users to **quickly verify** that the code and model run correctly.

### `Generated_instances/`
This folder contains **all generated instances** used in the computational experiments described in the paper.

Each file within this folder corresponds to a specific set of instances, including four instances generated for different planning‑horizon values for each combination of **α** and **c**, and encodes all parameters required by the model.

---

## Usage

- Run `generator.py` to create new instances or regenerate existing ones.  
- Use `test_instance.txt` to perform quick functionality checks before running large‑scale experiments.  
- Refer to the paper for a detailed explanation of the parameters and instance generation process.
