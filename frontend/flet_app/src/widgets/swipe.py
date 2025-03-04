import flet as ft



# 5 Макс
# Должен быть swipe выгодных предложений
# Предложение - это контейнер с чем-то




class Swipe(ft.Container):
     def __init__(self):
          self.data = [
               ("Burger", "40%", "https://avatars.mds.yandex.net/get-pdb/901820/85e3cf3f-f95d-4a4b-996b-60105b56e733/s1200?webp=false", "90", "150")
          ]
          
          self.control_row = []
          for item in self.data:
               name, benefit, image, new_price, old_price = item
               
               self.control_row.append(
                    ft.Row(
                         controls=[
                              ft.Column(
                                   controls=[
                                        ft.Text(value=f"{name}", size=15, color=ft.Colors.BLACK, text_align=ft.TextAlign.LEFT),
                                        ft.Image(src=image, width=150, height=150)
                                   ],
                              ),
                              ft.Column(
                                   controls=ft.Row(
                                        controls=[
                                             ft.Text(
                                                  value=old_price, 
                                                  color=ft.Colors.RED, 
                                                  style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)
                                             ),
                                             ft.Text(value=new_price, color=ft.Colors.RED)
                                        ],
                                   )
                              )
                         ]
                    )
               )
                    
          super().__init__(
               content=self.control_row[0],
               border_radius=15,
               padding=30,
               width=400,
               bgcolor=ft.Colors.PURPLE_50
          )
          
          
          
          