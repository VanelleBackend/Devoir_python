# Importation de library
from affichage import *

# Création de la fenêtre de l'application
def creer_fenetre():
    root = tk.Tk()
    root.title("GraphiStudio — Gestion des commandes")
    root.geometry("700x520")

    entete = tk.Frame(root, bg="#1E293B", height=48)
    entete.pack(fill="x")
    tk.Label(entete, text="  GraphiStudio — Système de gestion",
            bg="#1E293B", fg="white", font=("Georgia", 15, "bold")
    ).pack(side="left", pady=10)

    onglets = ttk.Notebook(root)
    onglets.pack(fill="both", expand=True, padx=10, pady=10)
    tab_clients   = ttk.Frame(onglets)
    tab_commandes = ttk.Frame(onglets)
    onglets.add(tab_clients,   text="  Clients  ")
    onglets.add(tab_commandes, text="  Commandes  ")
    construire_onglet_clients(tab_clients)
    construire_onglet_commandes(tab_commandes)
    root.mainloop()

if __name__ == "__main__":
    creer_fenetre()