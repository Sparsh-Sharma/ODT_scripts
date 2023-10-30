# ODT Data Post-Processing Python Scripts

This repository contains Python scripts designed for post-processing ODT ([One Dimensional Turbulence](https://doi.org/10.1063/5.0101270)) data. The scripts offer user-friendly and efficient ways to perform data analysis, extraction, and transformation on ODT files. Whether you're working with text documents, reports, or any ODT data, these scripts will assist in automating tasks and streamlining your workflow.

## Scripts

### Script 1: Velocity Field Visualizer

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)

#### Description

This Python script processes and visualizes velocity field data from a collection of `.dat` files. It offers the following features:

- Data extraction and manipulation.
- Customizable color mapping for visualizing velocity.
- Export the visualized velocity field as a PDF file.
- Detailed comments for easy understanding.

#### Usage

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/Sparsh-Sharma/ODT_scripts.git
   ```

2. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

3. Run the script, providing the directory containing the `.dat` files and the file prefix.

   ```shell
   python VelField_OneRlz.py --input_dir path/to/input/odt/files --file_prefix data_00700
   ```

4. The script will process the ODT data, visualize the velocity field, and save it as a PDF file.

### Script 2: Ensemble Average Velocity Field Visualizer

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)

#### Description

This Python script calculates and visualizes the ensemble average velocity field based on data from multiple simulation directories. Key features include:

- Data extraction, ensemble averaging, and visualization.
- Customizable color mapping for visualizing velocity.
- Export the ensemble average velocity field as a PDF file.
- User-friendly with detailed comments.

#### Usage

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/Sparsh-Sharma/ODT_scripts.git
   ```

2. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

3. Run the script, providing the base directory containing simulation data and the number of ensembles.

   ```shell
   python avgVelField_MultRlz.py --base_dir path/to/simulation/data --num_ensembles 5
   ```

4. The script will calculate the ensemble average, visualize the velocity field, and save it as a PDF file.

### Script 3: Ensemble Average & TKE Visualizer

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)

#### Description

This Python script calculates the ensemble average velocity field and visualizes the mean A field based on data from 'data_' directories within a specified base directory. Key features include:

- Data extraction, ensemble averaging, and visualization.
- Customizable color mapping for visualizing the mean A field.
- Export the ensemble average velocity field and mean A field as high-resolution PDF files.
- User-friendly with detailed comments.

#### Usage

1. Clone this repository to your local machine.

2. Install the required Python packages:

   ```shell
   pip install -r requirements.txt
   ```

3. Run the script, providing the base directory containing simulation data.

   ```shell
   python script3.py
   ```

4. The script will calculate the ensemble average velocity field and TKE field, visualize them, and save as PDF files.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Author

- Sparsh Sharma
- sparsh.sharma@dlr.de
- DLR Braunschweig

## Citation

If you find these scripts helpful in your research related to one-dimensional turbulence (ODT), please consider citing our paper:

- [Title of Your Paper](https://doi.org/10.1063/5.0101270)
- Author(s): Your Name(s)
- Published in: Journal Name
- DOI: [https://doi.org/10.1063/5.0101270](https://doi.org/10.1063/5.0101270)
---

Feel free to customize the content, add more sections, or provide further details about each script as needed.
```
