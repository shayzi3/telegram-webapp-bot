import flet as ft

from typing import Any



class ContainerItems(ft.Container):
     def __init__(
          self,
          product: tuple[Any],
          page: ft.Page
     ) -> None:
          price, name, image = product
          
          
          super().__init__(
               content=ft.Column(
                    controls=[
                         ft.Image(src=image, width=150, height=150),
                         ft.Text(name, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
                         ft.Text(f"Цена: {price} руб.", color=ft.Colors.BLACK),
                         ft.FilledButton(
                              text="Buy",
                              icon=ft.Icons.SHOPPING_BAG,
                              data=f"buy:{name}",
                              on_click=self.buy_button,
                              icon_color=ft.Colors.WHITE,
                              color=ft.Colors.WHITE,
                              bgcolor=ft.Colors.BLUE_500,
                              width=160
                         )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
               ),
               bgcolor=ft.Colors.WHITE,
               padding=15,
               margin=12,
               border_radius=20,
               expand=True,
          )
          
          
     async def buy_button(self, event: ft.ControlEvent) -> None:
          mode = event.control.data.split(":")
          print(f"User {self.page.user_id} buy {mode[1]}")
          
          if mode[0] == "buy":
               event.control.text = "Remove"
               event.control.bgcolor = ft.Colors.RED_500
               event.control.data = f"remove:{mode[1]}"
               
          elif mode[0] == "remove":
               event.control.text = "Buy"
               event.control.bgcolor = ft.Colors.BLUE_500
               event.control.data = f"buy:{mode[1]}"
          await self.page.update_async()
          
          
          
          
class ContainerError(ft.Container):
     def __init__(self) -> None:
          super().__init__(
               content=ft.Row(
                    controls=[
                         ft.Image(src="/images/error.png", width=80, height=80),
                         ft.Text(
                              value="Запрос отправлен без пользовательского ID.",
                              size=20,
                              style=ft.TextThemeStyle.TITLE_MEDIUM,
                              color=ft.Colors.BROWN_50
                         )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
               ),
               border_radius=15,
               width=650,
               height=200,
               padding=10,
               bgcolor=ft.Colors.BLACK38
          )