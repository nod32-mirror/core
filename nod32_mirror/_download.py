"""
Module for download files from a list of file paths.
"""

import os
from urllib.parse import urlparse
import concurrent.futures
import httpx


class Download:
    """
    A class for downloading files from a list of file paths.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        files: list,
        client: httpx.Client,
        target_dir: os.path,
        save_structure: bool = True,
        multidownload: bool = True,
    ) -> None:
        """
        Call needed functions based on the value retrieved from the multidownload variable.
        """
        if multidownload:
            Download.multiple_download(files, client, target_dir, save_structure)
        else:
            Download.single_download(files, client, target_dir, save_structure)

    @staticmethod
    def single_download(
        files: list,
        client: httpx.Client,
        target_dir: os.path,
        save_structure: bool = True,
    ) -> None:
        """
        Downloads files from the given list and saves them to the target directory.

        Args:
            files (list): A list of files to be downloaded.
            client (httpx.Client): An HTTP client for making requests.
            target_dir (os.path): The target directory to save the downloaded files.
            save_structure (bool): A boolean flag that determines whether to save the downloaded
                                   files in their original structure or not.

        Returns:
            None

        Todo:
            logging
        """
        for file in files:
            file_path = urlparse(file).path
            if file_path.startswith("/"):
                file_path = file_path[1:]
            if save_structure:
                target_path = os.path.join(target_dir, file_path)
            else:
                target_path = os.path.join(target_dir, os.path.basename(file_path))
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "wb") as f:
                f.write(client.get(file).content)

    @staticmethod
    def multiple_download(
        files: list,
        client: httpx.Client,
        target_dir: os.path,
        save_structure: bool = True,
    ) -> None:
        """
        A function for multiple downloads using concurrent execution.

        Args:
            files (list): List of files to be downloaded
            client (httpx.Client): HTTP client for downloading files
            target_dir (os.path): Target directory for saving the downloaded files
            save_structure (bool): A boolean flag that determines whether to save
                                   the downloaded files in their original structure or not.

        Returns:
            None
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for file in files:
                futures.append(
                    executor.submit(
                        Download.single_download,
                        [file],
                        client,
                        target_dir,
                        save_structure,
                    )
                )
            for future in concurrent.futures.as_completed(futures):
                future.result()
