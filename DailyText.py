import requests
from bs4 import BeautifulSoup
import tkinter as tk
from datetime import datetime

def fetch_daily_text():
    today = datetime.now()
    url = f"https://wol.jw.org/en/wol/dt/r1/lp-e/{today.year}/{today.month}/{today.day}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    scripture_tag = soup.find('p', class_='themeScrp')
    scripture = scripture_tag.get_text(strip=True) if scripture_tag else "No scripture found 💔"

    comment_tag = soup.find('div', class_='bodyTxt')
    comment = comment_tag.get_text(strip=True) if comment_tag else "No comment found 💔"

    return f"{scripture}\n\n{comment}"

def create_widget():
    def refresh_text():
        text = fetch_daily_text()
        text_widget.config(state='normal')
        text_widget.delete('1.0', tk.END)
        text_widget.insert('1.0', text)
        text_widget.config(state='disabled')

    root = tk.Tk()
    root.title("Daily Text 💭")
    root.geometry("500x400")
    root.attributes('-topmost', True)  # Always on top

    text_widget = tk.Text(root, wrap='word', padx=10, pady=10, font=('Segoe UI', 10))
    text_widget.pack(expand=True, fill='both')

    refresh_button = tk.Button(root, text="🔁 Refresh", command=refresh_text)
    refresh_button.pack(pady=5)

    refresh_text()  # Load initially
    root.mainloop()

create_widget()
