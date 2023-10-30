# ODT Data Post-Processing Python Scripts

This repository contains Python scripts designed for post-processing ODT (Open Document Text) data. The scripts offer user-friendly and efficient ways to perform data analysis, extraction, and transformation on ODT files. Whether you're working with text documents, reports, or any ODT data, these scripts will assist in automating tasks and streamlining your workflow.

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

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Author

- Sparsh Sharma
- sparsh.sharma@dlr.de
- DLR Braunschweig

---

Feel free to customize the content, add more sections, or provide further details about each script as needed.
