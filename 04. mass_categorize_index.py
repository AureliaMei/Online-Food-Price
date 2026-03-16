import os
import subprocess
import sys
from pathlib import Path

def run_script(file_path: Path, python_exec: str, root_dir: Path) -> int:
    """Helper function to execute a python script."""
    print(f"\n🚀 --- Running: {file_path.relative_to(root_dir)} ---")
    
    cmd = [python_exec, str(file_path)]
    try:
        # Run the file with cwd set to its parent directory
        res = subprocess.run(cmd, check=False, cwd=str(file_path.parent))
        if res.returncode == 0:
            print(f"✅ Success: {file_path.name}")
        else:
            print(f"❌ Failed (Exit code {res.returncode}): {file_path.name}")
        return res.returncode
    except Exception as e:
        print(f"⚠️ Error executing {file_path.name}: {e}")
        return 1

def main():
    root_dir = Path(__file__).parent.resolve()
    print(f"🔍 Scanning subdirectories in: {root_dir}")
    
    categorize_targets = []
    index_targets = []
    
    # 1. SCAN DIRECTORIES
    data_dir = root_dir / 'data'
    for subdir in data_dir.iterdir():
        if subdir.is_dir() and not subdir.name.startswith('.'):
            
            for file_path in subdir.iterdir():
                if file_path.is_file():
                    fname = file_path.name.lower()
                    
                    # Prevent runner files from causing infinite loops
                    if "run" in fname:
                        continue
                        
                    # Catch categorize files
                    if "categorize" in fname:
                        categorize_targets.append(file_path)
                        
                    # Catch subcat_index files
                    elif "subcat_index" in fname:
                        index_targets.append(file_path)

    total_targets = len(categorize_targets) + len(index_targets)
    if total_targets == 0:
        print("⚠️ No 'categorize' or 'subcat_index' scripts found in the subdirectories.")
        return

    print(f"\n🎯 Found {len(categorize_targets)} categorize script(s) and {len(index_targets)} index script(s).")
    
    python_exec = sys.executable or "python3"
    failures = 0

    # ==========================================
    # PHASE 1: RUN ALL CATEGORIZE SCRIPTS
    # ==========================================
    if categorize_targets:
        print("\n" + "="*50)
        print("⏳ PHASE 1: Running Categorization Scripts...")
        print("="*50)
        for t in categorize_targets:
            rc = run_script(t, python_exec, root_dir)
            if rc != 0: failures += 1

    # ==========================================
    # PHASE 2: RUN ALL INDEXING SCRIPTS
    # ==========================================
    if index_targets:
        print("\n" + "="*50)
        print("⏳ PHASE 2: Running Subcat Indexing Scripts...")
        print("="*50)
        for t in index_targets:
            rc = run_script(t, python_exec, root_dir)
            if rc != 0: failures += 1

    # ==========================================
    # SUMMARY
    # ==========================================
    print("\n" + "="*60)
    print(f"📊 SUMMARY: Executed {total_targets} file(s) | ✅ {total_targets - failures} passed | ❌ {failures} failed")
    print("="*60)

if __name__ == "__main__":
    main()