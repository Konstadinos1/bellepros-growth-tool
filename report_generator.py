"""
report_generator.py — Génère le rapport Markdown de croissance Bellepros.
"""

from typing import Any, Dict
from datetime import datetime


def generate_report(assessment: Dict[str, Any], org_name: str = "Bellepros") -> str:
    tier = assessment["tier"]
    overall = assessment["overall_score"]
    stars = "★" * assessment["stars"] + "☆" * (5 - assessment["stars"])

    lines = [
        f"# Rapport de Stratégie de Croissance — {org_name}",
        f"**Date :** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Dimensions évaluées :** {len(assessment['dimensions_assessed'])}",
        "",
        "---",
        "",
        "## Sommaire Exécutif",
        "",
        f"### Niveau de Préparation à la Croissance : {stars} ({overall:.0f}/100)",
        f"**Classification :** {tier['label']} — {tier['desc']}",
        "",
        "| Dimension | Score | Priorité |",
        "|-----------|-------|----------|",
    ]

    for dim_key in assessment["dimensions_assessed"]:
        res = assessment["dimension_results"][dim_key]
        lines.append(f"| {res['name']} | {res['score']:.0f}% | {res['priority']} |")

    lines += ["", "---", "", "## Analyse Détaillée par Dimension", ""]

    for dim_key in assessment["dimensions_assessed"]:
        res = assessment["dimension_results"][dim_key]
        lines.append(f"### {res['name']}")
        lines.append(f"**Score :** {res['score']:.0f}% | **Priorité :** {res['priority']}")
        lines.append("")
        if res["gaps"]:
            lines.append("**Lacunes identifiées :**")
            for g in res["gaps"]:
                lines.append(f"- ⚠️ {g}")
            lines.append("")
        if res["recommendations"]:
            lines.append("**Recommandations :**")
            for i, r in enumerate(res["recommendations"], 1):
                lines.append(f"{i}. {r}")
            lines.append("")
        lines.append("---")
        lines.append("")

    # Regional analysis
    lines += ["## Analyse Régionale — Marchés Prioritaires", ""]
    lines.append("| Région | Population | Densité QSR | Loyer moy. $/pi² | Potentiel | Priorité |")
    lines.append("|--------|-----------|-------------|-------------------|-----------|----------|")
    for reg in assessment["regions"]:
        star = " ⭐" if reg["targeted"] else ""
        lines.append(
            f"| {reg['name']}{star} | {reg['population']:,} | {reg['densite']} | "
            f"{reg['loyer']:.0f}$ | {reg['potentiel']} | {reg['priority']} |"
        )
    lines += ["", "*⭐ = région ciblée par le client*", ""]

    lines.append("### Notes par région")
    for reg in assessment["regions"][:5]:
        lines.append(f"- **{reg['name']}** — {reg['notes']}")
    lines += ["", "---", ""]

    # Competitive analysis
    lines += ["## Analyse Concurrentielle", ""]
    lines.append("| Concurrent | Unités QC | Menace | Vulnérabilité | Opportunité |")
    lines.append("|------------|-----------|--------|---------------|-------------|")
    for comp in assessment["competitors"]:
        opp = comp["opportunites"][0] if comp["opportunites"] else "—"
        lines.append(
            f"| {comp['name']} | {comp['unites_qc']} | {comp['niveau_menace']} | "
            f"{comp['vulnerabilite']}% | {opp} |"
        )
    lines += ["", "---", ""]

    # Roadmap
    roadmap = assessment["roadmap"]
    lines += ["## Feuille de Route d'Expansion", ""]

    if roadmap["critique"]:
        lines.append("### 🔴 Actions Immédiates (0-3 mois) — Critique")
        for item in roadmap["critique"]:
            lines.append(f"- [ ] {item}")
        lines.append("")

    if roadmap["court_terme"]:
        lines.append("### 🟠 Court Terme (3-6 mois) — Priorité Élevée")
        for item in roadmap["court_terme"]:
            lines.append(f"- [ ] {item}")
        lines.append("")

    if roadmap["moyen_terme"]:
        lines.append("### 🟡 Moyen Terme (6-12 mois) — Priorité Moyenne")
        for item in roadmap["moyen_terme"]:
            lines.append(f"- [ ] {item}")
        lines.append("")

    if roadmap["long_terme"]:
        lines.append("### 🟢 Long Terme (12+ mois) — Amélioration Continue")
        for item in roadmap["long_terme"]:
            lines.append(f"- [ ] {item}")
        lines.append("")

    lines += [
        "---",
        f"*Rapport généré par la Console de Croissance Bellepros — {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
    ]

    return "\n".join(lines)
