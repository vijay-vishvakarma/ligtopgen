topology generator tool:

# Ligand Topology Generator

This project provides a graphical user interface (GUI) to generate topology files for ligands using ACPYPE and AmberTools. The setup script will install all necessary dependencies and create an executable for the tool.

## Prerequisites

Before running the setup script, ensure you have the following installed on your system:

- Bash shell
- Superuser (sudo) privileges

## Setup Instructions

1. **Download the Script**

   Save the setup to your local machine.

2. **Run the Script Executable**

   Open your terminal and navigate to the directory where you saved the script. Run the following command to make the script executable:
   
   cd ligtopgen
   
   sudo chmod +x install_tools.sh
   
   ./install_tools.sh

The script will install:

    Install Miniconda
    Install AmberTools
    Install ACPYPE
    Install GROMACS
    Install PyInstaller

After the script completes, restart your terminal.
Generate Executable

Once the dependencies are installed, you can use PyInstaller to generate an executable for the ligand topology generator script. Run the following commands:

bash

    pyinstaller topology_generator.spec

    
This will create a standalone executable named ligtopgen in the dist directory.

    mv ./dist/ligtopgen /usr/local/bin/ligtopgen
    chmod +x /usr/local/bin/ligtopgen
    
Usage

    Launch the Ligand Topology Generator, just type on terminal
    
    ligtopgen
    
You can also add an alias to your .bashrc file for easier access:

bash

echo "export ligtopgen=~/dist/ligtopgen" >> ~/.bashrc
source ~/.bashrc

Then you can run the executable using:

bash

    ligtopgen

    Select Ligand File
        Click on the "Browse..." button to select your ligand file (in .mol2 format).

    Generate Topology
        Click on the "Generate Topology" button to start the topology generation process.
        The output and any messages will be displayed in the message area.

Troubleshooting

    Ensure that you have selected a valid ligand file in .mol2 format.
    Check that all dependencies are correctly installed by re-running the setup script if necessary.
    If the topology generation fails, check the message area for error details.

License

This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgements

    ACPYPE
    AmberTools
    GROMACS
