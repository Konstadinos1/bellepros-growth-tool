"""
config.py — Console de Croissance Bellepros — Configuration.

Intelligence de marché québécois, profils de concurrents, dimensions de
croissance et données régionales intégrées.
"""

# ---------------------------------------------------------------------------
# Dimensions de croissance
# ---------------------------------------------------------------------------
DIMENSIONS = {
    "operations": {
        "name": "Excellence Opérationnelle",
        "short": "Opérations",
        "description": "Uniformité des procédures, efficacité cuisine, rapidité de service, contrôle qualité",
        "weight": 0.15,
    },
    "brand": {
        "name": "Marque & Positionnement",
        "short": "Marque",
        "description": "Notoriété, différenciation, fidélité client, présence sociale",
        "weight": 0.12,
    },
    "financial": {
        "name": "Santé Financière",
        "short": "Finances",
        "description": "Économie unitaire, modèle de franchise, capacité de financement, flux de trésorerie",
        "weight": 0.15,
    },
    "real_estate": {
        "name": "Immobilier & Expansion",
        "short": "Immobilier",
        "description": "Sélection de sites, couverture marché, ciblage démographique, stratégie de bail",
        "weight": 0.12,
    },
    "supply_chain": {
        "name": "Chaîne d'Approvisionnement",
        "short": "Approvisionnement",
        "description": "Relations fournisseurs, contrôle des coûts, approvisionnement local, distribution",
        "weight": 0.10,
    },
    "technology": {
        "name": "Technologie & Numérique",
        "short": "Techno",
        "description": "POS, commande en ligne, appli fidélité, analytique, intégration livraison",
        "weight": 0.10,
    },
    "people": {
        "name": "Équipe & Culture",
        "short": "Équipe",
        "description": "Recrutement, rétention, programmes de formation, main-d'œuvre francophone",
        "weight": 0.10,
    },
    "regulatory": {
        "name": "Réglementation & Conformité QC",
        "short": "Réglementation",
        "description": "MAPAQ, Loi 96 (langue française), divulgation franchise, normes du travail",
        "weight": 0.06,
    },
    "menu": {
        "name": "Stratégie Menu & Produits",
        "short": "Menu",
        "description": "Ingénierie de menu, goûts locaux, marges, pipeline d'innovation, jeu de poutine",
        "weight": 0.05,
    },
    "competitive": {
        "name": "Positionnement Concurrentiel",
        "short": "Concurrence",
        "description": "vs Tim Hortons, McDonald's, A&W, St-Hubert, Valentine, Ashton, Dic Ann's",
        "weight": 0.05,
    },
}

ALL_DIMENSION_KEYS = list(DIMENSIONS.keys())

# ---------------------------------------------------------------------------
# Régions du Québec & données de marché
# ---------------------------------------------------------------------------
QUEBEC_REGIONS = {
    "montreal": {
        "name": "Grand Montréal",
        "population": 4_300_000,
        "densite_qsr": "Très élevée",
        "loyer_moyen_pied2": 35.0,
        "potentiel": "Moyen",
        "notes": "Saturé mais volume massif. Idéal pour flagship / construction de marque.",
    },
    "quebec_city": {
        "name": "Ville de Québec (RCN)",
        "population": 830_000,
        "densite_qsr": "Élevée",
        "loyer_moyen_pied2": 22.0,
        "potentiel": "Élevé",
        "notes": "Forte loyauté locale. Territoire d'Ashton — différenciation obligatoire.",
    },
    "laval": {
        "name": "Laval",
        "population": 440_000,
        "densite_qsr": "Élevée",
        "loyer_moyen_pied2": 28.0,
        "potentiel": "Moyen-Élevé",
        "notes": "Banlieue familiale. Service au volant essentiel.",
    },
    "longueuil": {
        "name": "Longueuil / Rive-Sud",
        "population": 420_000,
        "densite_qsr": "Moyen-Élevé",
        "loyer_moyen_pied2": 24.0,
        "potentiel": "Élevé",
        "notes": "Zones sous-desservies près des stations REM. Sites adjacents au transport.",
    },
    "gatineau": {
        "name": "Gatineau / Outaouais",
        "population": 340_000,
        "densite_qsr": "Moyen",
        "loyer_moyen_pied2": 20.0,
        "potentiel": "Élevé",
        "notes": "Transfrontalier avec Ottawa. Marché bilingue, loyers plus bas.",
    },
    "sherbrooke": {
        "name": "Sherbrooke / Estrie",
        "population": 230_000,
        "densite_qsr": "Moyen",
        "loyer_moyen_pied2": 16.0,
        "potentiel": "Élevé",
        "notes": "Ville universitaire. Démographie plus jeune, sensible au prix.",
    },
    "trois_rivieres": {
        "name": "Trois-Rivières / Mauricie",
        "population": 160_000,
        "densite_qsr": "Faible-Moyen",
        "loyer_moyen_pied2": 14.0,
        "potentiel": "Élevé",
        "notes": "Peu de concurrence. Forte identité locale. Expansion économique.",
    },
    "saguenay": {
        "name": "Saguenay–Lac-Saint-Jean",
        "population": 160_000,
        "densite_qsr": "Faible",
        "loyer_moyen_pied2": 12.0,
        "potentiel": "Moyen-Élevé",
        "notes": "Fierté locale intense. Gagner la confiance. Loyer bas = marge élevée.",
    },
    "drummondville": {
        "name": "Drummondville / Centre-du-Québec",
        "population": 100_000,
        "densite_qsr": "Faible",
        "loyer_moyen_pied2": 13.0,
        "potentiel": "Élevé",
        "notes": "Ville corridor autoroutier. Idéal service au volant + hub livraison.",
    },
    "rimouski": {
        "name": "Rimouski / Bas-Saint-Laurent",
        "population": 55_000,
        "densite_qsr": "Très faible",
        "loyer_moyen_pied2": 10.0,
        "potentiel": "Moyen",
        "notes": "Ancrage régional. Peu de concurrence mais petit marché.",
    },
}

# ---------------------------------------------------------------------------
# Concurrents QSR au Québec
# ---------------------------------------------------------------------------
COMPETITORS = {
    "tim_hortons": {
        "name": "Tim Hortons",
        "unites_qc": 900,
        "force": "Omniprésence, déjeuner, habitude café",
        "faiblesse": "Fatigue du menu, perception qualité en baisse",
        "niveau_menace": "Élevé",
    },
    "mcdonalds": {
        "name": "McDonald's",
        "unites_qc": 300,
        "force": "Marque mondiale, investissement techno, uniformité",
        "faiblesse": "Pas 'local', prix en hausse",
        "niveau_menace": "Élevé",
    },
    "subway": {
        "name": "Subway",
        "unites_qc": 400,
        "force": "Nombre d'unités, faible coût de franchise",
        "faiblesse": "Déclin de la marque, fermetures en série",
        "niveau_menace": "Moyen",
    },
    "st_hubert": {
        "name": "St-Hubert",
        "unites_qc": 120,
        "force": "Icône québécoise, salle à manger + livraison, niche rôtisserie",
        "faiblesse": "Prix plus élevé, service plus lent",
        "niveau_menace": "Moyen",
    },
    "valentine": {
        "name": "Valentine",
        "unites_qc": 100,
        "force": "Nostalgie québécoise, patrimoine hot-dog + poutine",
        "faiblesse": "Marque vieillissante, peu d'innovation",
        "niveau_menace": "Moyen",
    },
    "ashton": {
        "name": "Ashton",
        "unites_qc": 25,
        "force": "Culte à Québec, roi de la poutine",
        "faiblesse": "Régional seulement, pas de modèle franchise",
        "niveau_menace": "Faible (régional)",
    },
    "dic_anns": {
        "name": "Dic Ann's",
        "unites_qc": 12,
        "force": "Classique culte montréalais, burgers pas chers",
        "faiblesse": "Minuscule empreinte, pas d'ambition de croissance",
        "niveau_menace": "Faible (régional)",
    },
    "aw": {
        "name": "A&W",
        "unites_qc": 100,
        "force": "Positionnement qualité, boeuf sans hormones, bon branding",
        "faiblesse": "Empreinte plus petite, moins québécois",
        "niveau_menace": "Moyen-Élevé",
    },
    "harveys": {
        "name": "Harvey's",
        "unites_qc": 60,
        "force": "Burgers personnalisables, marque canadienne",
        "faiblesse": "Pertinence en déclin, moins de points de vente",
        "niveau_menace": "Faible",
    },
}

# ---------------------------------------------------------------------------
# Niveaux de croissance
# ---------------------------------------------------------------------------
GROWTH_TIERS = {
    "dominator": {"min": 85, "label": "Dominateur du Marché", "stars": 5, "desc": "Prêt pour une expansion agressive à travers le Québec"},
    "contender": {"min": 70, "label": "Compétiteur Solide", "stars": 4, "desc": "Base solide — expansion ciblée recommandée"},
    "builder": {"min": 55, "label": "Bâtisseur de Fondations", "stars": 3, "desc": "Solidifier les fondamentaux avant de scaler"},
    "starter": {"min": 40, "label": "Phase de Démarrage", "stars": 2, "desc": "Se concentrer sur le modèle dans 1-2 emplacements"},
    "concept": {"min": 0, "label": "Phase Conceptuelle", "stars": 1, "desc": "Valider l'adéquation produit-marché avant tout"},
}


def get_growth_tier(score: float) -> dict:
    for tier in GROWTH_TIERS.values():
        if score >= tier["min"]:
            return tier
    return list(GROWTH_TIERS.values())[-1]
