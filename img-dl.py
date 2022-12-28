import argparse
import csv
import os
import requests


def download_image(url, directory, image_name=None):
    """Download an image from the given URL and save it to the specified directory.

    If image_name is not provided, the original file name from the URL is used.
    """
    response = requests.get(url, allow_redirects=True)
    if not response.ok:
        raise Exception(f"Error: Could not download image from URL {url}")
    file_name, file_ext = os.path.splitext(url.split("/")[-1])
    if image_name:
        file_name = image_name
    file_path = os.path.join(directory, file_name + file_ext)
    with open(file_path, "wb") as f:
        f.write(response.content)
    return file_name, file_ext, url, response.url


def read_csv(file_name):
    """Read a CSV file and return the rows as a list of dictionaries."""
    with open(file_name, "r") as csv_file:
        column_names = next(csv_file).strip().split(",")
        reader = csv.DictReader(csv_file, fieldnames=column_names)
        return list(reader)


def read_text(file_name):
    """Read a text file and return the lines as a list."""
    with open(file_name, "r") as txt_file:
        return txt_file.read().strip().split("\n")


def main(file_name, directory, log_file):
    """Download images from the given file and save them to the specified directory."""
    # Check file extension to determine how to read the file
    file_extension = os.path.splitext(file_name)[1]
    if file_extension == ".csv":
        rows = read_csv(file_name)
    else:
        rows = [({"image_url": url}) for url in read_text(file_name)]
    num_rows = len(rows)

    # Create the output directory if it doesn't already exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Open the log file for writing
    with open(log_file, "w") as log:
        skipped_urls = []
        for i, row in enumerate(rows):
            try:
                image_name = row.get("image_name")
                file_name, file_ext, original_url, final_url = download_image(row["image_url"], directory, image_name)
                print(f"Downloaded image {i+1} of {num_rows}: {file_name}{file_ext}")
            except Exception as e:
                log.write(f"{i+1}, {row['image_url']}, {e}\n")
                print(f"Error: {e}")
                skipped_urls.append(i+1)
        if skipped_urls:
            print(f"Skipped URLs at row(s): {', '.join(str(i) for i in skipped_urls)}")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="name of the file containing the image URLs")
    parser.add_argument("--directory", "-d", default="image", help="name of the directory to save the images")
    parser.add_argument("--log-file", "-l", default="error_log.txt", help="name of the file to log errors")
    args = parser.parse_args()

    main(args.file_name, args.directory, args.log_file)
