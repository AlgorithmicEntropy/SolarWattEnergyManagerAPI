from abc import ABC, abstractmethod

class BaseClient(ABC):
    """
    Base class for API clients.
    """
    @abstractmethod
    def test_connection(self):
        """
        Test the connection to the API.
        """

    @abstractmethod
    def fetch_data_json(self):
        """
        Fetch data from the API as json.
        """
