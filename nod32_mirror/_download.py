"""
Module for download files from a list of file urls.
"""

import os
from urllib.parse import urlparse
import concurrent.futures
import httpx


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


class Download:
    """
    A class for downloading files from a list of file urls.
    """

    def __init__(
        self,
        urls: list,
        client: httpx.Client,
        target_dir: os.path,
        multidownload: bool = True,
    ) -> None:
        """
        Call needed functions based on the value retrieved from the multidownload variable.
        """
        if multidownload:
            Download.multiple_download(urls, client, target_dir)
        else:
            Download.single_download(urls, client, target_dir)

    @staticmethod
    def single_download(
        urls: list,
        client: httpx.Client,
        target_dir: os.path,
    ) -> None:
        """
        Downloads files from the given list and saves them to the target directory.

        Args:
            urls (list): A list of urls to be downloaded.
            client (httpx.Client): An HTTP client for making requests.
            target_dir (os.path): The target directory to save the downloaded urls.

        Returns:
            None

        Todo:
            logging
        """
        for file in urls:
            file_path = urlparse(file).path
            if file_path.startswith("/"):
                file_path = file_path[1:]
            target_path = os.path.join(target_dir, os.path.basename(file_path))
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "wb") as f:
                f.write(client.get(file).content)

    @staticmethod
    def multiple_download(
        urls: list,
        client: httpx.Client,
        target_dir: os.path,
    ) -> None:
        """
        A function for multiple downloads using concurrent execution.

        Args:
            urls (list): List of urls to be downloaded
            client (httpx.Client): HTTP client for downloading urls
            target_dir (os.path): Target directory for saving the downloaded urls

        Returns:
            None
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for file in urls:
                futures.append(
                    executor.submit(
                        Download.single_download,
                        [file],
                        client,
                        target_dir,
                    )
                )
            for future in concurrent.futures.as_completed(futures):
                future.result()
