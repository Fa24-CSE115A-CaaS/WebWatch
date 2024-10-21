from difflib import unified_diff
import glob
from os import path

def get_latest_file(directory, website_name):

    files = glob.glob(f"{directory}/{website_name}-*.txt")
    if not files:
        return None
    return max(files, key=path.getmtime)


def diffFiles(oldVersionFile, newVersionFile):
    
    try:
        with open(oldVersionFile, 'r') as file1, open(newVersionFile, 'r') as file2:
            oldVersion = file1.readlines()  
            newVersion = file2.readlines()  

        diff = list(unified_diff(oldVersion, newVersion, 
                                fromfile=oldVersionFile, tofile=newVersionFile)) # get differences

        if diff:
            # Write the differnce to a file
            with open("diffVersion.txt", "w") as diffFile:
                diffFile.writelines(diff)
            print("Differences written to diffVersion.txt")
            return True
        else:
            print("No differences found")
            return False
        

    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
        return False
    except OSError as e:
        print(f"File operation failed: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
