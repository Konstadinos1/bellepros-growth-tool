"""
main.py — CLI pour la Console de Croissance Bellepros.
"""

import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from questionnaire import default_answers
from assessor import run_assessment
from report_generator import generate_report

console = Console()


def main():
    parser = argparse.ArgumentParser(description="Console de Croissance Bellepros — CLI")
    parser.add_argument("--defaults", action="store_true", help="Utiliser les réponses démo")
    parser.add_argument("--org", default="Bellepros", help="Nom de l'organisation")
    args = parser.parse_args()

    console.print(Panel(
        "[bold white]🍟 Console de Croissance Bellepros[/bold white]\n"
        "Stratégie d'expansion QSR — Province de Québec",
        style="bold red",
    ))

    if args.defaults:
        console.print("Utilisation des réponses démo...\n")
        answers = default_answers()
    else:
        console.print("[yellow]Mode interactif non implémenté — utilisez --defaults ou l'interface web.[/yellow]")
        return

    assessment = run_assessment(answers)
    tier = assessment["tier"]
    overall = assessment["overall_score"]
    stars = "★" * assessment["stars"] + "☆" * (5 - assessment["stars"])

    console.print(Panel(
        f"[bold]{stars}  {overall:.0f}/100[/bold]\n{tier['label']} — {tier['desc']}",
        title="🏆 Niveau de Croissance",
    ))

    # Dimension table
    table = Table(title="Scores par Dimension")
    table.add_column("Dimension", style="bold")
    table.add_column("Score", justify="center")
    table.add_column("Priorité", justify="center")
    table.add_column("Lacune principale", max_width=50)

    for dim_key in assessment["dimensions_assessed"]:
        res = assessment["dimension_results"][dim_key]
        gap = res["gaps"][0][:50] if res["gaps"] else "—"
        table.add_row(
            res["name"],
            f"{res['score']:.0f}%",
            res["priority"],
            gap,
        )

    console.print(table)

    # Top regions
    console.print("\n[bold]🗺️ Top 5 Marchés Recommandés :[/bold]")
    for reg in assessment["regions"][:5]:
        star = " ⭐" if reg["targeted"] else ""
        console.print(f"  {reg['priority']:12s}  {reg['name']}{star} — {reg['notes']}")

    # Save report
    report = generate_report(assessment, org_name=args.org)
    report_path = "rapport_croissance.md"
    with open(report_path, "w") as f:
        f.write(report)
    console.print(f"\n✅ Rapport complet sauvegardé : {report_path}")


if __name__ == "__main__":
    main()
