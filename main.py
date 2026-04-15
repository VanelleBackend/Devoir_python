# Importation de library
from affichage import *

# Creation de la splash screen (Ecran de démarrage)
def splash_screen():
        splash = tk.Tk()
        splash.overrideredirect(True)  # enlever barre fenêtre
        splash.geometry("700x520+150+100")  # taille + position
        splash.configure(bg="#1E293B")

        tk.Label(
            splash,
            text="GraphiStudio",
            fg="white",
            bg="#1E293B",
            font=("Poppins", 20, "bold")
        ).pack(pady=40)

        tk.Label(
            splash,
            text="Chargement en cours...",
            fg="#94A3B8",
            bg="#1E293B",
            font=("Arial", 10)
        ).pack()

        # Barre de progression(Changement) simulée pour la splash sreen(Ecran démarrage)
        progress = ttk.Progressbar(splash, orient="horizontal", length=250, mode="determinate")
        progress.pack(pady=20)
        def charger():
            for i in range(101):
                progress["value"] = i
                splash.update_idletasks()
                splash.after(20)
        charger()

        # fermer splash après 2 secondes
        splash.after(2000, splash.destroy)

        splash.mainloop()

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
    splash_screen()
    creer_fenetre()