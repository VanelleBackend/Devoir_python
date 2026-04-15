import tkinter as tk
from exportation import *


# liste des services proposés par GraphiStudio
SERVICES = ["Conception de Logo", "Banderole", "Site Web",]

# Placeholder pour le champs de recherche
def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg="grey")

    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# function pour construire l'interface de l'onglet Clients
def construire_onglet_clients(parent):

    var_nom = tk.StringVar()
    var_tel = tk.StringVar()


    cadre_search = tk.Frame(parent)
    cadre_search.pack(fill="x", padx=10, pady=5)

    var_search = tk.StringVar()

    # `Rechercher` et `Réinitialiser` pour la recherche de clients
    tk.Button(
    cadre_search,
    text="Reinitialiser",
    font=("Arial", 10, "bold"),
    command=lambda: [
        var_search.set(""),
        charger_clients(tree_clients),
        entry_search.delete(0, tk.END),
        entry_search.insert(0, "Rechercher un client..."),
        entry_search.config(fg="grey"),
        entry_search.master.focus()
    ]
    ).pack(side="right", padx=5)
    tk.Button(
        cadre_search,
        text="Rechercher",
        bg="#3B82F6",
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: rechercher_clients(var_search.get(), tree_clients)
    ).pack(side="right")

    # Champs de recherche avec placeholder
    entry_search = tk.Entry(cadre_search, textvariable=var_search, width=30)
    entry_search.pack(side="right", padx=5)
    add_placeholder(entry_search, "Rechercher un client...")

    cadre_form = tk.LabelFrame(parent,
                    text=" Informations client ", padx=10, pady=10)
    cadre_form.pack(fill="x", padx=10, pady=8)

    # Champs pour le nom du client
    tk.Label(
        cadre_form, 
        text="Nom complet :").grid(
        row=0, column=0, sticky="w", pady=4)
    tk.Entry(
        cadre_form, 
        textvariable=var_nom, width=30).grid(
        row=0, column=1, padx=8)

    # Champs pour le téléphone du client
    tk.Label(
        cadre_form, 
        text="Téléphone :").grid(
        row=1, column=0, sticky="w", pady=4)
    tk.Entry(
        cadre_form, 
        textvariable=var_tel, width=30).grid(
        row=1, column=1, padx=8)

    cadre_btn = tk.Frame(parent)
    cadre_btn.pack(fill="x", padx=10, pady=4)

    # Boutons pour ajouter, modifier, supprimer et réinitialiser les clients
    tk.Button(
        cadre_btn, 
        text="Ajouter", 
        width=12, 
        bg="#3B82F6", 
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: ajouter_client(var_nom, var_tel, tree_clients)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Modifier", 
        width=12, 
        bg="#F59E0B", 
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: modifier_client(var_nom, var_tel, tree_clients)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Supprimer", 
        width=12, 
        bg="#EF4444", 
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: supprimer_client(tree_clients)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Réinitialiser", 
        width=12,
        font=("Arial", 10, "bold"),
        command=lambda: [var_nom.set(""), var_tel.set("")]
    ).pack(side="left", padx=4)

    style = ttk.Style()

    # Modifier le header du tableau pour les clients
    style.configure("Treeview.Heading",
                    background="#1E293B",   # couleur fond
                    foreground="white",     # couleur texte
                    font=("Verdana", 11, "bold"))
    # Désactiver les effets hover / clic
    style.map("Treeview.Heading",
            background=[("active", "#1E293B"), ("pressed", "#1E293B")],
            foreground=[("active", "white"), ("pressed", "white")])
    
    # Créer le tableau pour afficher les clients
    colonnes = ("id", "nom", "telephone")
    tree_clients = ttk.Treeview(parent, columns=colonnes, show="headings", height=10)
    tree_clients.heading("id",        text="ID")
    tree_clients.heading("nom",       text="Nom")
    tree_clients.heading("telephone", text="Téléphone")
    tree_clients.column("id",        width=20, anchor="center")
    tree_clients.column("nom",       width=10, anchor="center")
    tree_clients.column("telephone", width=10, anchor="center")
    tree_clients.pack(fill="both", expand=True, padx=10, pady=8)
    charger_clients(tree_clients)
    tree_clients.bind("<<TreeviewSelect>>",
        lambda e: selectionner_client(tree_clients, var_nom, var_tel))


# function pour construire l'interface de l'onglet Commandes
def construire_onglet_commandes(parent):

    var_client_id = tk.StringVar()
    var_service   = tk.StringVar()
    var_prix      = tk.StringVar()
    var_statut      = tk.StringVar()

    cadre_form = tk.LabelFrame(parent,
                    text=" Nouvelle commande ", padx=10, pady=10)
    cadre_form.pack(fill="x", padx=10, pady=8)

    # Champs pour l'ID du client
    tk.Label(
        cadre_form, 
        text="ID client :").grid(
        row=0, column=0, sticky="w", pady=4)
    tk.Entry(
        cadre_form, 
        textvariable=var_client_id, width=15).grid(
        row=0, column=1, padx=8, sticky="w")

    # Champs pour le service demandé
    tk.Label(
        cadre_form, 
        text="Service :").grid(
        row=1, column=0, sticky="w", pady=4)
    combo_service = ttk.Combobox(cadre_form, textvariable=var_service,
                        values=SERVICES, state="readonly", width=28)
    combo_service.grid(row=1, column=1, padx=8, sticky="w")
    combo_service.set(SERVICES[0])

    # Champs pour le prix du service
    tk.Label(
        cadre_form, 
        text="Prix :").grid(
        row=2, column=0, sticky="w", pady=4)
    tk.Entry(
        cadre_form, 
        textvariable=var_prix, width=30).grid(
        row=2, column=1, padx=8, sticky="w")
    
    # Champs pour le statut de la commande
    tk.Label(
        cadre_form, 
        text="Statut de la commande :").grid(
        row=3, column=0, sticky="w", pady=4)
    tk.Entry(
        cadre_form, 
        textvariable=var_statut, width=30).grid(
        row=3, column=1, padx=8, sticky="w")

    # Boutons pour ajouter, modifier, supprimer et réinitialiser les commandes
    cadre_btn = tk.Frame(parent)
    cadre_btn.pack(fill="x", padx=10, pady=4)
    tk.Button(
        cadre_btn, 
        text="Ajouter", 
        width=12, 
        bg="#3B82F6", 
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: ajouter_commande(var_client_id, var_service,var_prix,var_statut, tree_cmd)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Modifier", 
        width=12, 
        bg="#F59E0B", 
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: modifier_commande(var_client_id, var_service, var_prix, var_statut, tree_cmd)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Supprimer", 
        width=12, 
        bg="#EF4444", 
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: supprimer_commande(tree_cmd)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Réinitialiser", 
        width=12,
        font=("Arial", 10, "bold"),
        command=lambda: [var_client_id.set(""), var_service.set(""), var_prix.set(""), var_statut.set("")]
    ).pack(side="left", padx=4)

    # tableau pour afficher les commandes
    colonnes = ("id_cmd", "id_client", "service", "prix","statut", "date")
    tree_cmd = ttk.Treeview(parent, columns=colonnes, show="headings", height=10)
    tree_cmd.heading("id_cmd",    text="N° Cmd")
    tree_cmd.heading("id_client", text="ID Client")
    tree_cmd.heading("service",   text="Service")
    tree_cmd.heading("prix",   text="Prix")
    tree_cmd.heading("statut",   text="Statut")
    tree_cmd.heading("date",      text="Date")
    tree_cmd.column("id_cmd",    width=70, anchor="center")
    tree_cmd.column("id_client", width=80, anchor="center")
    tree_cmd.column("service",   width=200, anchor="center")
    tree_cmd.column("prix",   width=90, anchor="center")
    tree_cmd.column("statut",   width=70, anchor="center")
    tree_cmd.column("date",      width=100, anchor="center")
    tree_cmd.pack(fill="both", expand=True, padx=10, pady=8)
    charger_commandes(tree_cmd)
    tree_cmd.bind("<<TreeviewSelect>>",
        lambda e: selectionner_commande(tree_cmd, var_client_id, var_service, var_prix, var_statut))


