import sys
import os
import gzip
import lzma
import shutil

def compress_files(file_paths, compressed_folder, compression_function):
    os.makedirs(compressed_folder, exist_ok=True)
    for file_path in file_paths:
        with open(file_path, 'rb') as f_in:
            with compression_function(os.path.join(compressed_folder, f"{os.path.basename(file_path)}.compressed"), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def decompress_files(compressed_folder, decompressed_folder, decompression_function):
    os.makedirs(decompressed_folder, exist_ok=True)
    for compressed_file in os.listdir(compressed_folder):
        compressed_path = os.path.join(compressed_folder, compressed_file)
        with decompression_function(compressed_path, 'rb') as f_in:
            decompressed_path = os.path.join(decompressed_folder, os.path.splitext(compressed_file)[0])
            with open(decompressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def calculate_loss(original_file, decompressed_file):
    original_size = os.path.getsize(original_file)
    decompressed_size = os.path.getsize(decompressed_file)
    return original_size - decompressed_size

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py file1 file2 file3")
        sys.exit(1)

    # Get the list of input files from command-line arguments
    files_to_compress = sys.argv[1:]

    # Folder for compressed files using gzip
    compressed_folder_gzip = 'compressed_files_gzip'
    compress_files(files_to_compress, compressed_folder_gzip, gzip.open)

    # Folder for decompressed files using gzip
    decompressed_folder_gzip = 'decompressed_files_gzip'
    decompress_files(compressed_folder_gzip, decompressed_folder_gzip, gzip.open)

    # Folder for compressed files using lzma
    compressed_folder_lzma = 'compressed_files_lzma'
    compress_files(files_to_compress, compressed_folder_lzma, lzma.open)

    # Folder for decompressed files using lzma
    decompressed_folder_lzma = 'decompressed_files_lzma'
    decompress_files(compressed_folder_lzma, decompressed_folder_lzma, lzma.open)

    # Calculate and print loss for each file using gzip
    print("Losses using gzip:")
    for original_file in files_to_compress:
        decompressed_file = os.path.join(decompressed_folder_gzip, f"{os.path.basename(original_file)}")
        loss = calculate_loss(original_file, decompressed_file)
        print(f"Loss for {os.path.basename(original_file)}: {loss} bytes")

    # Calculate and print loss for each file using lzma
    print("\nLosses using lzma:")
    for original_file in files_to_compress:
        decompressed_file = os.path.join(decompressed_folder_lzma, f"{os.path.basename(original_file)}")
        loss = calculate_loss(original_file, decompressed_file)
        print(f"Loss for {os.path.basename(original_file)}: {loss} bytes")

    # Clean up: Remove the compressed and decompressed folders
    shutil.rmtree(compressed_folder_gzip)
    shutil.rmtree(decompressed_folder_gzip)
    shutil.rmtree(compressed_folder_lzma)
    shutil.rmtree(decompressed_folder_lzma)
