#!/bin/bash

# Define the file path
file_path="challenge/app/model.h5"

# Function to split the file into two halves
split_file_half() {
    # Ensure the file exists
    if [[ ! -f "$file_path" ]]; then
        echo "Error: $file_path not found!"
        exit 1
    fi

    # Get the total size of the file in bytes
    file_size=$(stat --format=%s "$file_path")

    # Calculate the half size of the file
    half_size=$(($file_size / 2))

    # Split the file into two parts using split
    echo "Splitting $file_path into two parts..."

    split -b $half_size "$file_path" "${file_path}_part_"

    echo "File split into two parts: ${file_path}_part_aa and ${file_path}_part_ab"
}

# Function to combine the file
combine_files() {
    echo "Combining parts into $file_path..."

    # Combine the parts using cat
    cat "${file_path}_part_aa" "${file_path}_part_ab" > "$file_path"

    echo "Files combined into $file_path."
}

# Main logic to check if we are splitting or combining
if [[ $# -lt 1 ]]; then
    echo "Usage:"
    echo "  To split: $0 split"
    echo "  To combine: $0 combine"
    exit 1
fi

# Command-line argument logic
command="$1"
shift

case "$command" in
    split)
        split_file_half
        ;;
    
    combine)
        combine_files
        ;;
    
    *)
        echo "Invalid command: $command"
        echo "Usage: $0 {split|combine}"
        exit 1
        ;;
esac

    echo "  To combine: $0 combine"
    exit 1
fi

# Command-line argument logic
command="$1"
shift

case "$command" in
    split)
        split_file_half
        ;;
    
    combine)
        combine_files
        ;;
    
    *)
        echo "Invalid command: $command"
        echo "Usage: $0 {split|combine}"
        exit 1
        ;;
esac
