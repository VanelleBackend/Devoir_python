import datetime
import os
from tkinter import messagebox

FICHIER_CLIENTS = "clients.txt"
FICHIER_COMMANDES = "commandes.txt"


def lire_fichier(chemin):
    if not os.path.exists(chemin):
        return []
    with open(chemin, "r", encoding="utf-8") as fichier:
        return [ligne.strip() for ligne in fichier.readlines() if ligne.strip()]


def ecrire_ligne(chemin, ligne):
    with open(chemin, "a", encoding="utf-8") as fichier:
        fichier.write(ligne + "\n")


def reecrire_fichier(chemin, lignes):
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.writelines([ligne + "\n" for ligne in lignes])


def supprimer_ligne(chemin, identifiant):
    lignes = lire_fichier(chemin)
    nouvelles_lignes = [ligne for ligne in lignes if int(ligne.split(";")[0]) != identifiant]
    reecrire_fichier(chemin, nouvelles_lignes)


def modifier_ligne(chemin, identifiant, *champs):
    lignes = lire_fichier(chemin)
    nouvelles_lignes = []
    for ligne in lignes:
        parties = ligne.split(";")
        if int(parties[0]) == identifiant:
            nouvelles_lignes.append(";".join([parties[0]] + list(champs)))
        else:
            nouvelles_lignes.append(ligne)
    reecrire_fichier(chemin, nouvelles_lignes)


def generer_id(fichier):
    lignes = lire_fichier(fichier)
    if not lignes:
        return 1
    ids = [int(ligne.split(";")[0]) for ligne in lignes]
    return max(ids) + 1


def lister_clients():
    clients = []
    for ligne in lire_fichier(FICHIER_CLIENTS):
        parties = ligne.split(";")
        if len(parties) == 3:
            clients.append(tuple(parties))
    return clients


def lister_commandes():
    commandes = []
    for ligne in lire_fichier(FICHIER_COMMANDES):
        parties = ligne.split(";")
        if len(parties) == 4:
            commandes.append(tuple(parties))
    return commandes


def compter_clients():
    return len(lister_clients())


def compter_commandes():
    return len(lister_commandes())


def client_existe(cid):
    try:
        identifiant = int(cid)
    except (TypeError, ValueError):
        return False
    return any(int(ligne.split(";")[0]) == identifiant for ligne in lire_fichier(FICHIER_CLIENTS))


def nettoyer_tableau(tree):
    for item in tree.get_children():
        tree.delete(item)


def charger_clients(tree):
    nettoyer_tableau(tree)
    for client in lister_clients():
        tree.insert("", "end", values=client)


def charger_commandes(tree):
    nettoyer_tableau(tree)
    for commande in lister_commandes():
        tree.insert("", "end", values=commande)


def selectionner_client(tree, var_nom, var_tel):
    selection = tree.selection()
    if not selection:
        return
    valeurs = tree.item(selection[0], "values")
    if len(valeurs) >= 3:
        var_nom.set(valeurs[1])
        var_tel.set(valeurs[2])


def ajouter_client(var_nom, var_tel, tree, on_success=None):
    nom = var_nom.get().strip()
    tel = var_tel.get().strip()
    if not nom or not tel:
        messagebox.showwarning("Champ vide", "Veuillez remplir tous les champs.")
        return False

    client_id = generer_id(FICHIER_CLIENTS)
    ecrire_ligne(FICHIER_CLIENTS, f"{client_id};{nom};{tel}")
    charger_clients(tree)
    var_nom.set("")
    var_tel.set("")
    if on_success:
        on_success()
    messagebox.showinfo("Succes", f"Client #{client_id} ajoute.")
    return True


def modifier_client(var_nom, var_tel, tree, on_success=None):
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Selection", "Selectionnez un client a modifier.")
        return False

    nom = var_nom.get().strip()
    tel = var_tel.get().strip()
    if not nom or not tel:
        messagebox.showwarning("Champ vide", "Remplissez les champs avant de modifier.")
        return False

    client_id = tree.item(selection[0], "values")[0]
    modifier_ligne(FICHIER_CLIENTS, int(client_id), nom, tel)
    charger_clients(tree)
    if on_success:
        on_success()
    messagebox.showinfo("Mis a jour", f"Client #{client_id} modifie.")
    return True


def supprimer_client(tree, on_success=None):
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Selection", "Selectionnez un client a supprimer.")
        return False

    client_id = tree.item(selection[0], "values")[0]
    if not messagebox.askyesno("Confirmer", f"Supprimer le client #{client_id} ?"):
        return False

    supprimer_ligne(FICHIER_CLIENTS, int(client_id))
    charger_clients(tree)
    if on_success:
        on_success()
    return True


def ajouter_commande(var_client_id, var_service, tree, on_success=None):
    client_id = var_client_id.get().strip()
    service = var_service.get().strip()

    if not client_id or not service:
        messagebox.showwarning("Erreur", "ID client et service sont obligatoires.")
        return False
    if not client_id.isdigit():
        messagebox.showerror("ID invalide", "L'ID client doit etre numerique.")
        return False
    if not client_existe(client_id):
        messagebox.showerror("Client introuvable", f"Aucun client avec l'ID {client_id}.")
        return False

    numero = generer_id(FICHIER_COMMANDES)
    date_du_jour = datetime.date.today().isoformat()
    ecrire_ligne(FICHIER_COMMANDES, f"{numero};{client_id};{service};{date_du_jour}")
    charger_commandes(tree)
    var_client_id.set("")
    if on_success:
        on_success()
    messagebox.showinfo("Succes", f"Commande #{numero} enregistree.")
    return True


def supprimer_commande(tree, on_success=None):
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Selection", "Selectionnez une commande a supprimer.")
        return False

    numero = tree.item(selection[0], "values")[0]
    if not messagebox.askyesno("Confirmer", f"Supprimer la commande #{numero} ?"):
        return False

    supprimer_ligne(FICHIER_COMMANDES, int(numero))
    charger_commandes(tree)
    if on_success:
        on_success()
    return True
