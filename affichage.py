import tkinter as tk
from tkinter import ttk
from pathlib import Path
import sys

try:
    import customtkinter as ctk
except ModuleNotFoundError:
    project_root = Path(__file__).resolve().parent
    for candidate in project_root.glob("env/lib/python*/site-packages"):
        sys.path.insert(0, str(candidate))
        break
    import customtkinter as ctk

from exportation import (
    ajouter_client,
    ajouter_commande,
    charger_clients,
    charger_commandes,
    compter_clients,
    compter_commandes,
    lister_clients,
    lister_commandes,
    modifier_client,
    selectionner_client,
    supprimer_client,
    supprimer_commande,
)

SERVICES = ["Conception de Logo", "Banderole", "Site Web"]

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class GraphiStudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GraphiStudio - Systeme de gestion")
        self.geometry("1360x820")
        self.minsize(1180, 720)
        self.configure(fg_color="#EEF3FB")

        self.nav_buttons = {}
        self.pages = {}
        self.stat_cards = {}

        self._configure_grid()
        self._setup_treeview_style()
        self._build_sidebar()
        self._build_topbar()
        self._build_content()
        self.show_page("dashboard")
        self.refresh_dashboard()

    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

    def _setup_treeview_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "GraphiStudio.Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#24324B",
            rowheight=34,
            borderwidth=0,
            relief="flat",
            font=("Arial", 11),
        )
        style.configure(
            "GraphiStudio.Treeview.Heading",
            background="#F3F7FC",
            foreground="#61708C",
            relief="flat",
            borderwidth=0,
            font=("Arial", 11, "bold"),
        )
        style.map(
            "GraphiStudio.Treeview",
            background=[("selected", "#DCEAFE")],
            foreground=[("selected", "#1D4ED8")],
        )
        style.map(
            "GraphiStudio.Treeview.Heading",
            background=[("active", "#EAF1FB")],
        )

    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=250, fg_color="#FFFFFF", corner_radius=0)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        sidebar.grid_rowconfigure(7, weight=1)

        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.grid(row=0, column=0, sticky="ew", padx=24, pady=(24, 20))

        logo = ctk.CTkLabel(
            brand,
            text="G",
            width=34,
            height=34,
            fg_color="#2563EB",
            text_color="white",
            corner_radius=10,
            font=("Arial", 18, "bold"),
        )
        logo.grid(row=0, column=0, padx=(0, 12))

        title_wrap = ctk.CTkFrame(brand, fg_color="transparent")
        title_wrap.grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(
            title_wrap,
            text="GRAPHISTUDIO",
            font=("Arial", 20, "bold"),
            text_color="#15315B",
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_wrap,
            text="Management v1.0",
            font=("Arial", 11),
            text_color="#94A3B8",
        ).pack(anchor="w", pady=(2, 0))

        nav_items = [
            ("dashboard", "Dashboard", "[]"),
            ("clients", "Clients", "o-"),
            ("commandes", "Commandes", "><"),
            ("archives", "Archives", "::"),
        ]
        for index, (page_name, label, icon) in enumerate(nav_items, start=1):
            button = ctk.CTkButton(
                sidebar,
                text=f"{icon}  {label}",
                anchor="w",
                height=44,
                corner_radius=12,
                fg_color="transparent",
                hover_color="#E8F0FF",
                text_color="#5F6F89",
                font=("Arial", 14, "bold"),
                command=lambda name=page_name: self.show_page(name),
            )
            button.grid(row=index, column=0, sticky="ew", padx=18, pady=6)
            self.nav_buttons[page_name] = button

        helper = ctk.CTkFrame(sidebar, fg_color="transparent")
        helper.grid(row=8, column=0, sticky="ew", padx=24, pady=(12, 14))
        ctk.CTkLabel(
            helper,
            text="?  AIDE",
            font=("Arial", 13, "bold"),
            text_color="#94A3B8",
        ).pack(anchor="w", pady=(0, 18))

        logout_btn = ctk.CTkButton(
            helper,
            text="<  DECONNEXION",
            anchor="w",
            height=42,
            corner_radius=12,
            fg_color="#FFF1F2",
            hover_color="#FFE4E6",
            text_color="#DC2626",
            font=("Arial", 13, "bold"),
            command=self.destroy,
        )
        logout_btn.pack(fill="x")

    def _build_topbar(self):
        topbar = ctk.CTkFrame(self, height=74, fg_color="#26439C", corner_radius=0)
        topbar.grid(row=0, column=1, sticky="ew")
        topbar.grid_columnconfigure(0, weight=1)
        topbar.grid_columnconfigure(1, weight=0)

        left = ctk.CTkFrame(topbar, fg_color="transparent")
        left.grid(row=0, column=0, sticky="w", padx=26, pady=16)
        self.current_page_label = ctk.CTkLabel(
            left,
            text="Dashboard",
            font=("Arial", 14, "bold"),
            text_color="#DDE8FF",
        )
        self.current_page_label.pack(side="left", padx=(0, 20))

        nav_hint = ctk.CTkLabel(
            left,
            text="Clients",
            font=("Arial", 13),
            text_color="#C3D4FF",
        )
        nav_hint.pack(side="left", padx=(0, 16))

        nav_hint2 = ctk.CTkLabel(
            left,
            text="Commandes",
            font=("Arial", 13),
            text_color="#9CB2EA",
        )
        nav_hint2.pack(side="left")

        right = ctk.CTkFrame(topbar, fg_color="transparent")
        right.grid(row=0, column=1, sticky="e", padx=24, pady=14)

        search = ctk.CTkEntry(
            right,
            width=250,
            height=40,
            corner_radius=12,
            fg_color="#3551AB",
            border_width=0,
            text_color="#E8EFFF",
            placeholder_text="Recherche rapide...",
            placeholder_text_color="#AFC1F8",
        )
        search.pack(side="left", padx=(0, 14))

        for symbol in ["*", "o", "@"]:
            badge = ctk.CTkLabel(
                right,
                text=symbol,
                width=34,
                height=34,
                corner_radius=17,
                fg_color="#3551AB",
                text_color="#F8FAFF",
                font=("Arial", 13, "bold"),
            )
            badge.pack(side="left", padx=5)

    def _build_content(self):
        self.content = ctk.CTkFrame(self, fg_color="#EEF3FB", corner_radius=0)
        self.content.grid(row=1, column=1, sticky="nsew")
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.pages["dashboard"] = self._build_dashboard_page()
        self.pages["clients"] = self._build_clients_page()
        self.pages["commandes"] = self._build_commandes_page()
        self.pages["archives"] = self._build_archives_page()

        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew", padx=26, pady=24)

    def _make_page_shell(self, title, breadcrumb):
        page = ctk.CTkFrame(self.content, fg_color="transparent")
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(page, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        ctk.CTkLabel(
            header,
            text=title,
            font=("Arial", 34, "bold"),
            text_color="#14294B",
        ).pack(anchor="w")
        ctk.CTkLabel(
            header,
            text=breadcrumb,
            font=("Arial", 13),
            text_color="#7C8AA5",
        ).pack(anchor="w", pady=(4, 0))
        return page

    def _build_dashboard_page(self):
        page = self._make_page_shell("Vue d'ensemble", "Dashboard / Accueil")
        body = ctk.CTkFrame(page, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew")
        for column in range(3):
            body.grid_columnconfigure(column, weight=1)
        body.grid_rowconfigure(1, weight=1)

        stat_specs = [
            ("clients", "Clients actifs", "#2563EB"),
            ("commandes", "Commandes", "#F59E0B"),
            ("services", "Services suivis", "#10B981"),
        ]
        for col, (key, label, color) in enumerate(stat_specs):
            card = self._build_stat_card(body, label, color)
            card.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 8, 8 if col < 2 else 0), pady=(0, 18))
            self.stat_cards[key] = card

        panel = ctk.CTkFrame(body, fg_color="#FFFFFF", corner_radius=22)
        panel.grid(row=1, column=0, columnspan=3, sticky="nsew")
        panel.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            panel,
            text="Activite recente",
            font=("Arial", 20, "bold"),
            text_color="#1E335B",
        ).pack(anchor="w", padx=24, pady=(22, 8))

        self.dashboard_feed = ctk.CTkTextbox(
            panel,
            fg_color="#F8FBFF",
            corner_radius=16,
            border_width=0,
            text_color="#4C5A74",
            font=("Arial", 13),
            wrap="word",
        )
        self.dashboard_feed.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        self.dashboard_feed.configure(state="disabled")
        return page

    def _build_stat_card(self, parent, label, color):
        card = ctk.CTkFrame(parent, fg_color="#FFFFFF", corner_radius=22)
        accent = ctk.CTkLabel(
            card,
            text="",
            width=12,
            height=48,
            fg_color=color,
            corner_radius=8,
        )
        accent.pack(anchor="w", padx=20, pady=(20, 12))

        value = ctk.CTkLabel(
            card,
            text="0",
            font=("Arial", 30, "bold"),
            text_color="#163057",
        )
        value.pack(anchor="w", padx=20)

        text = ctk.CTkLabel(
            card,
            text=label,
            font=("Arial", 13),
            text_color="#8391A8",
        )
        text.pack(anchor="w", padx=20, pady=(2, 20))

        card.value_label = value
        return card

    def _build_clients_page(self):
        page = self._make_page_shell("Gestion des Clients", "Dashboard / Clients")
        body = ctk.CTkFrame(page, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        form_card = ctk.CTkFrame(body, fg_color="#FFFFFF", corner_radius=22)
        form_card.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        for column in range(2):
            form_card.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            form_card,
            text="Informations client",
            font=("Arial", 20, "bold"),
            text_color="#19335A",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(20, 18))

        self.var_nom = tk.StringVar()
        self.var_tel = tk.StringVar()

        self._build_entry_block(form_card, "NOM COMPLET", self.var_nom, "Ex: Jean Dupont", 1)
        self._build_entry_block(form_card, "TELEPHONE", self.var_tel, "+237 6 00 00 00 00", 3)

        button_row = ctk.CTkFrame(form_card, fg_color="transparent")
        button_row.grid(row=5, column=0, columnspan=2, sticky="ew", padx=24, pady=(10, 22))
        for column in range(4):
            button_row.grid_columnconfigure(column, weight=1)

        buttons = [
            ("+  Ajouter", "#2563EB", "#1D4ED8", lambda: ajouter_client(self.var_nom, self.var_tel, self.tree_clients, self.refresh_dashboard)),
            ("~  Modifier", "#F59E0B", "#D97706", lambda: modifier_client(self.var_nom, self.var_tel, self.tree_clients, self.refresh_dashboard)),
            ("x  Supprimer", "#DC2626", "#B91C1C", lambda: self._supprimer_client()),
            ("o  Reinitialiser", "#E2E8F0", "#CBD5E1", self._reset_client_form),
        ]

        for col, (label, color, hover, command) in enumerate(buttons):
            text_color = "#FFFFFF" if col < 3 else "#475569"
            ctk.CTkButton(
                button_row,
                text=label,
                height=44,
                corner_radius=12,
                fg_color=color,
                hover_color=hover,
                text_color=text_color,
                font=("Arial", 13, "bold"),
                command=command,
            ).grid(row=0, column=col, sticky="ew", padx=6)

        table_card = ctk.CTkFrame(body, fg_color="#FFFFFF", corner_radius=22)
        table_card.grid(row=1, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(table_card, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text="Liste des contacts",
            font=("Arial", 19, "bold"),
            text_color="#19335A",
        ).grid(row=0, column=0, sticky="w")
        self.clients_count_label = ctk.CTkLabel(
            header,
            text="0 clients",
            font=("Arial", 12, "bold"),
            text_color="#7C8AA5",
        )
        self.clients_count_label.grid(row=0, column=1, sticky="e")

        table_wrap = ctk.CTkFrame(table_card, fg_color="#F8FBFF", corner_radius=18)
        table_wrap.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        table_wrap.grid_columnconfigure(0, weight=1)
        table_wrap.grid_rowconfigure(0, weight=1)

        columns = ("id", "nom", "telephone")
        self.tree_clients = ttk.Treeview(
            table_wrap,
            columns=columns,
            show="headings",
            style="GraphiStudio.Treeview",
        )
        self.tree_clients.heading("id", text="ID")
        self.tree_clients.heading("nom", text="NOM COMPLET")
        self.tree_clients.heading("telephone", text="TELEPHONE")
        self.tree_clients.column("id", width=90, anchor="center")
        self.tree_clients.column("nom", width=420, anchor="w")
        self.tree_clients.column("telephone", width=220, anchor="w")
        self.tree_clients.grid(row=0, column=0, sticky="nsew")

        client_scroll = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree_clients.yview)
        client_scroll.grid(row=0, column=1, sticky="ns")
        self.tree_clients.configure(yscrollcommand=client_scroll.set)
        self.tree_clients.bind(
            "<<TreeviewSelect>>",
            lambda _event: selectionner_client(self.tree_clients, self.var_nom, self.var_tel),
        )

        charger_clients(self.tree_clients)
        self._update_client_counter()
        return page

    def _build_entry_block(self, parent, label, variable, placeholder, row):
        ctk.CTkLabel(
            parent,
            text=label,
            font=("Arial", 12, "bold"),
            text_color="#66768F",
        ).grid(row=row, column=0, sticky="w", padx=24, pady=(0, 6))

        entry = ctk.CTkEntry(
            parent,
            textvariable=variable,
            height=44,
            corner_radius=12,
            border_width=0,
            fg_color="#F1F5F9",
            text_color="#1F2F46",
            placeholder_text=placeholder,
            placeholder_text_color="#A3B0C2",
        )
        entry.grid(row=row + 1, column=0, columnspan=2, sticky="ew", padx=24, pady=(0, 8))

    def _build_commandes_page(self):
        page = self._make_page_shell("Gestion des Commandes", "Dashboard / Commandes")
        body = ctk.CTkFrame(page, fg_color="transparent")
        body.grid(row=1, column=0, sticky="nsew")
        body.grid_columnconfigure(0, weight=1)
        body.grid_rowconfigure(1, weight=1)

        form_card = ctk.CTkFrame(body, fg_color="#FFFFFF", corner_radius=22)
        form_card.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        for column in range(2):
            form_card.grid_columnconfigure(column, weight=1)

        ctk.CTkLabel(
            form_card,
            text="Nouvelle commande",
            font=("Arial", 20, "bold"),
            text_color="#19335A",
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=24, pady=(20, 18))

        self.var_client_id = tk.StringVar()
        self.var_service = tk.StringVar(value=SERVICES[0])

        self._build_entry_block(form_card, "ID CLIENT", self.var_client_id, "Ex: 3", 1)

        ctk.CTkLabel(
            form_card,
            text="SERVICE",
            font=("Arial", 12, "bold"),
            text_color="#66768F",
        ).grid(row=3, column=0, sticky="w", padx=24, pady=(12, 6))
        service_menu = ctk.CTkOptionMenu(
            form_card,
            variable=self.var_service,
            values=SERVICES,
            height=44,
            corner_radius=12,
            fg_color="#2563EB",
            button_color="#1D4ED8",
            button_hover_color="#1E40AF",
            dropdown_fg_color="#FFFFFF",
            dropdown_hover_color="#E8F0FF",
            text_color="#FFFFFF",
            font=("Arial", 13, "bold"),
        )
        service_menu.grid(row=4, column=0, columnspan=2, sticky="ew", padx=24, pady=(0, 14))

        button_row = ctk.CTkFrame(form_card, fg_color="transparent")
        button_row.grid(row=5, column=0, columnspan=2, sticky="ew", padx=24, pady=(8, 22))
        for column in range(3):
            button_row.grid_columnconfigure(column, weight=1)

        ctk.CTkButton(
            button_row,
            text="+  Ajouter",
            height=44,
            corner_radius=12,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            text_color="#FFFFFF",
            font=("Arial", 13, "bold"),
            command=lambda: ajouter_commande(
                self.var_client_id,
                self.var_service,
                self.tree_commandes,
                self.refresh_dashboard,
            ),
        ).grid(row=0, column=0, sticky="ew", padx=6)

        ctk.CTkButton(
            button_row,
            text="x  Supprimer",
            height=44,
            corner_radius=12,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            text_color="#FFFFFF",
            font=("Arial", 13, "bold"),
            command=self._supprimer_commande,
        ).grid(row=0, column=1, sticky="ew", padx=6)

        ctk.CTkButton(
            button_row,
            text="o  Reinitialiser",
            height=44,
            corner_radius=12,
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color="#475569",
            font=("Arial", 13, "bold"),
            command=self._reset_commande_form,
        ).grid(row=0, column=2, sticky="ew", padx=6)

        table_card = ctk.CTkFrame(body, fg_color="#FFFFFF", corner_radius=22)
        table_card.grid(row=1, column=0, sticky="nsew")
        table_card.grid_columnconfigure(0, weight=1)
        table_card.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(table_card, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=24, pady=(20, 10))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header,
            text="Liste des commandes",
            font=("Arial", 19, "bold"),
            text_color="#19335A",
        ).grid(row=0, column=0, sticky="w")
        self.commandes_count_label = ctk.CTkLabel(
            header,
            text="0 commandes",
            font=("Arial", 12, "bold"),
            text_color="#7C8AA5",
        )
        self.commandes_count_label.grid(row=0, column=1, sticky="e")

        table_wrap = ctk.CTkFrame(table_card, fg_color="#F8FBFF", corner_radius=18)
        table_wrap.grid(row=1, column=0, sticky="nsew", padx=24, pady=(0, 24))
        table_wrap.grid_columnconfigure(0, weight=1)
        table_wrap.grid_rowconfigure(0, weight=1)

        columns = ("id_cmd", "id_client", "service", "date")
        self.tree_commandes = ttk.Treeview(
            table_wrap,
            columns=columns,
            show="headings",
            style="GraphiStudio.Treeview",
        )
        self.tree_commandes.heading("id_cmd", text="N CMD")
        self.tree_commandes.heading("id_client", text="ID CLIENT")
        self.tree_commandes.heading("service", text="SERVICE")
        self.tree_commandes.heading("date", text="DATE")
        self.tree_commandes.column("id_cmd", width=90, anchor="center")
        self.tree_commandes.column("id_client", width=100, anchor="center")
        self.tree_commandes.column("service", width=320, anchor="w")
        self.tree_commandes.column("date", width=170, anchor="center")
        self.tree_commandes.grid(row=0, column=0, sticky="nsew")

        commandes_scroll = ttk.Scrollbar(table_wrap, orient="vertical", command=self.tree_commandes.yview)
        commandes_scroll.grid(row=0, column=1, sticky="ns")
        self.tree_commandes.configure(yscrollcommand=commandes_scroll.set)

        charger_commandes(self.tree_commandes)
        self._update_commande_counter()
        return page

    def _build_archives_page(self):
        page = self._make_page_shell("Archives", "Dashboard / Archives")
        card = ctk.CTkFrame(page, fg_color="#FFFFFF", corner_radius=22)
        card.grid(row=1, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            card,
            text="Section reservee",
            font=("Arial", 24, "bold"),
            text_color="#19335A",
        ).pack(anchor="center", pady=(120, 12))
        ctk.CTkLabel(
            card,
            text="Cette zone est prete pour une future gestion des archives\nou des exports avances.",
            font=("Arial", 15),
            text_color="#7C8AA5",
            justify="center",
        ).pack(anchor="center")
        return page

    def show_page(self, name):
        titles = {
            "dashboard": "Dashboard",
            "clients": "Clients",
            "commandes": "Commandes",
            "archives": "Archives",
        }
        self.current_page_label.configure(text=titles.get(name, "Dashboard"))
        for page_name, page in self.pages.items():
            if page_name == name:
                page.tkraise()

        for page_name, button in self.nav_buttons.items():
            if page_name == name:
                button.configure(fg_color="#E8F0FF", text_color="#2563EB")
            else:
                button.configure(fg_color="transparent", text_color="#5F6F89")

        if name == "clients":
            charger_clients(self.tree_clients)
            self._update_client_counter()
        elif name == "commandes":
            charger_commandes(self.tree_commandes)
            self._update_commande_counter()
        self.refresh_dashboard()

    def _reset_client_form(self):
        self.var_nom.set("")
        self.var_tel.set("")
        self.tree_clients.selection_remove(self.tree_clients.selection())

    def _reset_commande_form(self):
        self.var_client_id.set("")
        self.var_service.set(SERVICES[0])
        self.tree_commandes.selection_remove(self.tree_commandes.selection())

    def _supprimer_client(self):
        if supprimer_client(self.tree_clients, self.refresh_dashboard):
            self._reset_client_form()

    def _supprimer_commande(self):
        if supprimer_commande(self.tree_commandes, self.refresh_dashboard):
            self._reset_commande_form()

    def _update_client_counter(self):
        total = compter_clients()
        self.clients_count_label.configure(text=f"{total} client{'s' if total > 1 else ''}")

    def _update_commande_counter(self):
        total = compter_commandes()
        self.commandes_count_label.configure(text=f"{total} commande{'s' if total > 1 else ''}")

    def refresh_dashboard(self):
        if "clients" in self.stat_cards:
            self.stat_cards["clients"].value_label.configure(text=str(compter_clients()))
        if "commandes" in self.stat_cards:
            self.stat_cards["commandes"].value_label.configure(text=str(compter_commandes()))
        if "services" in self.stat_cards:
            self.stat_cards["services"].value_label.configure(text=str(len(SERVICES)))
        if hasattr(self, "tree_clients"):
            self._update_client_counter()
        if hasattr(self, "tree_commandes"):
            self._update_commande_counter()
        self._refresh_dashboard_feed()

    def _refresh_dashboard_feed(self):
        lignes = []
        for client_id, nom, telephone in lister_clients()[-3:]:
            lignes.append(f"Client #{client_id}  |  {nom}  |  {telephone}")
        for commande_id, client_id, service, date in lister_commandes()[-3:]:
            lignes.append(f"Commande #{commande_id}  |  Client {client_id}  |  {service}  |  {date}")

        if not lignes:
            lignes = ["Aucune activite enregistree pour le moment."]

        self.dashboard_feed.configure(state="normal")
        self.dashboard_feed.delete("1.0", "end")
        self.dashboard_feed.insert("1.0", "\n\n".join(lignes[::-1]))
        self.dashboard_feed.configure(state="disabled")
