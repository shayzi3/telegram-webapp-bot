import flet as ft

from src.pages import Error, Explore

    
class Main:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        
        user = page.route.split("/")[-1].strip()
        if user.isdigit() is False:
            Error(self.page)
            return None
        
        self.page.__dict__["user_id"] = user
        self.page.title = "Bot'sShop"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.DARK
        
        Explore(self.page)
        
     
if __name__ == "__main__":
    ft.app(target=Main, view=ft.WEB_BROWSER, port=8082, host="0.0.0.0")