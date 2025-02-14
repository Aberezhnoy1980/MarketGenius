import os
from datetime import datetime

from moex_api.iss_client import MicexISSDataHandler
from typing import Any, Set, Dict, Tuple, Union, Type, Collection


class CSVHandler(MicexISSDataHandler):
    """ This handler for perform csv or parquet file.
    """

    def process_the_data(self, moex_data: Any):
        """ Write chunks of data into file.
        """
        self.container.write_data(moex_data)


class SQLHandler(MicexISSDataHandler):
    pass


class DFHandler(MicexISSDataHandler):
    pass


class CSVContainer:
    """ Container that will be used by the handler to store data in csv or parquet file.
    Kept separately from the handler for scalability purposes: in order
    to differentiate storage and output from the processing.
    """

    def __init__(self):
        self.filepath = None

    def write_file(self, content: Collection):
        if self.filepath is None:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filepath = f"unknown_{current_time}.csv"
            self.set_pathfile(filepath=filepath)
        else:
            if os.path.exists(self.filepath):
                base_name, ext = os.path.splitext(self.filepath)
                count = 1
                while True:
                    new_file_name = f"{base_name} ({count}){ext}"
                    if not os.path.exists(new_file_name):
                        self.filepath = new_file_name
                        break
                    count += 1
            with open(self.filepath, 'a') as file:
                for line in content:
                    file.write(line + '\n')

    def set_pathfile(self, filepath: str) -> None:
        self.filepath = filepath


class SQLContainer:
    pass


class DFContainer:
    pass
