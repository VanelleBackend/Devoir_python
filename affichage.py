import tkinter as tk
from exportation import *

# Fichier de stockage des commandes
SERVICES = ["Conception de Logo", "Banderole", "Site Web"]

def construire_onglet_clients(parent):
    var_nom = tk.StringVar()
    var_tel = tk.StringVar()

    cadre_form = tk.LabelFrame(parent,
                    text=" Informations client ", padx=10, pady=10)
    cadre_form.pack(fill="x", padx=10, pady=8)

    tk.Label(
        cadre_form, 
        text="Nom complet :").grid(
        row=0, column=0, sticky="w", pady=4)
    tk.Entry(
        cadre_form, 
        textvariable=var_nom, width=30).grid(
        row=0, column=1, padx=8)

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

    tk.Button(
        cadre_btn, 
        text="Ajouter", 
        width=12, 
        bg="#3B82F6", 
        fg="white",
        command=lambda: ajouter_client(var_nom, var_tel, tree_clients)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Modifier", 
        width=12, 
        bg="#F59E0B", 
        fg="white",
        command=lambda: modifier_client(var_nom, var_tel, tree_clients)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Supprimer", 
        width=12, 
        bg="#EF4444", 
        fg="white",
        command=lambda: supprimer_client(tree_clients)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Réinitialiser", 
        width=12,
        command=lambda: [var_nom.set(""), var_tel.set("")]
    ).pack(side="left", padx=4)

    style = ttk.Style()

    # Modifier le header
    style.configure("Treeview.Heading",
                    background="#1E293B",   # couleur fond
                    foreground="white",     # couleur texte
                    font=("Verdana", 11, "bold"))
    # Désactiver les effets hover / clic
    style.map("Treeview.Heading",
            background=[("active", "#1E293B"), ("pressed", "#1E293B")],
            foreground=[("active", "white"), ("pressed", "white")])
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



def construire_onglet_commandes(parent):
    var_client_id = tk.StringVar()
    var_service   = tk.StringVar()
    var_prix      = tk.StringVar()
    var_statut      = tk.StringVar()

    cadre_form = tk.LabelFrame(parent,
                    text=" Nouvelle commande ", padx=10, pady=10)
    cadre_form.pack(fill="x", padx=10, pady=8)

    tk.Label(
        cadre_form, 
        text="ID client :").grid(
        row=0, column=0, sticky="w", pady=4)
    tk.Entry(
        cadre_form, 
        textvariable=var_client_id, width=15).grid(
        row=0, column=1, padx=8, sticky="w")

    tk.Label(
        cadre_form, 
        text="Service :").grid(
        row=1, column=0, sticky="w", pady=4)
    combo_service = ttk.Combobox(cadre_form, textvariable=var_service,
                        values=SERVICES, state="readonly", width=28)
    combo_service.grid(row=1, column=1, padx=8, sticky="w")
    combo_service.set(SERVICES[0])

    tk.Label(
        cadre_form, 
        text="Prix :").grid(
        row=2, column=0, sticky="w", pady=4)
    tk.Entry(
        cadre_form, 
        textvariable=var_prix, width=30).grid(
        row=2, column=1, padx=8, sticky="w")
    
    tk.Label(
        cadre_form, 
        text="Statut de la commande :").grid(
        row=3, column=0, sticky="w", pady=4)
    tk.Entry(
        cadre_form, 
        textvariable=var_statut, width=30).grid(
        row=3, column=1, padx=8, sticky="w")

    cadre_btn = tk.Frame(parent)
    cadre_btn.pack(fill="x", padx=10, pady=4)
    tk.Button(
        cadre_btn, 
        text="Ajouter", 
        width=12, 
        bg="#3B82F6", 
        fg="white",
        command=lambda: ajouter_commande(var_client_id, var_service,var_prix,var_statut, tree_cmd)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Modifier", 
        width=12, 
        bg="#F59E0B", 
        fg="white",
        command=lambda: modifier_commande(var_client_id, var_service, var_prix, var_statut, tree_cmd)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Supprimer", 
        width=12, 
        bg="#EF4444", 
        fg="white",
        command=lambda: supprimer_commande(tree_cmd)
    ).pack(side="left", padx=4)
    tk.Button(
        cadre_btn, 
        text="Réinitialiser", 
        width=12,
        command=lambda: [var_client_id.set(""), var_service.set(""), var_prix.set(""), var_statut.set("")]
    ).pack(side="left", padx=4)


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
