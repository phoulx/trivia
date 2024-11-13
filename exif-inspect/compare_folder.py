"""
比较两个文件夹的内容是否一致
"""

import filecmp
import os

def compare_folders(folder1, folder2):
    # Compare the directories
    comparison = filecmp.dircmp(folder1, folder2)
    
    # Print the differences
    print_differences(comparison)

def print_differences(comparison):
    # Files that are in both directories but differ
    diff_files = [file for file in comparison.diff_files if os.path.splitext(file)[0] not in comparison.same_files]
    if diff_files:
        print("Differing files:", diff_files)
    
    # Files that are only in folder1
    left_only = [file for file in comparison.left_only if os.path.splitext(file)[0] not in [os.path.splitext(f)[0] for f in comparison.right_only]]
    if left_only:
        print("Files only in folder1:", left_only)
    
    # Files that are only in folder2
    right_only = [file for file in comparison.right_only if os.path.splitext(file)[0] not in [os.path.splitext(f)[0] for f in comparison.left_only]]
    if right_only:
        print("Files only in folder2:", right_only)
    
    # Recursively compare subdirectories
    for subdir in comparison.subdirs.values():
        print_differences(subdir)

# Example usage
folder1 = '/Users/ph/repos/trivia/adjusted/GT-S5830/'
folder2 = '/Users/ph/Desktop/tmp/'
compare_folders(folder1, folder2)