# Image Downloader from a list of URLs
This is a Python script tool that allows you to download images from a list of URLs. The URLs can be provided either in a CSV file or a text file. The script will create a directory to save the images if it doesn't already exist. If there are any errors while downloading the images, they will be logged in a file.

## Requirements
- Python 3
- `requests` library

## Usage
```commandline
python img-dl.py file_name [-d output_folder] [-l log.txt]
```

- file_name: Name of the file containing the image URLs (e.g., `links.csv` or `links.txt`).

- `--directory`, `-d`: Name of the directory to save the images (default: image).

- `--log-file`, `-l`: Name of the file to log errors (default: error_log.txt).

## File Formats
The URLs can be provided either in a CSV file or a text file.

### CSV File
The CSV file should have a header row with the column name `image_url`. Optionally, you can also include a `image_name` column with the file name you want to use for the downloaded image.

### Text File
The text file should contain one image URL per line.

## Examples
To download images from a CSV file `image_urls.csv` and save them to the `images` directory:
```commandline
python img-dl.py links.csv -d images
```
To download images from a text file `image_urls.txt` and save them to the `images` directory, logging any errors to `error.log`:

```commandline
python img-dl.py links.txt --d images -l error.log
```