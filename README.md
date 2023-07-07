# Convert SRT to TTML

This script converts SRT subtitle files to TTML format using Python.

## Usage

1. Make sure you have Python installed on your system.
2. Clone this repository or download the script file.
3. Open a terminal or command prompt and navigate to the directory where the script is located.
4. Run the following command:


5. The script will start converting SRT files to TTML format recursively in the specified directory.
6. Converted TTML files will be generated in the same directory as the corresponding SRT files.
7. Permissions for the generated TTML files will be set to 775.
8. If any SRT file encounters an encoding error, the path of the file will be logged in the specified error.log file.

## Configuration

You can modify the following parameters in the script according to your requirements:

- `root_directory`: The root directory where the script will search for SRT files. Update this to your desired directory.
- `language`: The language code for the subtitles. Update this to the appropriate language code.
- `log_file`: The path of the error log file where the paths of SRT files with encoding errors will be logged. Update this to your desired log file path.

## Requirements

The script requires the following dependencies:

- Python 3.x

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
