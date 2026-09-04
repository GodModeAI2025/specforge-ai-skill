#!/usr/bin/env python3
"""
CI/CD Baseline Validator for SpecForge

This script statically validates the existence and basic integrity of the 
essential SpecForge governance files within a repository. It is designed 
to be run in a CI/CD pipeline (e.g., GitHub Actions, GitLab CI).

It deliberately avoids any hardcoded local paths and works entirely relative 
to the repository root from which it is executed.

Usage:
  python3 ci_validate_baseline.py
"""

import os
import sys
import json

def error(msg):
    print(f"❌ ERROR: {msg}", file=sys.stderr)
    return False

def success(msg):
    print(f"✅ PASS: {msg}")
    return True

def validate_baseline():
    repo_root = os.getcwd()
    print(f"Starting SpecForge baseline validation in: {repo_root}")
    
    all_passed = True
    
    # 1. Check constitution.md
    # We expect a constitution.md somewhere. Common places are the root, docs/, or an architecture folder.
    # We will search for it, or require it to be configured in specforge.json.
    
    # 2. Check specforge.json
    config_path = os.path.join(repo_root, 'specforge.json')
    if not os.path.isfile(config_path):
        all_passed = error("specforge.json not found in repository root. This file is required for automated gating.")
        config_data = {}
    else:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            success("specforge.json is valid JSON.")
            
            # Check basic schema
            if "profile" not in config_data:
                all_passed = error("specforge.json is missing the required 'profile' field.")
            else:
                success(f"Configured profile: {config_data['profile']}")
                
        except json.JSONDecodeError as e:
            all_passed = error(f"specforge.json contains invalid JSON: {e}")
            config_data = {}

    # 3. Find and check constitution.md
    constitution_path = config_data.get('paths', {}).get('constitution', 'constitution.md')
    full_const_path = os.path.join(repo_root, constitution_path)
    
    if not os.path.isfile(full_const_path):
        # Fallback search if not at explicit path
        found = False
        for root, dirs, files in os.walk(repo_root):
            if '.git' in dirs:
                dirs.remove('.git')
            if 'constitution.md' in files:
                full_const_path = os.path.join(root, 'constitution.md')
                found = True
                break
        
        if not found:
            all_passed = error("constitution.md not found. A Single Source of Truth for architecture principles must exist.")
        else:
            success(f"Found constitution.md at {os.path.relpath(full_const_path, repo_root)}")
    else:
        success(f"Found constitution.md at configured path: {constitution_path}")

    # 4. If constitution.md exists, do a light heuristic check
    if os.path.isfile(full_const_path):
        with open(full_const_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            if 'principle' not in content and 'prinzip' not in content:
                print("⚠️ WARNING: constitution.md seems to lack defined principles.")
            
            # Context Graph Traceability soft-check: Are there links to other docs?
            if '][' not in content and '](' not in content and '[[' not in content:
                print("⚠️ WARNING: constitution.md contains no links. Consider adopting a Context Graph approach by linking your specs and architecture docs.")

    if all_passed:
        print("\n✨ All SpecForge baseline checks passed. Repository is ready for execution.")
        sys.exit(0)
    else:
        print("\n🚨 SpecForge baseline checks failed. Please fix the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    validate_baseline()