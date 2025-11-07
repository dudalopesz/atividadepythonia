"""Aplicação Tkinter: Chatbot desktop com login, tema escuro/claro, e avatares.

Como usar:
 - Execute `python app.py`.
 - Login com credenciais definidas em VALID_USERS.
"""
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
import time
from chatbot import get_response

VALID_USERS = {
    "Maria": "1234",
    "João": "1234",
    "luis": "1234",
    "Ana": "1234",
    "Mariana": "1234",
}


class ChatBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatTI — Simulador de Chatbot")
        self.root.geometry("800x600")
        self.user_name = None

        self.themes = {
            "light": {
                "bg": "#FFF0F5", 
                "fg": "#2F4F4F",  
                "user_bg": "#FFB6C1",  
                "bot_bg": "#FFC0CB",  
                "input_bg": "#ffffff",
            },
            "dark": {
                "bg": "#4A4454",  
                "fg": "#FFE4E1",  
                "user_bg": "#DB7093",  
                "bot_bg": "#C71585", 
                "input_bg": "#483D8B",  
            },
        }
        self.current_theme = "light"

        default_font = (None, 10)
        self.fonts = {
            "title": (None, 12, "bold"),
            "name": (None, 9, "bold"),
            "msg": (None, 10),
            "time": (None, 8),
        }

        self._build_login()

    def _build_login(self):
        self.root.configure(bg="#FFF0F5")  
        
        
        self.login_frame = tk.Frame(self.root, bg="#FFF0F5", padx=40, pady=30)
        self.login_frame.pack(expand=True)

        
        title_frame = tk.Frame(self.login_frame, bg="#FFF0F5")
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        lbl = tk.Label(title_frame, 
                      text="Bem-vindo ao ChatTI",
                      font=("Helvetica", 24, "bold"),
                      bg="#FFF0F5",
                      fg="#DB7093")  
        lbl.pack()

    
        subtitle = tk.Label(title_frame,
                          text="Seu assistente de TI",
                          font=("Helvetica", 12),
                          bg="#FFF0F5",
                          fg="#C71585")
        subtitle.pack(pady=(5,0))

        
        tk.Label(self.login_frame, 
                text="Usuário:",
                font=("Helvetica", 12),
                bg="#FFF0F5",
                fg="#2F4F4F").grid(row=1, column=0, sticky="e", padx=5)
        
        self.user_entry = tk.Entry(self.login_frame,
                                 font=("Helvetica", 12),
                                 bg="white",
                                 fg="#2F4F4F",
                                 insertbackground="#DB7093",  
                                 relief="solid",
                                 borderwidth=1)
        self.user_entry.grid(row=1, column=1, pady=5, padx=5, ipady=5)

        tk.Label(self.login_frame,
                text="Senha:",
                font=("Helvetica", 12),
                bg="#FFF0F5",
                fg="#2F4F4F").grid(row=2, column=0, sticky="e", padx=5)
        
        self.pass_entry = tk.Entry(self.login_frame,
                                 font=("Helvetica", 12),
                                 show="●",  
                                 bg="white",
                                 fg="#2F4F4F",
                                 insertbackground="#DB7093",
                                 relief="solid",
                                 borderwidth=1)
        self.pass_entry.grid(row=2, column=1, pady=5, padx=5, ipady=5)

    
        login_btn = tk.Button(self.login_frame,
                            text="Entrar",
                            command=self._attempt_login,
                            font=("Helvetica", 12, "bold"),
                            bg="#DB7093",
                            fg="white",
                            activebackground="#C71585",
                            activeforeground="white",
                            relief="solid",
                            borderwidth=1,
                            padx=30,
                            pady=8,
                            cursor="hand2")  
        login_btn.grid(row=3, column=0, columnspan=2, pady=20)

        self.user_entry.focus_set()

    def _attempt_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        if username in VALID_USERS and VALID_USERS[username] == password:
            self.user_name = username
            self.login_frame.destroy()
            self._build_chat_window()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def _build_chat_window(self):
        self.root.configure(bg=self.themes[self.current_theme]["bg"]) 

        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill="x", padx=8, pady=8)

        title = ttk.Label(top_frame, text=f"ChatTI — Usuário: {self.user_name}", font=(None, 12, "bold"))
        title.pack(side="left")

        ttk.Separator(self.root, orient="horizontal").pack(fill="x")

        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side="right")

        self.theme_btn = ttk.Button(btn_frame, text="Alternar Tema", command=self._toggle_theme)
        self.theme_btn.pack(side="left", padx=4)

        clear_btn = ttk.Button(btn_frame, text="Limpar", command=self._clear_messages)
        clear_btn.pack(side="left", padx=4)

        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True, padx=8, pady=(0,8))

        self.canvas = tk.Canvas(container, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        input_frame = ttk.Frame(self.root, padding=8)
        input_frame.pack(fill="x")

        self.msg_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.msg_var)
        self.input_entry.pack(side="left", fill="x", expand=True, padx=(0,8))
        self.input_entry.bind("<Return>", lambda e: self._on_send())

        send_btn = ttk.Button(input_frame, text="Enviar", command=self._on_send)
        send_btn.pack(side="left")

        self._apply_theme_to_widgets()

        self._add_bot_message("Olá! Sou o ChatTI. Pergunte algo sobre Tecnologia da Informação (TI).")

    def _add_message_widget(self, name, text, is_user=False):
        
        frame = tk.Frame(self.scrollable_frame, bg=self.themes[self.current_theme]["bg"])
        frame.pack(fill="x", pady=6, padx=6)

        avatar = tk.Canvas(frame, width=40, height=40, highlightthickness=0, bg=self.themes[self.current_theme]["bg"])
        avatar_side = "right" if is_user else "left"
        avatar.pack(side=avatar_side, padx=6)
        avatar_color = self.themes[self.current_theme]["user_bg"] if is_user else self.themes[self.current_theme]["bot_bg"]
        text_color = self.themes[self.current_theme]["fg"]
        avatar.create_oval(4, 4, 36, 36, fill=avatar_color, outline=avatar_color)
        initial = (name[0] if name else "?").upper()
        avatar.create_text(20, 20, text=initial, fill=text_color, font=self.fonts["name"])

        bubble_bg = avatar_color
        bubble_frame = tk.Frame(frame, bg=bubble_bg, bd=0)

        ts = time.strftime("%H:%M")
        name_lbl = tk.Label(bubble_frame, text=name, bg=bubble_bg, fg=text_color, font=self.fonts["name"])
        name_lbl.pack(anchor="w", padx=6, pady=(6,0))
        text_lbl = tk.Label(bubble_frame, text=text, wraplength=520, justify="left", bg=bubble_bg, fg=text_color, font=self.fonts["msg"], padx=6, pady=4)
        text_lbl.pack(anchor="w", padx=6)
        time_lbl = tk.Label(bubble_frame, text=ts, bg=bubble_bg, fg=text_color, font=self.fonts["time"])
        time_lbl.pack(anchor="e", padx=6, pady=(0,6))

        if is_user:
            bubble_frame.pack(side="right", padx=(0,10))
        else:
            bubble_frame.pack(side="left", padx=(10,0))

        self.root.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def _add_user_message(self, text):
        self._add_message_widget(self.user_name, text, is_user=True)

    def _add_bot_message(self, text):
        self._add_message_widget("ChatTI", text, is_user=False)

    def _on_send(self):
        text = self.msg_var.get().strip()
        if not text:
            return
        self.msg_var.set("")
        self._add_user_message(text)

        typing_label = ttk.Label(self.scrollable_frame, text="ChatTI está digitando...", padding=6)
        typing_label.pack(anchor="w", padx=10, pady=2)
        self.canvas.yview_moveto(1.0)

        def worker():
            delay = 0.8 + (0.8 * (0.5))
            time.sleep(delay)
            resp = get_response(text)

            def show_response():
                typing_label.destroy()
                self._add_bot_message(resp)

            self.root.after(0, show_response)

        threading.Thread(target=worker, daemon=True).start()

    def _clear_messages(self):
        for child in list(self.scrollable_frame.winfo_children()):
            child.destroy()
        
        self._add_bot_message("Conversa limpa. Em que posso ajudar sobre TI?")

   
    def _toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self._apply_theme_to_widgets()

    def _apply_theme_to_widgets(self):
        colors = self.themes[self.current_theme]
        self.root.configure(bg=colors["bg"]) 
        
        try:
            self.canvas.configure(bg=colors["bg"]) 
            self.scrollable_frame.configure(bg=colors["bg"]) 
            for msg_frame in self.scrollable_frame.winfo_children():
                try:
                    msg_frame.configure(bg=colors["bg"]) 
                except Exception:
                    pass
                
                bubble = None
                avatar = None
                for w in msg_frame.winfo_children():
                    if isinstance(w, tk.Frame):
                        bubble = w
                    elif isinstance(w, tk.Canvas):
                        avatar = w

                name = None
                if bubble:
                    
                    for sub in bubble.winfo_children():
                        if isinstance(sub, tk.Label):
                            name = sub.cget("text")
                            break
                    bubble_bg = colors["user_bg"] if name == self.user_name else colors["bot_bg"]
                   
                    for sub in bubble.winfo_children():
                        if isinstance(sub, tk.Label):
                            sub.configure(bg=bubble_bg, fg=colors["fg"]) 

                if avatar:
                    avatar.configure(bg=colors["bg"])
                    avatar.delete("all")
                  
                    avatar_color = colors["user_bg"] if name == self.user_name else colors["bot_bg"]
                    avatar.create_oval(4, 4, 36, 36, fill=avatar_color, outline=avatar_color)
                    initial = (name[0] if name else "?").upper()
                    avatar.create_text(20, 20, text=initial, fill=colors["fg"], font=self.fonts["name"])
        except Exception:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotApp(root)
    root.mainloop()
