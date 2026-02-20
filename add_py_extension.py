#!/usr/bin/env python3
"""
Add .py extension to all 'categorize' and 'subcat_index' files in level-1 subdirectories.
Usage:
  python add_py_extension.py --root "/Users/my/Online Food Price" --dry-run
  python add_py_extension.py --root "/Users/my/Online Food Price"
"""

import argparse
import os
import shutil
from pathlib import Path
from typing import List

TARGET_FILES = ["categorize", "subcat_index"]

def find_target_files(root: Path) -> List[tuple]:
    """
    Find all target files (without .py) in level-1 subdirectories.
    Targets: 'categorize', 'subcat_index'
    Returns: List of (old_path, new_path) tuples
    """
    targets = []
    
    # Scan only level-1 subdirectories
    try:
        for item in os.listdir(root):
            item_path = root / item
            
            # Only process directories
            if not os.path.isdir(item_path):
                continue
            
            # Check each target file type
            for target_name in TARGET_FILES:
                target_file = item_path / target_name
                target_py_file = item_path / f"{target_name}.py"
                
                # If target exists and .py version doesn't
                if target_file.exists() and not target_py_file.exists():
                    targets.append((target_file, target_py_file))
                elif target_file.exists() and target_py_file.exists():
                    print(f"⚠️  Both exist in {item}: '{target_name}' and '{target_name}.py' (skipping)")
    
    except Exception as e:
        print(f"❌ Error scanning directory: {e}")
    
    return targets

def main() -> int:
    parser = argparse.ArgumentParser(description="Add .py extension to target files")
    parser.add_argument("--root", "-r", default='.', help="Root dir to scan")
    parser.add_argument("--dry-run", action="store_true", help="Only list targets, do not rename")
    args = parser.parse_args()
    
    root = Path(args.root).resolve()
    print(f"🔍 Scanning: {root}")
    print(f"🎲 Target files: {', '.join(TARGET_FILES)}\n")
    
    targets = find_target_files(root)
    
    if not targets:
        print("✅ No target files found to rename.")
        return 0
    
    print(f"🎯 Found {len(targets)} file(s) to rename:\n")
    for old, new in targets:
        print(f"   {old.name} → {new.name}")
        print(f"      {old.parent.name}/")
    
    if args.dry_run:
        print(f"\n🛑 Dry run complete. {len(targets)} file(s) would be renamed.")
        return 0
    
    print(f"\n⏳ Renaming {len(targets)} file(s)...\n")
    
    failures = 0
    for old_path, new_path in targets:
        try:
            shutil.move(str(old_path), str(new_path))
            print(f"✅ {old_path.parent.name}: {old_path.name} → {new_path.name}")
        except Exception as e:
            print(f"❌ {old_path.parent.name}: Failed - {e}")
            failures += 1
    
    print("\n" + "="*50)
    print(f"📊 Done: {len(targets) - failures}/{len(targets)} renamed successfully")
    if failures > 0:
        print(f"   {failures} failed")
    print("="*50)
    
    return 1 if failures else 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
