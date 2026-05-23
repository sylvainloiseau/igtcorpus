from abc import ABC, abstractmethod
from typing import List, Tuple

class IGTCorpus(ABC):

    @abstractmethod
    def object_languages(self) -> List[str]:
        pass

    @abstractmethod
    def meta_languages(self) -> List[str]:
        pass

    @abstractmethod
    def get_fields(self, level) -> List[Tuple[str, str]]:
        pass

    @abstractmethod
    def get_forms(self, level, field) -> List[str]:
        pass

    @abstractmethod
    def get_distinct_forms(self, level, field) -> List[str]:
        pass

    @abstractmethod
    def get_unit_by_index(self, level, index) -> IGTCorpus:
        pass

    @abstractmethod
    def get_unit_by_id(self, level, id) -> IGTCorpus:
        pass
