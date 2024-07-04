#!/usr/bin/env bash

# Update and install prerequisites
sudo apt-get update
sudo apt-get install -y \
    python3-pmw python3-tk python3-pandas python3-matplotlib python3-numpy python3-openbabel \
    git make csh flex gfortran g++ xorg-dev zlib1g-dev libbz2-dev patch wget

# Function to install Miniconda
install_miniconda() {
    local miniconda_dir="${HOME}/miniconda3"
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
    bash ~/miniconda.sh -b -p "${miniconda_dir}"
    rm ~/miniconda.sh
    eval "$("${miniconda_dir}/bin/conda" shell.bash hook)"
    conda init
    source ~/.bashrc
}

# Function to install AmberTools
install_ambertools() {
    conda install -c conda-forge ambertools
}

# Function to install ACPYPE
install_acpype() {
    git clone https://github.com/alanwilter/acpype.git "${HOME}/acpype"
    sudo ln -s "${HOME}/acpype/run_acpype.py" /usr/local/bin/acpype
}

# Function to install GROMACS
install_gromacs() {
    sudo apt-get install -y gromacs
}


# Function to install PyInstaller
install_pyinstaller() {
    pip install pyinstaller
}

# Main installation function
main() {
    echo "Installing Miniconda..."
    install_miniconda
    echo "Miniconda installation complete."

    echo "Installing AmberTools via Miniconda..."
    install_ambertools
    echo "AmberTools installation complete."

    echo "Installing ACPYPE..."
    install_acpype
    echo "ACPYPE installation complete."

    echo "Installing GROMACS..."
    install_gromacs
    echo "GROMACS installation complete."

    echo "Installing PyInstaller..."
    install_pyinstaller
    echo "PyInstaller installation complete."

    echo "All installations complete. Please restart your terminal or run 'source ~/.bashrc' to apply changes."
}

# Execute the main installation function
main
