import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font

# Function to select ligand file
def select_ligand_file():
    file_path = filedialog.askopenfilename(
        title="Select Ligand File",
        filetypes=(("MOL2 files", "*.mol2"), ("All files", "*.*"))
    )
    if file_path:
        ligand_file_entry.delete(0, tk.END)  # Clear previous entry
        ligand_file_entry.insert(0, file_path)

# Function to generate topology
def generate_topology():
    ligand = ligand_file_entry.get()

    if not ligand:
        update_message("Please select a ligand file.")
        return

    output_dir = os.path.dirname(ligand)
    output_basename = os.path.splitext(os.path.basename(ligand))[0]

    try:
        # Path to the AmberTools activation script miniconda3/envs/AmberTools23
        home_dir = os.path.expanduser("~")
        ambertools_activation = os.path.join(home_dir, "miniconda3", "amber.sh")

        # Prepare command to execute acpype
        acpype_executable = "/usr/local/bin/acpype"

        # Prepare command to activate AmberTools and execute acpype
        command = f"source {ambertools_activation} && acpype -i {ligand} -o all"

        # Debug statement to print the command
        update_message(f"Running command: {command}\n")

        # Execute the command and capture output with a timeout of 300 seconds
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=output_dir, executable='/bin/bash')
        try:
            stdout, stderr = process.communicate(timeout=300)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            error_message = "The process timed out."
            update_message(error_message)
            return

        # Debug statement to print the command output
        update_message(f"Command stdout: {stdout.decode()}\n")
        update_message(f"Command stderr: {stderr.decode()}\n")

        # Check return code
        if process.returncode != 0:
            error_message = f"An error occurred during topology generation:\n\n{stderr.decode()}"
            update_message(error_message)
        else:
            success_message = "Topology generation completed successfully."
            update_message(success_message)

    except Exception as e:
        # Display full traceback in message area
        error_message = f"An error occurred during topology generation:\n\n{str(e)}"
        update_message(error_message)

# Function to update message on screen
def update_message(message):
    message_text.config(state=tk.NORMAL)
    message_text.insert(tk.END, message + "\n")
    message_text.config(state=tk.DISABLED)  # Disable editing
    message_text.see(tk.END)  # Scroll to the end of the text

# Create the main application window
root = tk.Tk()
root.title("Ligand Topology Generator")
root.geometry("800x600")  # Increased frame size

# Define larger font
large_font = font.Font(size=12)

# Ligand file selection
tk.Label(root, text="Select Ligand File:", font=large_font).pack(pady=5)
ligand_file_entry = tk.Entry(root, width=70, font=large_font)
ligand_file_entry.pack(pady=5)
tk.Button(root, text="Browse...", command=select_ligand_file, font=large_font).pack(pady=5)

# Generate topology button
tk.Button(root, text="Generate Topology", command=generate_topology, font=large_font).pack(pady=20)

# Message area
message_text = tk.Text(root, height=10, wrap=tk.WORD, state=tk.DISABLED, font=large_font)
message_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Start the Tkinter event loop
root.mainloop()
