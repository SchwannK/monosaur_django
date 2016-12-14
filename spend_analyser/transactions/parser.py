from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def read_transactions(self, file, session_id):
        pass
