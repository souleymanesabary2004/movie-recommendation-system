"""
Pipeline Orchestrator
Step 3.2.5: Simple scheduler to run all ETL scripts in the correct order
"""

import subprocess
import time
import sys

# Configuration
SCRIPTS = [
    # INGESTION
    ("src/ingestion/ingest_movies.py", "Ingesting movies"),
    ("src/ingestion/ingest_ratings.py", "Ingesting ratings"),
    
    # CLEANING
    ("src/processing/clean_movies.py", "Cleaning movies"),
    ("src/processing/clean_ratings.py", "Cleaning ratings"),
    
    # TRANSFORMATION
    ("src/processing/transform_ratings.py", "Transforming ratings"),
    ("src/processing/transform_movies.py", "Transforming movies")
]

def run_script(script_path, description):
    """Execute a Python script and return success/failure"""
    print(f"\n{'='*60}")
    print(f" Running: {description}")
    print(f" Script: {script_path}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Run the script
        result = subprocess.run([sys.executable, script_path], 
                               capture_output=True, 
                               text=True)
        
        # Print output
        if result.stdout:
            print("\n OUTPUT:")
            print(result.stdout)
        
        if result.stderr:
            print("\n ERRORS/WARNINGS:")
            print(result.stderr)
        
        # Check if successful
        if result.returncode == 0:
            elapsed = time.time() - start_time
            print(f"\n SUCCESS: {description} completed in {elapsed:.2f} seconds")
            return True
        else:
            print(f"\n FAILED: {description} (return code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"\n EXCEPTION: {e}")
        return False

def main():
    """Main pipeline orchestrator"""
    print("="*60)
    print(" MOVIE RECOMMENDATION SYSTEM - ETL PIPELINE")
    print("="*60)
    print(f"Starting pipeline at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.executable}")
    print("="*60)
    
    start_time = time.time()
    success_count = 0
    
    for script_path, description in SCRIPTS:
        if run_script(script_path, description):
            success_count += 1
        else:
            print(f"\n Pipeline stopped at: {description}")
            break
    
    elapsed = time.time() - start_time
    print("\n" + "="*60)
    print(f" PIPELINE SUMMARY")
    print("="*60)
    print(f" Successful steps: {success_count}/{len(SCRIPTS)}")
    print(f"  Total time: {elapsed:.2f} seconds")
    print(f" Finished at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

if __name__ == "__main__":
    main()