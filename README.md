# Shaft Diameter Estimation Tool

## Overview

This project was developed for MAE 190 to estimate the required diameter of a shaft based on user-defined loading conditions, material properties, and design criteria. The program features a graphical user interface (GUI) that allows users to input the necessary parameters and obtain an estimated shaft diameter.

The tool automates the shaft design process by incorporating relevant engineering relationships and material property data, reducing the need for manual calculations and table lookups.

## Features

- **Graphical User Interface:** Provides an accessible interface for entering design parameters.
- **Loading Conditions:** Accepts applied bending moment (\(M_m\)), alternating bending moment (\(M_a\)), mean torque (\(T_m\)), and alternating torque (\(T_a\)).
- **Material Selection:** Uses material property data to evaluate shaft design requirements.
- **Safety Factor:** Incorporates a user-defined factor of safety into the diameter estimation.
- **Automated Calculations:** Determines necessary diameter-dependent design parameters internally rather than requiring users to obtain them manually from reference charts.
- **Diameter Estimation:** Calculates an estimated shaft diameter based on the selected inputs and design criteria.

## Files

| File | Description |
|---|---|
| `MAE190_Project.py` | Main Python script that runs the program and launches the GUI. It processes user inputs and performs the shaft diameter calculations. |
| `ASTM.json` | Contains material property and reference table data transcribed from *Shigley's Mechanical Engineering Design*, used in the shaft design calculations. |
| `proof_of_concept` | Contains preliminary calculations using preset values to verify the calculation method and demonstrate the program's functionality. |

## Requirements

- Python 3
- Python libraries required by the main program (see the imports in `MAE190_Project.py`).

## How to Run

1. Download or clone this repository.
2. Ensure Python and the required dependencies are installed.
3. Run the main program:

   ```bash
   python MAE190_Project.py
   ```

4. Use the GUI to enter the loading conditions, select a material, specify the factor of safety, and provide any other required design assumptions.
5. Run the calculation to obtain the estimated shaft diameter.

## Methodology

The program uses the user-provided loading conditions, material properties, and design criteria to estimate the required shaft diameter. Reference data stored in `ASTM.json` supports the material selection and design calculations.

Because some shaft design parameters depend on the shaft diameter itself, the program determines these quantities internally as part of the calculation process. The preliminary calculations in `proof_of_concept` provide a reference for checking the implementation against a simplified, predefined case.

## Limitations

The estimated diameter depends on the accuracy of the input loads, material properties, and design assumptions. The result should be treated as a preliminary engineering estimate and independently verified before using it in an actual shaft design.

## Feedback and Contributions

Although this project was originally developed for MAE 190, I believe there is still room for improvement in both the code and the overall shaft design process. I'm always open to suggestions, feedback, and ideas for improvement!

If you have any recommendations or notice something that could be done better, feel free to reach out or open an issue. I'd love to hear your thoughts and continue improving the project.

## References

- Budynas, R. G., and Nisbett, J. K., *Shigley's Mechanical Engineering Design*. Material properties and reference table data are used from this source.
