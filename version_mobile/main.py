# Importation. 
import tkinter as tk
from tkinter import ttk, messagebox
import datetime, os

# Constantes. 
FICHIER_CLIENTS = "clients.txt"
FICHIER_COMMANDES = "commandes.txt"
SERVICES = ["Conception de Logo", "Banderole", "Site Web"]


# Fonction onglet clients. 
def construire_onglet_clients(parent):
    var_nom = tk.StringVar()
    var_tel = tk.StringVar()

    cadre_form = tk.LabelFrame(
        parent,
        text=" Informations client ",
        padx=10,
        pady=10
    )
    cadre_form.pack(fill="x", padx=10, pady=8)

    tk.Label(cadre_form, text="Nom complet :").grid(
        row=0, column=0, sticky="w", pady=4
    )
    tk.Entry(cadre_form, textvariable=var_nom, width=30).grid(
        row=0, column=1, padx=8
    )

    tk.Label(cadre_form, text="Téléphone :").grid(
        row=1, column=0, sticky="w", pady=4
    )
    tk.Entry(cadre_form, textvariable=var_tel, width=30).grid(
        row=1, column=1, padx=8
    )

    cadre_btn = tk.Frame(parent)
    cadre_btn.pack(fill="x", padx=10, pady=4)

    colonnes = ("id", "nom", "telephone")

    tree_clients = ttk.Treeview(
        parent,
        columns=colonnes,
        show="headings",
        height=10
    )

    tk.Button(
        cadre_btn,
        text="Ajouter",
        width=12,
        bg="#185FA5",
        fg="white",
        command=lambda: ajouter_client(var_nom, var_tel, tree_clients)
    ).pack(side="left", padx=4)

    tk.Button(
        cadre_btn,
        text="Modifier",
        width=12,
        command=lambda: modifier_client(var_nom, var_tel, tree_clients)
    ).pack(side="left", padx=4)

    tk.Button(
        cadre_btn,
        text="Supprimer",
        width=12,
        bg="#A32D2D",
        fg="white",
        command=lambda: supprimer_client(tree_clients)
    ).pack(side="left", padx=4)

    tk.Button(
        cadre_btn,
        text="Réinitialiser",
        width=12,
        command=lambda: [var_nom.set(""), var_tel.set("")]
    ).pack(side="left", padx=4)

    tree_clients.heading("id", text="ID")
    tree_clients.heading("nom", text="Nom")
    tree_clients.heading("telephone", text="Téléphone")

    tree_clients.column("id", width=60)
    tree_clients.column("nom", width=250)
    tree_clients.column("telephone", width=150)

    tree_clients.pack(fill="both", expand=True, padx=10, pady=8)
    charger_clients(tree_clients)

    tree_clients.bind(
        "<<TreeviewSelect>>",
        lambda e: selectionner_client(tree_clients, var_nom, var_tel)
    )

# Function onglet commande. 
def construire_onglet_commandes(parent):
    var_client_id = tk.StringVar()
    var_service = tk.StringVar()

    cadre_form = tk.LabelFrame(
        parent,
        text=" Nouvelle commande ",
        padx=10,
        pady=10
    )
    cadre_form.pack(fill="x", padx=10, pady=8)

    tk.Label(cadre_form, text="ID client :").grid(
        row=0, column=0, sticky="w", pady=4
    )
    tk.Entry(cadre_form, textvariable=var_client_id, width=15).grid(
        row=0, column=1, padx=8, sticky="w"
    )

    tk.Label(cadre_form, text="Service :").grid(
        row=1, column=0, sticky="w", pady=4
    )

    combo_service = ttk.Combobox(
        cadre_form,
        textvariable=var_service,
        values=SERVICES,
        state="readonly",
        width=28
    )
    combo_service.grid(row=1, column=1, padx=8, sticky="w")
    combo_service.set(SERVICES[0])

    cadre_btn = tk.Frame(parent)
    cadre_btn.pack(fill="x", padx=10, pady=4)

    colonnes = ("id_cmd", "id_client", "service", "date")

    tree_cmd = ttk.Treeview(
        parent,
        columns=colonnes,
        show="headings",
        height=10
    )

    tk.Button(
        cadre_btn,
        text="Ajouter",
        width=12,
        bg="#185FA5",
        fg="white",
        command=lambda: ajouter_commande(var_client_id, var_service, tree_cmd)
    ).pack(side="left", padx=4)

    tk.Button(
        cadre_btn,
        text="Supprimer",
        width=12,
        bg="#A32D2D",
        fg="white",
        command=lambda: supprimer_commande(tree_cmd)
    ).pack(side="left", padx=4)

    tree_cmd.heading("id_cmd", text="N° Cmd")
    tree_cmd.heading("id_client", text="ID Client")
    tree_cmd.heading("service", text="Service")
    tree_cmd.heading("date", text="Date")

    tree_cmd.column("id_cmd", width=70)
    tree_cmd.column("id_client", width=80)
    tree_cmd.column("service", width=200)
    tree_cmd.column("date", width=120)

    tree_cmd.pack(fill="both", expand=True, padx=10, pady=8)
    charger_commandes(tree_cmd)

# Logique métier CRUD.

# Clients — Ajouter / Modifier / Supprimer / Sélectionner
def generer_id(fichier):
    lignes = lire_fichier(fichier)
    if not lignes:
        return 1

    ids = [int(l.split(";")[0]) for l in lignes if l.strip()]
    return max(ids) + 1


def ajouter_client(var_nom, var_tel, tree):
    nom = var_nom.get().strip()
    tel = var_tel.get().strip()

    if not nom or not tel:
        messagebox.showwarning("Champ vide", "Veuillez remplir tous les champs.")
        return

    cid = generer_id(FICHIER_CLIENTS)
    ecrire_ligne(FICHIER_CLIENTS, f"{cid};{nom};{tel}")

    tree.insert("", "end", values=(cid, nom, tel))

    var_nom.set("")
    var_tel.set("")

    messagebox.showinfo("Succès", f"Client #{cid} ajouté.")


def modifier_client(var_nom, var_tel, tree):
    sel = tree.selection()

    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un client à modifier.")
        return

    cid = tree.item(sel[0], "values")[0]
    nom = var_nom.get().strip()
    tel = var_tel.get().strip()

    if not nom or not tel:
        messagebox.showwarning(
            "Champ vide",
            "Remplissez les champs avant de modifier."
        )
        return

    modifier_ligne(FICHIER_CLIENTS, int(cid), nom, tel)

    tree.item(sel[0], values=(cid, nom, tel))

    messagebox.showinfo("Mis à jour", f"Client #{cid} modifié.")


def supprimer_client(tree):
    sel = tree.selection()

    if not sel:
        messagebox.showwarning("Sélection", "Sélectionnez un client à supprimer.")
        return

    cid = tree.item(sel[0], "values")[0]

    if messagebox.askyesno("Confirmer", f"Supprimer le client #{cid} ?"):
        supprimer_ligne(FICHIER_CLIENTS, int(cid))
        tree.delete(sel[0])


def selectionner_client(tree, var_nom, var_tel):
    sel = tree.selection()

    if sel:
        vals = tree.item(sel[0], "values")
        var_nom.set(vals[1])
        var_tel.set(vals[2])

# Commandes — Ajouter / Supprimer
def ajouter_commande(var_client_id, var_service, tree):
    cid = var_client_id.get().strip()
    service = var_service.get().strip()

    if not cid or not service:
        messagebox.showwarning(
            "Erreur",
            "ID client et service sont obligatoires."
        )
        return

    if not client_existe(int(cid)):
        messagebox.showerror(
            "Client introuvable",
            f"Aucun client avec l'ID {cid}."
        )
        return

    num = generer_id(FICHIER_COMMANDES)
    date = datetime.date.today().isoformat()

    ecrire_ligne(FICHIER_COMMANDES, f"{num};{cid};{service};{date}")

    tree.insert("", "end", values=(num, cid, service, date))

    messagebox.showinfo("Succès", f"Commande #{num} enregistrée.")


def supprimer_commande(tree):
    sel = tree.selection()

    if not sel:
        messagebox.showwarning(
            "Sélection",
            "Sélectionnez une commande à supprimer."
        )
        return

    num = tree.item(sel[0], "values")[0]

    if messagebox.askyesno("Confirmer", f"Supprimer la commande #{num} ?"):
        supprimer_ligne(FICHIER_COMMANDES, int(num))
        tree.delete(sel[0])
        
# Persistance — lecture et écriture dans les fichiers. 

# ─── FONCTIONS GÉNÉRIQUES DE FICHIER ─────────────────
def lire_fichier(chemin):
    """Retourne toutes les lignes non vides d'un fichier."""
    if not os.path.exists(chemin):
        return []

    with open(chemin, "r", encoding="utf-8") as f:
        return [l.strip() for l in f.readlines() if l.strip()]


def ecrire_ligne(chemin, ligne):
    """Ajoute une ligne à la fin du fichier (mode append)."""
    with open(chemin, "a", encoding="utf-8") as f:
        f.write(ligne + "\n")


def reecrire_fichier(chemin, lignes):
    """Réécrit l'intégralité du fichier (pour update/delete)."""
    with open(chemin, "w", encoding="utf-8") as f:
        f.writelines([l + "\n" for l in lignes])


def supprimer_ligne(chemin, identifiant):
    lignes = lire_fichier(chemin)
    nouvelles = [
        l for l in lignes
        if int(l.split(";")[0]) != identifiant
    ]
    reecrire_fichier(chemin, nouvelles)


def modifier_ligne(chemin, identifiant, *champs):
    lignes = lire_fichier(chemin)
    nouvelles = []

    for l in lignes:
        parties = l.split(";")

        if int(parties[0]) == identifiant:
            nouvelles.append(";".join([parties[0]] + list(champs)))
        else:
            nouvelles.append(l)

    reecrire_fichier(chemin, nouvelles)


# ─── CHARGEMENT INITIAL ────────────────────────────────
def charger_clients(tree):
    for ligne in lire_fichier(FICHIER_CLIENTS):
        p = ligne.split(";")

        if len(p) == 3:
            tree.insert("", "end", values=tuple(p))


def charger_commandes(tree):
    for ligne in lire_fichier(FICHIER_COMMANDES):
        p = ligne.split(";")

        if len(p) == 4:
            tree.insert("", "end", values=tuple(p))


def client_existe(cid):
    return any(
        int(l.split(";")[0]) == cid
        for l in lire_fichier(FICHIER_CLIENTS)
    )


# Fonction principale
def creer_fenetre():
    root = tk.Tk()
    root.title("GraphiStudio")
    root.geometry("400x300")

    header = tk.Frame(root, bg="#185FA5", height=80)
    header.pack(fill="x")

    tk.Label(
        header,
        text="GraphiStudio — Système de gestion",
        bg="#185FA5",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(side="left", pady=10)

    onglets = ttk.Notebook(root)
    onglets.pack(fill="both", expand=True, padx=10, pady=10)

    tab_clients = ttk.Frame(onglets)
    tab_cmdes = ttk.Frame(onglets)

    onglets.add(tab_clients, text="Clients")
    onglets.add(tab_cmdes, text="Commandes")

    # appel des fonctions onglets clients et commandes
    construire_onglet_clients(tab_clients)
    construire_onglet_commandes(tab_cmdes)

    root.mainloop()


if __name__ == "__main__":
    creer_fenetre()