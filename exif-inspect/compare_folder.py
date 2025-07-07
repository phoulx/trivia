"""
比较两个文件夹的内容是否一致
"""

import filecmp
import os

def compare_folders(folder1, folder2, ignore_extension=False):
    # Compare the directories
    comparison = filecmp.dircmp(folder1, folder2)
    
    # Print the differences
    print_differences(comparison, ignore_extension)

def print_differences(comparison, ignore_extension=False):
    # Files that are in both directories but differ
    if ignore_extension:
        # Compare without extensions
        same_files_no_ext = {os.path.splitext(f)[0] for f in comparison.same_files}
        diff_files = [f for f in comparison.diff_files if os.path.splitext(f)[0] not in same_files_no_ext]
    else:
        diff_files = comparison.diff_files
    if diff_files:
        print("Differing files:", diff_files)
    
    # Files that are only in folder1
    if ignore_extension:
        right_files_no_ext = {os.path.splitext(f)[0] for f in comparison.right_list}
        left_only = [f for f in comparison.left_only if os.path.splitext(f)[0] not in right_files_no_ext]
    else:
        left_only = comparison.left_only
    if left_only:
        print("Files only in folder1:", left_only)
    
    # Files that are only in folder2
    if ignore_extension:
        left_files_no_ext = {os.path.splitext(f)[0] for f in comparison.left_list}
        right_only = [f for f in comparison.right_only if os.path.splitext(f)[0] not in left_files_no_ext]
    else:
        right_only = comparison.right_only
    if right_only:
        print("Files only in folder2:", right_only)
    
    # Recursively compare subdirectories
    for subdir in comparison.subdirs.values():
        print_differences(subdir, ignore_extension)

# Example usage
folder1 = '/Users/ph/Documents/Screenshots/Xperia/'
folder2 = '/Volumes/Extreme/reorgnizing documents/Mobile/Screenshots/Xperia/'
compare_folders(folder1, folder2, ignore_extension=False)  # Set to False to consider extensions