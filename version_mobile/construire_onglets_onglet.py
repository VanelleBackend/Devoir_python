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

    colonnes = ("id", "nom", "telephone")

    tree_clients = ttk.Treeview(
        parent,
        columns=colonnes,
        show="headings",
        height=10
    )

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