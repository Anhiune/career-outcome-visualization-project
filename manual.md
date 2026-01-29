# Machine Learning Environment Setup Guide

This guide will help you set up a Conda environment with all the necessary dependencies for your project, including Numpy, Matplotlib, and various Machine Learning packages.

## Prerequisites

- **Anaconda or Miniconda**: Ensure you have Conda installed on your system. You can verify this by running:
  ```bash
  conda --version
  ```

## 1. Create the Environment

Navigate to the project directory where `environment.yml` is located and run the following command to create the environment named `ml_env`:

```bash
conda env create -f environment.yml
```

*Note: This process may take a few minutes as it downloads and installs the required packages.*

## 2. Activate the Environment

Once the installation is complete, activate the environment using:

```bash
conda activate ml_env
```

## 3. Verify Installation

You can verify that the key packages are installed correctly by running a quick check in python:

```bash
python -c "import numpy; import matplotlib; import pandas; import sklearn; import torch; print('All packages imported successfully!')"
```

## 4. Updates

If you need to update the environment based on changes to `environment.yml` in the future, run:

```bash
conda env update -f environment.yml --prune
```

## Included Packages

- **Core**: Python 3.10
- **Data Manipulation**: NumPy, Pandas
- **Visualization**: Matplotlib
- **Machine Learning**: Scikit-Learn
- **Deep Learning**: PyTorch, Torchvision
- **Tools**: Jupyter

---
Happy Coding!
