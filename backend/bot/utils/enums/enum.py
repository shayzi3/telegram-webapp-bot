from enum import Enum


class PageMode(Enum):
     ONE = "one"
     ALL = "all"
     
     def __str__(self):
          return self.value