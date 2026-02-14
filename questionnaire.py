"""
questionnaire.py — 22 questions stratégiques pour évaluer le potentiel de
croissance d'une franchise QSR au Québec.
"""

from typing import Any, Dict, List, Optional


class Question:
    def __init__(
        self,
        qid: str,
        text: str,
        answer_type: str = "single",
        options: Optional[List[dict]] = None,
        help_text: str = "",
        dimension: str = "",
    ):
        self.qid = qid
        self.text = text
        self.answer_type = answer_type
        self.options = options or []
        self.help_text = help_text
        self.dimension = dimension


QUESTIONS: List[Question] = [
    # --- IDENTITÉ & VISION ---
    Question(
        qid="nb_unites",
        text="Combien de points de vente Bellepros sont actuellement en opération?",
        answer_type="single",
        options=[
            {"value": "1", "label": "1 seul (pilote)"},
            {"value": "2-5", "label": "2 à 5"},
            {"value": "6-15", "label": "6 à 15"},
            {"value": "16-30", "label": "16 à 30"},
            {"value": "30+", "label": "Plus de 30"},
        ],
        dimension="real_estate",
    ),
    Question(
        qid="objectif_5ans",
        text="Quel est votre objectif de nombre d'unités dans 5 ans?",
        answer_type="single",
        options=[
            {"value": "5-10", "label": "5 à 10 unités"},
            {"value": "10-25", "label": "10 à 25 unités"},
            {"value": "25-50", "label": "25 à 50 unités"},
            {"value": "50-100", "label": "50 à 100 unités"},
            {"value": "100+", "label": "100+ unités (domination provinciale)"},
        ],
        dimension="real_estate",
    ),
    Question(
        qid="regions_cibles",
        text="Quelles régions du Québec ciblez-vous pour l'expansion?",
        answer_type="multi",
        options=[
            {"value": "montreal", "label": "Grand Montréal"},
            {"value": "quebec_city", "label": "Ville de Québec"},
            {"value": "laval", "label": "Laval"},
            {"value": "longueuil", "label": "Longueuil / Rive-Sud"},
            {"value": "gatineau", "label": "Gatineau / Outaouais"},
            {"value": "sherbrooke", "label": "Sherbrooke / Estrie"},
            {"value": "trois_rivieres", "label": "Trois-Rivières / Mauricie"},
            {"value": "saguenay", "label": "Saguenay–Lac-Saint-Jean"},
            {"value": "drummondville", "label": "Drummondville / Centre-du-Québec"},
            {"value": "rimouski", "label": "Rimouski / Bas-Saint-Laurent"},
        ],
        help_text="Sélectionnez toutes les régions visées.",
        dimension="real_estate",
    ),

    # --- OPÉRATIONS ---
    Question(
        qid="sop_niveau",
        text="Quel est le niveau de standardisation de vos procédures opérationnelles (SOPs)?",
        answer_type="single",
        options=[
            {"value": "complet", "label": "Manuel complet, formation certifiée, audits réguliers"},
            {"value": "partiel", "label": "Documentation partielle, formation informelle"},
            {"value": "minimal", "label": "Quelques procédures écrites, beaucoup oral"},
            {"value": "aucun", "label": "Pas de SOPs formels"},
        ],
        dimension="operations",
    ),
    Question(
        qid="temps_service",
        text="Quel est votre temps de service moyen (commande à remise)?",
        answer_type="single",
        options=[
            {"value": "moins_3min", "label": "Moins de 3 minutes"},
            {"value": "3_5min", "label": "3 à 5 minutes"},
            {"value": "5_8min", "label": "5 à 8 minutes"},
            {"value": "plus_8min", "label": "Plus de 8 minutes"},
        ],
        dimension="operations",
    ),
    Question(
        qid="controle_qualite",
        text="Comment assurez-vous la constance de qualité entre les points de vente?",
        answer_type="single",
        options=[
            {"value": "systeme", "label": "Système d'audit régulier + clients mystères + KPIs"},
            {"value": "audits", "label": "Audits périodiques par la direction"},
            {"value": "informel", "label": "Visites informelles, feedback verbal"},
            {"value": "aucun", "label": "Pas de système de contrôle qualité"},
        ],
        dimension="operations",
    ),

    # --- FINANCES ---
    Question(
        qid="ventes_moyennes",
        text="Quel est le chiffre d'affaires moyen par unité par année?",
        answer_type="single",
        options=[
            {"value": "moins_500k", "label": "Moins de 500 000 $"},
            {"value": "500k_1m", "label": "500 000 $ à 1 M$"},
            {"value": "1m_1_5m", "label": "1 M$ à 1,5 M$"},
            {"value": "1_5m_2m", "label": "1,5 M$ à 2 M$"},
            {"value": "plus_2m", "label": "Plus de 2 M$"},
        ],
        dimension="financial",
    ),
    Question(
        qid="marge_nette",
        text="Quelle est votre marge nette moyenne par unité?",
        answer_type="single",
        options=[
            {"value": "moins_5", "label": "Moins de 5%"},
            {"value": "5_10", "label": "5% à 10%"},
            {"value": "10_15", "label": "10% à 15%"},
            {"value": "15_20", "label": "15% à 20%"},
            {"value": "plus_20", "label": "Plus de 20%"},
        ],
        dimension="financial",
    ),
    Question(
        qid="financement",
        text="Quelle est votre capacité de financement pour l'expansion?",
        answer_type="single",
        options=[
            {"value": "fort", "label": "Ligne de crédit établie + investisseurs confirmés"},
            {"value": "moyen", "label": "Autofinancement possible + relations bancaires"},
            {"value": "limite", "label": "Financement limité, cherche des sources"},
            {"value": "aucun", "label": "Pas de financement identifié pour la croissance"},
        ],
        dimension="financial",
    ),
    Question(
        qid="modele_franchise",
        text="Quel est l'état de votre modèle de franchise?",
        answer_type="single",
        options=[
            {"value": "mature", "label": "Modèle franchise documenté, FDD/circulaire prêt, franchisés actifs"},
            {"value": "en_dev", "label": "Modèle en développement, quelques franchisés"},
            {"value": "corporatif", "label": "100% corporatif, envisage la franchise"},
            {"value": "aucun", "label": "Pas de modèle de franchise, croissance corporative seulement"},
        ],
        dimension="financial",
    ),

    # --- MARQUE ---
    Question(
        qid="notoriete",
        text="Quel est le niveau de notoriété de la marque Bellepros?",
        answer_type="single",
        options=[
            {"value": "provincial", "label": "Reconnue à travers le Québec"},
            {"value": "regional", "label": "Bien connue dans notre région"},
            {"value": "local", "label": "Connue localement seulement"},
            {"value": "nouvelle", "label": "Marque nouvelle, peu de notoriété"},
        ],
        dimension="brand",
    ),
    Question(
        qid="reseaux_sociaux",
        text="Quelle est votre présence sur les réseaux sociaux?",
        answer_type="single",
        options=[
            {"value": "forte", "label": "50K+ abonnés, contenu régulier, engagement élevé"},
            {"value": "moyenne", "label": "10K-50K abonnés, publications régulières"},
            {"value": "faible", "label": "Moins de 10K, publications sporadiques"},
            {"value": "aucune", "label": "Quasi absente des réseaux sociaux"},
        ],
        dimension="brand",
    ),
    Question(
        qid="differenciateur",
        text="Quel est le principal différenciateur de Bellepros vs la concurrence?",
        answer_type="multi",
        options=[
            {"value": "prix", "label": "Meilleur rapport qualité-prix"},
            {"value": "qualite", "label": "Ingrédients supérieurs / frais / locaux"},
            {"value": "vitesse", "label": "Service plus rapide"},
            {"value": "menu_unique", "label": "Menu unique (spécialités exclusives)"},
            {"value": "experience", "label": "Expérience client / ambiance"},
            {"value": "identite_qc", "label": "Identité québécoise authentique"},
            {"value": "techno", "label": "Technologie / commande numérique"},
        ],
        help_text="Sélectionnez vos 2-3 principaux avantages.",
        dimension="brand",
    ),

    # --- MENU ---
    Question(
        qid="menu_engineering",
        text="Faites-vous de l'ingénierie de menu (analyse rentabilité + popularité)?",
        answer_type="single",
        options=[
            {"value": "avance", "label": "Oui — matrice BCG du menu, optimisation continue des marges"},
            {"value": "basique", "label": "Analyse de base des ventes et coûts"},
            {"value": "intuitif", "label": "Décisions de menu intuitives"},
            {"value": "aucun", "label": "Pas d'analyse formelle du menu"},
        ],
        dimension="menu",
    ),
    Question(
        qid="poutine_strategie",
        text="Quelle place occupe la poutine dans votre offre?",
        answer_type="single",
        options=[
            {"value": "vedette", "label": "Produit vedette — multiple variétés, identité de marque"},
            {"value": "important", "label": "Item important au menu, quelques variantes"},
            {"value": "standard", "label": "Poutine standard, rien de spécial"},
            {"value": "absent", "label": "Pas de poutine au menu"},
        ],
        help_text="Au Québec, la poutine est un indicateur clé de positionnement QSR.",
        dimension="menu",
    ),

    # --- TECHNOLOGIE ---
    Question(
        qid="techno_niveau",
        text="Quel est votre niveau d'adoption technologique?",
        answer_type="multi",
        options=[
            {"value": "pos_moderne", "label": "POS moderne avec analytique en temps réel"},
            {"value": "commande_ligne", "label": "Commande en ligne (site web / appli)"},
            {"value": "livraison", "label": "Intégration livraison (UberEats, DoorDash, Skip)"},
            {"value": "fidelite", "label": "Programme de fidélité numérique"},
            {"value": "inventaire", "label": "Gestion d'inventaire automatisée"},
            {"value": "kiosques", "label": "Bornes de commande en restaurant"},
        ],
        help_text="Sélectionnez tout ce qui est en place.",
        dimension="technology",
    ),

    # --- ÉQUIPE ---
    Question(
        qid="roulement",
        text="Quel est votre taux de roulement annuel du personnel?",
        answer_type="single",
        options=[
            {"value": "moins_50", "label": "Moins de 50% (excellent pour QSR)"},
            {"value": "50_100", "label": "50% à 100% (moyenne industrie)"},
            {"value": "100_150", "label": "100% à 150% (problématique)"},
            {"value": "plus_150", "label": "Plus de 150% (critique)"},
        ],
        dimension="people",
    ),
    Question(
        qid="formation",
        text="Comment formez-vous vos employés et gérants?",
        answer_type="single",
        options=[
            {"value": "academie", "label": "Académie de formation Bellepros + certification"},
            {"value": "structure", "label": "Programme de formation structuré avec manuels"},
            {"value": "terrain", "label": "Formation sur le terrain, jumelage"},
            {"value": "minimal", "label": "Formation minimale, apprendre en travaillant"},
        ],
        dimension="people",
    ),

    # --- CHAÎNE D'APPROVISIONNEMENT ---
    Question(
        qid="fournisseurs",
        text="Comment gérez-vous votre chaîne d'approvisionnement?",
        answer_type="single",
        options=[
            {"value": "centralise", "label": "Entrepôt central + distribution unifiée + contrats nationaux"},
            {"value": "negocie", "label": "Contrats négociés avec distributeurs majeurs (Sysco, GFS)"},
            {"value": "mixte", "label": "Mix de fournisseurs locaux et nationaux, peu de contrats"},
            {"value": "adhoc", "label": "Approvisionnement ad hoc, chaque unité gère ses achats"},
        ],
        dimension="supply_chain",
    ),

    # --- RÉGLEMENTATION ---
    Question(
        qid="conformite_qc",
        text="Quel est votre niveau de conformité aux réglementations québécoises?",
        answer_type="multi",
        options=[
            {"value": "mapaq", "label": "MAPAQ — permis et inspections à jour, formation hygiène"},
            {"value": "loi96", "label": "Loi 96 — affichage, menu, communications en français"},
            {"value": "franchise_law", "label": "Loi sur la divulgation en matière de franchise"},
            {"value": "normes_travail", "label": "Normes du travail QC — salaires, horaires, conditions"},
            {"value": "environnement", "label": "Réglementation environnementale (emballages, recyclage)"},
        ],
        help_text="Sélectionnez toutes les conformités en place.",
        dimension="regulatory",
    ),

    # --- CONCURRENCE ---
    Question(
        qid="positionnement_prix",
        text="Comment vous positionnez-vous par rapport aux prix de la concurrence?",
        answer_type="single",
        options=[
            {"value": "premium", "label": "Premium — qualité supérieure justifie un prix plus élevé"},
            {"value": "competitif", "label": "Compétitif — prix similaires aux concurrents majeurs"},
            {"value": "valeur", "label": "Valeur — meilleur rapport quantité/qualité/prix"},
            {"value": "economique", "label": "Économique — le moins cher du marché"},
        ],
        dimension="competitive",
    ),

    # --- AUTO-ÉVALUATION ---
    Question(
        qid="maturite_globale",
        text="Comment évaluez-vous la maturité globale de Bellepros pour scaler au Québec?",
        answer_type="scale",
        help_text="1 = Concept non prouvé, 5 = Machine de guerre prête à dominer la province.",
        dimension="operations",
    ),
]

QUESTION_MAP: Dict[str, Question] = {q.qid: q for q in QUESTIONS}


def default_answers() -> Dict[str, Any]:
    """Réponses démo réalistes pour un QSR québécois en phase de croissance."""
    return {
        "nb_unites": "6-15",
        "objectif_5ans": "25-50",
        "regions_cibles": ["montreal", "quebec_city", "laval", "longueuil", "sherbrooke"],
        "sop_niveau": "partiel",
        "temps_service": "3_5min",
        "controle_qualite": "audits",
        "ventes_moyennes": "1m_1_5m",
        "marge_nette": "10_15",
        "financement": "moyen",
        "modele_franchise": "en_dev",
        "notoriete": "regional",
        "reseaux_sociaux": "moyenne",
        "differenciateur": ["qualite", "identite_qc", "menu_unique"],
        "menu_engineering": "basique",
        "poutine_strategie": "important",
        "techno_niveau": ["pos_moderne", "livraison", "commande_ligne"],
        "roulement": "50_100",
        "formation": "structure",
        "fournisseurs": "negocie",
        "conformite_qc": ["mapaq", "loi96", "normes_travail"],
        "positionnement_prix": "valeur",
        "maturite_globale": 3,
    }
