
"""
extract_loudest_section_python.py

This script processes WAV files to extract the loudest segment of a specified length and saves it to a new file.
It uses a sliding window approach to efficiently compute the sum of squares of the samples, which is used as a measure of volume.

This is a port of the original repository written in C++ by Pete Warden: https://github.com/petewarden/extract_loudest_section
The original C++ code is licensed under the Apache 2.0 license and the same license applies to this Python port.

Author: Francis Lacle
License: Apache 2.0

Functions:
    trim_to_loudest_segment(input_samples, desired_samples)
    trim_to_loudest_segment_indices(input_samples, desired_samples)
    trim_file(input_filename, output_filename, desired_length_ms, min_volume)
    main()
"""

import sys
import os
import glob
import numpy as np
import soundfile as sf

def trim_to_loudest_segment(input_samples, desired_samples):
    """
    Finds the loudest segment of a given length within an array of audio samples.

    Args:
        input_samples (list or np.ndarray): The input array of audio samples.
        desired_samples (int): The length of the segment to find.

    Returns:
        tuple: A tuple containing the start and end indices of the loudest segment.
               If the desired segment length is greater than or equal to the input length,
               returns (0, input_size).
    """
    input_size = len(input_samples)
    if desired_samples >= input_size:
        return 0, input_size

    # Compute initial volume sum over the first window
    current_volume_sum = np.sum(np.square(input_samples[0:desired_samples]))
    loudest_volume = current_volume_sum
    loudest_start_index = 0

    for i in range(1, input_size - desired_samples + 1):
        trailing_value = input_samples[i - 1]
        leading_value = input_samples[i + desired_samples - 1]
        current_volume_sum -= trailing_value * trailing_value
        current_volume_sum += leading_value * leading_value

        if current_volume_sum > loudest_volume:
            loudest_volume = current_volume_sum
            loudest_start_index = i

    loudest_end_index = loudest_start_index + desired_samples
    return loudest_start_index, loudest_end_index

def trim_to_loudest_segment_indices(input_samples, desired_samples):
    """
    Finds the indices of the loudest segment in the input samples.

    This function calculates the loudest segment of a given length within an array of input samples.
    It uses a sliding window approach to efficiently compute the sum of squares of the samples,
    which is used as a measure of volume.

    Args:
        input_samples (list or np.ndarray): The input audio samples.
        desired_samples (int): The number of samples in the desired loudest segment.

    Returns:
        tuple: A tuple containing the start and end indices of the loudest segment.
               The end index is exclusive.
    """
    input_size = len(input_samples)
    if desired_samples >= input_size:
        return 0, input_size

    current_volume_sum = np.sum(np.square(input_samples[0:desired_samples]))
    loudest_volume = current_volume_sum
    loudest_start_index = 0

    for i in range(1, input_size - desired_samples + 1):
        trailing_value = input_samples[i - 1]
        leading_value = input_samples[i + desired_samples - 1]
        current_volume_sum -= trailing_value * trailing_value
        current_volume_sum += leading_value * leading_value

        if current_volume_sum > loudest_volume:
            loudest_volume = current_volume_sum
            loudest_start_index = i

    loudest_end_index = loudest_start_index + desired_samples
    return loudest_start_index, loudest_end_index

def trim_file(input_filename, output_filename, desired_length_ms, min_volume):
    """
    Trims a WAV file to the loudest segment of a specified length and saves it to a new file.

    Parameters:
    input_filename (str): Path to the input WAV file.
    output_filename (str): Path to save the trimmed WAV file.
    desired_length_ms (int): Desired length of the trimmed segment in milliseconds.
    min_volume (float): Minimum average volume threshold for the segment to be saved.

    Returns:
    None
    """
    try:
        # Read the WAV file; always return data as 2D array (even if mono)
        wav_samples, sample_rate = sf.read(input_filename, always_2d=True, dtype='float32')
    except Exception as e:
        print(f"Failed to decode '{input_filename}' as a WAV: {e}")
        return

    # Create a mono version for analysis
    mono_samples = wav_samples.mean(axis=1)

    desired_samples = int((desired_length_ms * sample_rate) / 1000)

    # Get indices of the loudest segment
    start_idx, end_idx = trim_to_loudest_segment_indices(mono_samples, desired_samples)

    # Compute average volume of the segment
    trimmed_mono_samples = mono_samples[start_idx:end_idx]
    average_volume = np.mean(np.abs(trimmed_mono_samples))

    if average_volume < min_volume:
        print(f"Skipped '{input_filename}' as too quiet ({average_volume})")
        return

    # Extract the corresponding segment from the original samples (preserving all properties)
    trimmed_samples = wav_samples[start_idx:end_idx, :]

    try:
        # Write the trimmed samples without any modifications
        sf.write(output_filename, trimmed_samples, sample_rate)
        print(f"Saved to '{output_filename}'")
    except Exception as e:
        print(f"Failed to write '{output_filename}': {e}")

def main():
    """
    Main function to process input WAV files and extract the loudest section.

    This function expects at least two command-line arguments: the input file path pattern (glob) 
    and the output directory path. It processes each input file, extracts the loudest section 
    of a specified length, and saves it to the output directory.

    Command-line arguments:
    sys.argv[1] (str): Glob pattern for input WAV files.
    sys.argv[2] (str): Path to the output directory.

    Returns:
    int: Returns 0 on success, -1 if the required arguments are not provided.
    """
    if len(sys.argv) < 3:
        print("You must supply paths to input and output wav files as arguments")
        return -1

    input_glob = sys.argv[1]
    input_filenames = glob.glob(input_glob)
    output_root = sys.argv[2]
    output_filenames = []
    output_dirs = set()

    for input_filename in input_filenames:
        _, input_base = os.path.split(input_filename)
        output_filename = os.path.join(output_root, input_base)
        output_filenames.append(output_filename)
        output_dir = os.path.dirname(output_filename)
        output_dirs.add(output_dir)

    for output_dir in output_dirs:
        os.makedirs(output_dir, exist_ok=True)

    assert len(input_filenames) == len(output_filenames)
    for input_filename, output_filename in zip(input_filenames, output_filenames):
        desired_length_ms = 1000  # 1 second
        min_volume = 0.004
        trim_file(input_filename, output_filename, desired_length_ms, min_volume)

    return 0

if __name__ == "__main__":
    main()