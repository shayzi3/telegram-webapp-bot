import flet as ft

from src.widgets import ContainerError



class Error:
     def __init__(self, page: ft.Page) -> None:
          self.page = page
          self.page.clean()
          
          self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
          self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
          
          self.display()
          
          
     def display(self) -> None:
          self.page.add(ContainerError())