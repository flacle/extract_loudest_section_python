# extract_loudest_section_python
This is a Python port of the C++ version of Pete Warden's [extract_loudest_section](https://github.com/petewarden/extract_loudest_section) tool. Distrubuted under the same license.

The extract_loudest_section_python script processes WAV files to extract the loudest segment of a specified length and saves it to a new file. It uses a sliding window approach to efficiently compute the sum of squares of the samples, which is used as a measure of volume.

The main reason for a Python port is that the original repository is an OSX only build ([see Pete's blog for more information](https://petewarden.com/2017/07/17/a-quick-hack-to-align-single-word-audio-recordings/)). Porting it to Python allows for cross-platform usage.

## Features
- Extracts the loudest section of a WAV file.
- Specify desired segment length in milliseconds.
- Skip audio files that are below a minimum volume threshold.
- Process multiple files using glob patterns.

## Prerequisites
- Python 3 (tested on version 3.12.7).
- NumPy (tested on version 2.1.3).
- PySoundFile (tested on version 0.12.1).

All dependencies are listed in the `requirements.txt` file. 

# Installation

1. Clone the repository:

```bash
git clone https://github.com/flacle/extract_loudest_section_python.git
cd extract_loudest_section_python
```

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate.bat
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

# Usage
The script `extract_loudest_section_python.py` can be run from the command line. It requires at least two arguments: an input file path pattern (glob) and an output directory path.

```bash
python extract_loudest_section_python.py <input_glob> <output_directory>
```

## Arguments
- `<input_glob>`: Glob pattern for input WAV files (e.g.,`input/*.wav`) that will match all WAV files in the `data` directory.
- `<output_directory>`: Path to the output directory where the extracted loudest sections (trimmed versions) will be saved.

## Optional Parameters:
You can modify the desired length and minimum volume threshold by editing the variables `desired_length_ms` and `min_volume` in the `main()` function of `extract_loudest_section_python.py`.


# Example
To process the WAV file in the `sample_wav` directory and save the trimmed version to the `sample_trimmed` directory, run the following command:

```bash
python extract_loudest_section_python.py sample_wav/*.wav sample_trimmed
```

## Provided Sample WAV file
This repository contains one sample WAV file from the [LibriSpeech dataset](http://www.openslr.org/12/). The file was originally in flac, and was converted to 16-bit PCM WAV file with a sample rate of 16 kHz, using the following FFmpeg command:

```bash
ffmpeg -i 1688-142285-0000.flac -ar 16000 -acodec pcm_s16le 1688-142285-0000.wav
```

# License
This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

# Acknowledgements
- Pete Warden for the original C++ implementation of the `extract_loudest_section` tool. Original repository: [extract_loudest_section](https://github.com/petewarden/extract_loudest_section).
- [LibriSpeech dataset](http://www.openslr.org/12/) for the sample WAV file.

# Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
