import os
from datetime import datetime

from typing import Any, Set, Dict, Tuple, Union, Type, Collection


class MicexISSDataHandler:
    """ Data handler which will be called
    by the ISS client to handle downloaded data.
    """

    def __init__(self, container: Type):
        """ The handler will have a container to store received data.
        """
        self.container = container()

    def process_the_data(self, market_data: Any):
        """ This handler method should be overridden to perform
        the processing of data returned by the server.
        """
        pass


class CSVHandler(MicexISSDataHandler):
    """ This handler for perform csv or parquet file.
    """

    def process_the_data(self, moex_data: Any):
        """ Write chunks of data into file.
        """
        with open(self.container.filepath, 'a') as file:
            for line in moex_data:
                file.write(line + '\n')


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

    def set_filepath(self, filepath: str):
        self.filepath = filepath
        if self.filepath is None:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            filepath = f"{current_time}.csv"
            self.set_filepath(filepath=filepath)
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


class SQLContainer:
    pass


class DFContainer:
    pass
