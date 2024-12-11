import os

def verify_files(*file_paths):
    verified = True
    r"""
    Verifies if the specified files exist.
    
    Args:
        file_paths: List of file paths to verify.

    Returns:
        None. Prints the result for each file path.

    """
    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"File exists: {file_path}")
        else:
            print(f"File missing: {file_path}")
            verified = False
    if not verified:
        print("Verification failed.")
        return False
    print("Verification successful.")
    return True
