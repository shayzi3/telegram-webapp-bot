import flet as ft


class Navigation(ft.NavigationBar):
     def __init__(self, main_page: ft.Page) -> None:
          self.main_page = main_page
          
          super().__init__(
               destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Главная"),
                    ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_BAG, label="Товары"),
                    ft.NavigationBarDestination(icon=ft.Icons.SHOPPING_BASKET, label="Корзина"),
               ],
               on_change=self.change
          )
          
          
     async def change(self, event: ft.ControlEvent) -> type:
          from src.pages import Explore, Items, Basket
          
          events = [Explore, Items, Basket]
          return events[event.control.selected_index](self.main_page)