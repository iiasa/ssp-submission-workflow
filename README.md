# Workflow for the SSP-ScenarioMIP scenario submission


Copyright 2022-2024 IIASA

[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Overview

This repository contains the workflow and configuration for the SSP-ScenarioMIP submission process starting in autumn 2024.

> [!TIP]
> For *users not comfortable working with GitHub repositories and yaml files*,
> the definitions for this project are available for download as an xlsx spreadsheet
> at https://files.ece.iiasa.ac.at/ssp-submission/ssp-submission-template.xlsx.

### Project nomenclature and model registration

This projects uses the variables region definitions from the
https://github.com/iamconsortium/common-definitions project.

The scenario names combine the SSP socio-economic assumptions and the 
climate ambition (i.e., emission pathways) according to the ScenarioMIP protocol (2024).

### Workflow

The module `workflow.py` has a function `main(df: pyam.IamDataFrame) -> pyam.IamDataFrame:`.

Per default, this function takes an **IamDataFrame** and returns it without
modifications. [Read the docs](https://pyam-iamc.readthedocs.io) for more information
about the **pyam** package for scenario analysis and data visualization.

**Important**: Do not change the name of the module `workflow.py` or the function `main`
as they are called like this by the Job Execution Service. Details can be found
[here](https://wiki.ece.iiasa.ac.at/wiki/index.php/Scenario_Explorer/Setup#Job_Execution_Service).
