# Dataset of Generated Instances

This directory contains all generated instances used in the computational study associated with this work.  
The instances are organized according to different levels of the **α ratio** and various **capacity‑to‑demand (c) ratios**.

Each file in this directory corresponds to a single instance and encodes all parameters required by the model described in the paper.

---

## 1. Instance File Content

Each instance file contains the following fields:

| Field | Description |
|:------|:------------|
| **ins** | Index of the instance within its corresponding class. |
| **f = (f_min, f_max)** | Range of the \( f^r \) ratio, as defined in the paper. |
| **c** | Capacity‑to‑demand ratio. A detailed definition is provided in the main text of the paper. |
| **T** | Length of the planning horizon (number of periods). |
| **i_n** | Number of instances generated for the specific combination of \( f \), \( c \), and \( T \). |
| **stat** | Statistical information related to a coefficient in the TPN model (see the paper for the exact definition and role of this coefficient). |
| **d** | Vector of demand values for each period in the planning horizon. |
| **p** | Vector of unit production costs. |
| **cap** | Vector of production capacities for each period. |
| **s** | Setup cost associated with initiating production. |
| **h** | Vector of inventory holding costs per period. |

---

## 2. Organization of Instances

Instances are grouped according to:

- **α‑ratio levels**, and  
- **capacity‑to‑demand (c) ratios**,

in order to support stratified analysis and reproducibility of the computational experiments.

The naming convention and grouping of files are consistent with the experimental design reported in the paper. Users are referred to the paper for:

- formal definitions of all parameters,  
- details of the instance generation procedure, and  
- the role of each parameter in the underlying optimization model.

---

## 3. Usage and Reproducibility

These instances are intended to enable:

- replication of the numerical experiments reported in the paper, and  
- further sensitivity analyses or methodological comparisons by other researchers.

When using this dataset, please cite the associated paper. If you modify or extend the instances, we recommend clearly documenting any changes (e.g., in a separate `README` or change log) to facilitate reproducibility.

---
