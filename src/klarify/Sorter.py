from abc import ABC, abstractmethod
import re


class Sorter(ABC):
    @abstractmethod
    def __init__(self, config):
        """Initial setup for the sorter."""
        pass

    @abstractmethod
    def getPath(self, resource: str, kind: str) -> str:
        """Return calculated path."""
        pass


class StandardSorter(Sorter):
    def __init__(self, config):
        if not "structure" in config:
            raise ValueError('"structure" section required in config file.')
        self.structure = config['structure']
        if not "categories" in config:
            raise ValueError('"categories" section required in config file.')
        self.categories = config['categories']

    def getPath(self, resource: str, kind: str) -> str:
        """Return the calculated path."""
        # Set defaults for mismatches
        path = "generated"
        sub = "unknown"
        # print(f"Getting path for: {resource}")
        for destination in self.structure:
            # print(f"Checking {destination}")
            if self.matches(resource, self.structure[destination], False):
                path = destination
                break
        for category in self.categories:
            # print(f"Checking {category}")
            if self.matches(kind, self.categories[category], True):
                sub = category
                break
        return f"{path}/{sub}"

    def matches(self, resource: str, patterns: list, exact: bool) -> bool:
        for pattern in patterns:
            if exact:
                p = f"^{pattern}$"
            else:
                p = pattern
            if re.search(p, resource):
                return True
        return False
