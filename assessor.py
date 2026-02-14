"""
assessor.py — Moteur d'évaluation pour la Console de Croissance Bellepros.

Prend les réponses au questionnaire et produit un score par dimension,
un score global, des lacunes, des recommandations et une feuille de route.
"""

from typing import Any, Dict, List, Optional
from config import DIMENSIONS, ALL_DIMENSION_KEYS, QUEBEC_REGIONS, COMPETITORS, get_growth_tier


# ---------------------------------------------------------------------------
# Scoring maps — each answer maps to a 0-100 contribution
# ---------------------------------------------------------------------------

SCORE_MAPS = {
    # --- REAL ESTATE / EXPANSION ---
    "nb_unites": {
        "1": 20, "2-5": 40, "6-15": 60, "16-30": 80, "30+": 95,
    },
    "objectif_5ans": {
        "5-10": 30, "10-25": 50, "25-50": 70, "50-100": 85, "100+": 95,
    },
    # --- OPERATIONS ---
    "sop_niveau": {
        "complet": 95, "partiel": 60, "minimal": 35, "aucun": 10,
    },
    "temps_service": {
        "moins_3min": 95, "3_5min": 75, "5_8min": 45, "plus_8min": 15,
    },
    "controle_qualite": {
        "systeme": 95, "audits": 65, "informel": 35, "aucun": 10,
    },
    # --- FINANCIAL ---
    "ventes_moyennes": {
        "moins_500k": 20, "500k_1m": 45, "1m_1_5m": 70, "1_5m_2m": 85, "plus_2m": 95,
    },
    "marge_nette": {
        "moins_5": 15, "5_10": 40, "10_15": 65, "15_20": 85, "plus_20": 95,
    },
    "financement": {
        "fort": 95, "moyen": 65, "limite": 35, "aucun": 10,
    },
    "modele_franchise": {
        "mature": 95, "en_dev": 60, "corporatif": 40, "aucun": 20,
    },
    # --- BRAND ---
    "notoriete": {
        "provincial": 95, "regional": 65, "local": 35, "nouvelle": 15,
    },
    "reseaux_sociaux": {
        "forte": 95, "moyenne": 65, "faible": 35, "aucune": 10,
    },
    # --- MENU ---
    "menu_engineering": {
        "avance": 95, "basique": 60, "intuitif": 30, "aucun": 10,
    },
    "poutine_strategie": {
        "vedette": 95, "important": 70, "standard": 40, "absent": 15,
    },
    # --- PEOPLE ---
    "roulement": {
        "moins_50": 95, "50_100": 65, "100_150": 35, "plus_150": 10,
    },
    "formation": {
        "academie": 95, "structure": 70, "terrain": 40, "minimal": 15,
    },
    # --- SUPPLY CHAIN ---
    "fournisseurs": {
        "centralise": 95, "negocie": 70, "mixte": 40, "adhoc": 15,
    },
    # --- COMPETITIVE ---
    "positionnement_prix": {
        "premium": 70, "competitif": 60, "valeur": 80, "economique": 50,
    },
}

# Multi-select scoring (score = proportion of items selected * max)
MULTI_SCORE_CONFIG = {
    "regions_cibles": {"max": 80, "dimension": "real_estate"},
    "differenciateur": {"max": 90, "dimension": "brand"},
    "techno_niveau": {"max": 95, "dimension": "technology"},
    "conformite_qc": {"max": 95, "dimension": "regulatory"},
}

# Which questions feed each dimension
DIMENSION_QUESTIONS = {
    "operations": ["sop_niveau", "temps_service", "controle_qualite", "maturite_globale"],
    "brand": ["notoriete", "reseaux_sociaux", "differenciateur"],
    "financial": ["ventes_moyennes", "marge_nette", "financement", "modele_franchise"],
    "real_estate": ["nb_unites", "objectif_5ans", "regions_cibles"],
    "supply_chain": ["fournisseurs"],
    "technology": ["techno_niveau"],
    "people": ["roulement", "formation"],
    "regulatory": ["conformite_qc"],
    "menu": ["menu_engineering", "poutine_strategie"],
    "competitive": ["positionnement_prix"],
}


# ---------------------------------------------------------------------------
# Gap & recommendation knowledge base
# ---------------------------------------------------------------------------

GAPS_DB = {
    "operations": {
        "low": [
            "Absence de procédures opérationnelles standardisées — impossible de garantir l'uniformité lors de l'expansion.",
            "Temps de service trop long — les clients QSR s'attendent à moins de 5 minutes.",
        ],
        "medium": [
            "SOPs partiellement documentés — risque d'incohérence entre les unités.",
            "Contrôle qualité informel — les problèmes ne sont détectés qu'après plaintes clients.",
        ],
        "recommendations": [
            "Créer un manuel opérationnel complet (« Playbook Bellepros ») couvrant chaque poste et procédure.",
            "Implanter un programme de clients mystères mensuel avec scorecard standardisé.",
            "Viser un temps de service moyen sous 4 minutes — benchmark QSR compétitif au Québec.",
            "Mettre en place des audits opérationnels trimestriels avec grille de notation.",
        ],
    },
    "brand": {
        "low": [
            "Notoriété limitée — la marque n'est pas assez connue pour attirer des franchisés ou des clients dans de nouveaux marchés.",
            "Présence sociale quasi inexistante — les Québécois découvrent les restos sur Instagram et TikTok.",
        ],
        "medium": [
            "Notoriété régionale seulement — besoin de campagnes provinciales avant d'expansion.",
            "Différenciation floue — le client ne sait pas pourquoi choisir Bellepros vs Valentine ou A&W.",
        ],
        "recommendations": [
            "Lancer une campagne de marque provinciale mettant en valeur l'identité québécoise authentique.",
            "Investir dans le contenu TikTok/Instagram — les food videos virales sont le marketing QSR #1.",
            "Développer un slogan/positionnement clair qui résume l'avantage Bellepros en 5 mots.",
            "Créer un programme d'ambassadeurs locaux dans chaque nouvelle région cible.",
        ],
    },
    "financial": {
        "low": [
            "Chiffre d'affaires par unité insuffisant pour justifier l'expansion — le modèle n'est pas prouvé.",
            "Aucun financement identifié — impossible de scaler sans capital.",
        ],
        "medium": [
            "Marges sous pression — il faut au moins 10-15% de marge nette pour un modèle franchise viable.",
            "Modèle franchise en développement — les franchisés potentiels ont besoin d'un FDD solide.",
        ],
        "recommendations": [
            "Documenter l'économie unitaire complète (Item 19 du FDD) pour attirer les franchisés.",
            "Viser 1,5 M$+ de ventes par unité — c'est le seuil de crédibilité franchise au Québec.",
            "Préparer un plan financier d'expansion 5 ans avec scénarios conservateur/modéré/agressif.",
            "Explorer le financement BDC (Banque de développement du Canada) — programmes spécifiques franchise.",
            "Optimiser le food cost à 28-32% — chaque point de marge compte x nombre d'unités.",
        ],
    },
    "real_estate": {
        "low": [
            "Trop peu d'unités pour prouver la réplicabilité du concept.",
        ],
        "medium": [
            "Stratégie d'expansion trop ambitieuse vs capacité actuelle — risque de dilution.",
        ],
        "recommendations": [
            "Établir des critères de sélection de site formels (population, revenus, trafic, concurrence, visibilité).",
            "Prioriser les marchés à faible densité QSR : Trois-Rivières, Drummondville, Sherbrooke.",
            "Négocier des baux avec clauses de protection territoriale pour chaque franchisé.",
            "Cibler les corridors autoroutiers pour des unités drive-thru à haut volume.",
        ],
    },
    "supply_chain": {
        "low": [
            "Approvisionnement ad hoc — impossible de maintenir qualité et coûts à grande échelle.",
        ],
        "medium": [
            "Chaîne d'approvisionnement fragile — dépendance à quelques fournisseurs sans contrats solides.",
        ],
        "recommendations": [
            "Négocier des contrats nationaux avec Sysco ou GFS pour verrouiller les prix et la qualité.",
            "Développer un réseau de fournisseurs locaux québécois comme avantage concurrentiel (« fait au Québec »).",
            "Planifier un entrepôt central ou partenariat 3PL à partir de 20+ unités.",
            "Créer des spécifications produit détaillées pour chaque ingrédient clé.",
        ],
    },
    "technology": {
        "low": [
            "Retard technologique critique — les concurrents comme McDonald's et Tim Hortons investissent massivement.",
        ],
        "medium": [
            "Adoption technologique partielle — manque d'intégration entre les systèmes.",
        ],
        "recommendations": [
            "Implanter un POS moderne avec tableau de bord en temps réel (Square, Lightspeed, TouchBistro).",
            "Lancer la commande en ligne propre à Bellepros (pas seulement UberEats — garder la marge).",
            "Créer un programme de fidélité numérique — les données clients sont un actif stratégique.",
            "Intégrer les plateformes de livraison (UberEats, DoorDash, Skip) avec gestion centralisée.",
        ],
    },
    "people": {
        "low": [
            "Taux de roulement critique — coûts de recrutement et formation qui grugent les marges.",
            "Formation minimale — qualité de service inconstante.",
        ],
        "medium": [
            "Roulement dans la moyenne industrie mais peut être amélioré avec de meilleures conditions.",
        ],
        "recommendations": [
            "Créer l'Académie Bellepros — programme de formation structuré avec certification.",
            "Implanter un plan de carrière clair : équipier → chef d'équipe → assistant-gérant → gérant → multi-unités.",
            "Offrir des avantages compétitifs : repas gratuits, horaires flexibles, programme de reconnaissance.",
            "Viser un taux de roulement sous 60% — chaque employé retenu = 5 000$+ économisé.",
        ],
    },
    "regulatory": {
        "low": [
            "Non-conformité réglementaire — risque d'amendes MAPAQ et plaintes Loi 96.",
        ],
        "medium": [
            "Conformité partielle — certaines obligations négligées.",
        ],
        "recommendations": [
            "S'assurer que CHAQUE unité a ses permis MAPAQ à jour et que le personnel est formé en hygiène.",
            "Audit Loi 96 : tout affichage, menu, site web et appli doit être en français d'abord.",
            "Préparer la circulaire de divulgation de franchise conforme à la loi québécoise.",
            "Implanter un calendrier de conformité avec rappels automatisés.",
        ],
    },
    "menu": {
        "low": [
            "Aucune analyse de menu — des items non rentables drainent les marges.",
            "La poutine est absente ou négligée — erreur stratégique au Québec.",
        ],
        "medium": [
            "Analyse de menu basique — potentiel d'optimisation significatif.",
        ],
        "recommendations": [
            "Faire une matrice BCG du menu : étoiles (populaire + rentable), vaches à lait, dilemmes, poids morts.",
            "Développer 3-5 poutines signature exclusives — c'est votre arme secrète au Québec.",
            "Implanter un calendrier d'innovation : 2-3 items saisonniers/à durée limitée par année.",
            "Tester des items « Instagram-worthy » — les plats photogéniques = marketing gratuit.",
        ],
    },
    "competitive": {
        "low": [
            "Positionnement prix flou — le client ne perçoit pas la valeur par rapport aux alternatives.",
        ],
        "medium": [
            "Positionnement correct mais pas assez distinctif pour créer une préférence de marque.",
        ],
        "recommendations": [
            "Cartographier les prix de chaque concurrent direct dans chaque zone cible.",
            "Créer un « pourquoi Bellepros » clair en 3 points — qualité, identité québécoise, rapport qualité-prix.",
            "Exploiter les faiblesses concurrentielles : Tim Hortons (qualité perçue), Subway (déclin), Valentine (vieillissement).",
            "Miser sur l'identité locale authentique — c'est l'avantage que McDonald's et Subway ne peuvent jamais copier.",
        ],
    },
}


def _score_single(qid: str, answer: Any) -> float:
    if qid == "maturite_globale":
        return float(answer) / 5.0 * 100.0 if isinstance(answer, (int, float)) else 50.0
    mapping = SCORE_MAPS.get(qid, {})
    return float(mapping.get(str(answer), 50))


def _score_multi(qid: str, answer: Any) -> float:
    config = MULTI_SCORE_CONFIG.get(qid)
    if not config or not isinstance(answer, list):
        return 50.0
    total_options = {
        "regions_cibles": 10,
        "differenciateur": 7,
        "techno_niveau": 6,
        "conformite_qc": 5,
    }
    max_opts = total_options.get(qid, 5)
    ratio = min(len(answer) / max_opts, 1.0)
    return ratio * config["max"]


def _compute_dimension_score(dim_key: str, answers: Dict[str, Any]) -> float:
    questions = DIMENSION_QUESTIONS.get(dim_key, [])
    if not questions:
        return 50.0
    scores = []
    for qid in questions:
        if qid not in answers:
            continue
        if qid in MULTI_SCORE_CONFIG:
            scores.append(_score_multi(qid, answers[qid]))
        else:
            scores.append(_score_single(qid, answers[qid]))
    return sum(scores) / len(scores) if scores else 50.0


def _get_gaps_and_recs(dim_key: str, score: float) -> Dict[str, List[str]]:
    db = GAPS_DB.get(dim_key, {})
    gaps = []
    recs = []
    if score < 40:
        gaps.extend(db.get("low", []))
        recs.extend(db.get("recommendations", []))
    elif score < 70:
        gaps.extend(db.get("medium", []))
        recs.extend(db.get("recommendations", [])[:2])
    return {"gaps": gaps, "recommendations": recs}


def _recommend_regions(answers: Dict[str, Any], overall_score: float) -> List[Dict[str, Any]]:
    """Recommande les meilleures régions pour l'expansion basées sur le profil."""
    targeted = answers.get("regions_cibles", [])
    nb = answers.get("nb_unites", "1")

    # Smaller chains should start with lower-competition regions
    size_factor = {"1": 0, "2-5": 1, "6-15": 2, "16-30": 3, "30+": 4}.get(nb, 0)

    region_scores = []
    for key, region in QUEBEC_REGIONS.items():
        score = 50.0
        is_targeted = key in targeted

        # Bonus for targeted regions
        if is_targeted:
            score += 15

        # Score based on potential
        pot_map = {"Élevé": 25, "Moyen-Élevé": 20, "Moyen": 10}
        score += pot_map.get(region["potentiel"], 5)

        # Smaller chains benefit more from low-density markets
        density_map = {"Très faible": 20, "Faible": 18, "Faible-Moyen": 15, "Moyen": 10, "Moyen-Élevé": 5, "Élevée": 0, "Très élevée": -5}
        density_bonus = density_map.get(region["densite_qsr"], 0)
        if size_factor < 2:
            score += density_bonus
        else:
            score += density_bonus * 0.5

        # Cost advantage
        if region["loyer_moyen_pied2"] < 20:
            score += 10

        # Clamp
        score = max(0, min(100, score))

        priority = "Prioritaire" if score >= 75 else "Recommandée" if score >= 60 else "Secondaire" if score >= 45 else "À long terme"

        region_scores.append({
            "key": key,
            "name": region["name"],
            "score": score,
            "priority": priority,
            "population": region["population"],
            "loyer": region["loyer_moyen_pied2"],
            "densite": region["densite_qsr"],
            "potentiel": region["potentiel"],
            "notes": region["notes"],
            "targeted": is_targeted,
        })

    region_scores.sort(key=lambda x: x["score"], reverse=True)
    return region_scores


def _competitive_analysis(answers: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Analyse concurrentielle contextuelle."""
    diffs = answers.get("differenciateur", [])
    prix = answers.get("positionnement_prix", "competitif")

    analysis = []
    for key, comp in COMPETITORS.items():
        vulnerability = 50  # baseline
        opportunities = []

        # Price positioning creates different competitive dynamics
        if prix == "valeur" and comp["niveau_menace"] in ("Élevé", "Moyen-Élevé"):
            vulnerability += 10
            opportunities.append(f"Positionnement valeur vs {comp['name']} en hausse de prix")

        if "identite_qc" in diffs and key in ("mcdonalds", "subway", "aw"):
            vulnerability += 15
            opportunities.append(f"Identité québécoise authentique vs {comp['name']} (marque internationale)")

        if "qualite" in diffs and key in ("tim_hortons", "subway", "harveys"):
            vulnerability += 15
            opportunities.append(f"Qualité supérieure vs {comp['name']} ({comp['faiblesse']})")

        if "menu_unique" in diffs and key in ("mcdonalds", "subway", "tim_hortons"):
            vulnerability += 10
            opportunities.append(f"Menu distinctif vs l'offre générique de {comp['name']}")

        if key in ("valentine", "harveys"):
            vulnerability += 10
            opportunities.append(f"{comp['name']} en déclin — territoire à prendre")

        analysis.append({
            "name": comp["name"],
            "unites_qc": comp["unites_qc"],
            "force": comp["force"],
            "faiblesse": comp["faiblesse"],
            "niveau_menace": comp["niveau_menace"],
            "vulnerabilite": min(vulnerability, 100),
            "opportunites": opportunities,
        })

    analysis.sort(key=lambda x: x["vulnerabilite"], reverse=True)
    return analysis


def run_assessment(
    answers: Dict[str, Any],
    dimensions: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Execute l'évaluation complète et retourne les résultats."""

    dims = dimensions or ALL_DIMENSION_KEYS

    # Score each dimension
    dim_results = {}
    for dim_key in dims:
        dim_info = DIMENSIONS[dim_key]
        score = _compute_dimension_score(dim_key, answers)
        gaps_recs = _get_gaps_and_recs(dim_key, score)

        if score >= 70:
            priority = "Faible"
        elif score >= 50:
            priority = "Moyen"
        elif score >= 30:
            priority = "Élevé"
        else:
            priority = "Critique"

        dim_results[dim_key] = {
            "name": dim_info["name"],
            "short": dim_info["short"],
            "score": score,
            "weight": dim_info["weight"],
            "priority": priority,
            "gaps": gaps_recs["gaps"],
            "recommendations": gaps_recs["recommendations"],
        }

    # Weighted overall score
    total_weight = sum(DIMENSIONS[d]["weight"] for d in dims)
    overall = sum(
        dim_results[d]["score"] * DIMENSIONS[d]["weight"]
        for d in dims
    ) / total_weight if total_weight > 0 else 0

    tier = get_growth_tier(overall)

    # Regional analysis
    regions = _recommend_regions(answers, overall)

    # Competitive analysis
    competitors = _competitive_analysis(answers)

    # Build roadmap
    roadmap = _build_roadmap(dim_results)

    return {
        "overall_score": overall,
        "tier": tier,
        "stars": tier["stars"],
        "dimensions_assessed": dims,
        "dimension_results": dim_results,
        "regions": regions,
        "competitors": competitors,
        "roadmap": roadmap,
    }


def _build_roadmap(dim_results: Dict[str, Any]) -> Dict[str, List[str]]:
    """Construit la feuille de route priorisée."""
    critique = []
    court_terme = []
    moyen_terme = []
    long_terme = []

    for dim_key, res in dim_results.items():
        for rec in res["recommendations"]:
            item = f"[{res['short']}] {rec}"
            if res["priority"] == "Critique":
                critique.append(item)
            elif res["priority"] == "Élevé":
                court_terme.append(item)
            elif res["priority"] == "Moyen":
                moyen_terme.append(item)
            else:
                long_terme.append(item)

    return {
        "critique": critique,
        "court_terme": court_terme,
        "moyen_terme": moyen_terme,
        "long_terme": long_terme,
    }
