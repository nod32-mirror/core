"""
Module for download files from a list of file urls.
"""

import os
from urllib.parse import urlparse
import concurrent.futures
import httpx
from loguru import logger


def download_file(
    url: str,
    client: httpx.Client,
    target_path: os.path,
) -> None:
    """
    Download a file from the given URL and save it to the target path.

    Args:
        url (str): The URL of the file to be downloaded.
        client (httpx.Client): The HTTP client used to make the request.
        target_path (os.path): The path where the downloaded file will be saved.

    Returns:
        None
    """
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "wb") as f:
        f.write(client.get(url).content)

def single_download(
    urls: list,
    client: httpx.Client,
    target_dir: os.path,
) -> tuple:
    """
    Downloads files from the given list and saves them to the target directory.

    Args:
        urls (list): A list of urls to be downloaded.
        client (httpx.Client): An HTTP client for making requests.
        target_dir (os.path): The target directory to save the downloaded urls.

    Returns:
        tuple: A tuple of two integers: the number of downloaded files and the
               number of skipped files.

    Todo:
        logging
    """
    downloaded = 0
    skipped = 0
    for file in urls:
        file_path = urlparse(file).path
        if file_path.startswith("/"):
            file_path = file_path[1:]
        filesize = int(client.head(file).headers["Content-Length"])
        target_path = os.path.join(target_dir, file_path)
        if os.path.exists(target_path) and os.path.getsize(target_path) == filesize:
            skipped += 1
            continue
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "wb") as f:
            f.write(client.get(file).content)
        downloaded += 1

    return downloaded, skipped


def multiple_download(
    urls: list,
    client: httpx.Client,
    target_dir: os.path,
    max_workers: int = 20,
) -> tuple:
    """
    A function for multiple downloads using concurrent execution.

    Args:
        urls (list): List of urls to be downloaded
        client (httpx.Client): HTTP client for downloading urls
        target_dir (os.path): Target directory for saving the downloaded urls

    Returns:
        tuple: A tuple of two integers: the number of downloaded files and the
               number of skipped files.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for file in urls:
            futures.append(
                executor.submit(
                    single_download,
                    [file],
                    client,
                    target_dir,
                )
            )
        downloaded = 0
        skipped = 0
        try:
            for future in concurrent.futures.as_completed(futures):
                d, s = future.result()
                downloaded += d
                skipped += s
        except Exception as e:
            print(f"\nCaught {e}, terminating threads...")
            executor.shutdown(wait=False, cancel_futures=True)
            raise
    return downloaded, skipped
