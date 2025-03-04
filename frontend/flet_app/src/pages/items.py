import flet as ft 

from typing import Any
from src.widgets import ContainerItems, Navigation



class Items:
     def __init__(self, page: ft.Page):
          self.page = page
          self.page.clean()
          
          self.display()
          
          
     def display(self) -> None:
          products = self.sorted_items(self.api_products)
          
          product_list = ft.ListView(expand=1)
          for item in products:
               rows = ft.Row(spacing=5)
               for product in item:
                    rows.controls.append(ContainerItems(product=product, page=self.page))
               product_list.controls.append(rows)

          self.page.add(
               ft.AppBar(title=ft.Text("Tasty's Shop"), center_title=True),
               product_list,
               Navigation(self.page)
          )
          
          
     def sorted_items(self, data: list[tuple[Any]]) -> list[list[tuple[Any]]]:
          products: list[list[tuple[str]]] = []
          
          left, right = 0, 2
          for _ in range((len(data) // 2) + 1):
               products.append(data[left:right])
               left += 2
               right += 2
          return products
     
               
     @property
     def api_products(self) -> list[tuple[Any]]:
          products_from_api = [
               (20, "Burger", "https://avatars.mds.yandex.net/get-pdb/901820/85e3cf3f-f95d-4a4b-996b-60105b56e733/s1200?webp=false"),
               (15, "Ice Cream", "https://thumbs.dreamstime.com/b/ice-cream-pixel-art-bit-icecream-vector-illustration-ice-cream-pixel-art-bit-icecream-vector-illustration-118270563.jpg"),
               (40, "Taco", "https://assets.change.org/photos/8/vd/ce/YwVdCeLMiyOYuve-1600x900-noPad.jpg?1626450095"),
               (10, "Chips", "https://main-cdn.sbermegamarket.ru/big2/hlr-system/285/401/275/112/017/5/100029691236b0.jpg"),
               (1, "Free Potato", "https://main-cdn.sbermegamarket.ru/big2/hlr-system/-14/422/472/341/127/192/6/100045196938b0.jpg")
          ]
          return products_from_api