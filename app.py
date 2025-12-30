import streamlit as st
import os
import subprocess
import shutil

st.set_page_config(page_title="LigTopGen", layout="centered")
st.title("LigTopGen: Ligand Topology Generator")
st.markdown("""
Upload a ligand in **.mol2** format to generate topology files using ACPYPE (AmberTools backend).  
Supports: **GROMACS**, **AMBER**, **CHARMM**, **OPLS**, **CNS/XPLOR**.
""")

# File uploader
uploaded_file = st.file_uploader("Upload ligand (.mol2)", type=["mol2"])

temp_dir = "temp_input"
output_dir = "generated_topology"
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

if uploaded_file is not None:
    ligand_path = os.path.join(temp_dir, uploaded_file.name)
    with open(ligand_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Uploaded: {uploaded_file.name}")
    
    # Display basic info (optional: add RDKit preview if you install it)
    st.info("Ready to generate topologies using ACPYPE.")

    if st.button("Generate Topology Files"):
        with st.spinner("Running ACPYPE... This may take 1-2 minutes."):
            try:
                # Clear previous output
                if os.path.exists(output_dir):
                    shutil.rmtree(output_dir)
                os.makedirs(output_dir)

                # Run ACPYPE with all common options
                cmd = [
                    "acpype",
                    "-i", ligand_path,
                    "-o", "all",          # Generate all formats
                    "-f",                 # Force overwrite
                    "-d",                 # Use default charge method (usually AM1-BCC)
                    "-n", "0",            # Net charge (adjust if needed; make selectable later)
                    "-c", "bcc"           # Charge method: bcc = AM1-BCC
                ]

                result = subprocess.run(cmd, capture_output=True, text=True, cwd=output_dir, timeout=300)  # Add timeout
                
                if result.returncode != 0 or "FAILED" in result.stdout or "ERROR" in result.stdout:
                    st.error("ACPYPE failed! See details below:")
                    st.code(result.stdout + "\n" + result.stderr)
                else:
                    st.success("Success!")
                    st.code(result.stdout)
                    # ... rest for downloads

                    # List and offer downloads
                    generated_files = []
                    for root, _, files in os.walk(output_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            generated_files.append((file, file_path))

                    if generated_files:
                        st.markdown("### Download Files:")
                        for name, path in generated_files:
                            with open(path, "rb") as f:
                                st.download_button(
                                    label=name,
                                    data=f,
                                    file_name=name,
                                    mime="text/plain" if name.endswith((".itp", ".top", ".prm", ".frcmod")) else None
                                )
                        
                        # Optional: ZIP all
                        zip_path = "ligand_topologies.zip"
                        shutil.make_archive(zip_path.replace(".zip", ""), 'zip', output_dir)
                        with open(zip_path, "rb") as f:
                            st.download_button("Download All as ZIP", data=f, file_name="ligand_topologies.zip")

            except Exception as e:
                st.error(f"Error: {str(e)}")

# Cleanup button
if st.button("Clear temporary files"):
    for d in [temp_dir, output_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
    st.success("Cleared!")

st.caption("Powered by ACPYPE/AmberTools • Original repo: https://github.com/vijay-vishvakarma/ligtopgen")
