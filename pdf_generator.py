"""
pdf_generator.py — Génère un rapport PDF professionnel pour Bellepros.
"""

import io
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fpdf import FPDF
import plotly.graph_objects as go


def _find_dejavu_font(style: str = "") -> str:
    """Find DejaVu font path across different OS/environments."""
    if style == "B":
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/DejaVuSans-Bold.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",
            "/usr/share/fonts/DejaVuSans.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            return path
    # Fallback: try to find it anywhere
    for root in ["/usr/share/fonts", "/usr/local/share/fonts"]:
        if os.path.isdir(root):
            name = "DejaVuSans-Bold.ttf" if style == "B" else "DejaVuSans.ttf"
            for dirpath, _, filenames in os.walk(root):
                if name in filenames:
                    return os.path.join(dirpath, name)
    return ""


# ---------------------------------------------------------------------------
# Couleurs
# ---------------------------------------------------------------------------
ROUGE = (196, 30, 58)
BLEU_FONCE = (30, 58, 95)
GRIS_CLAIR = (245, 245, 245)
BLANC = (255, 255, 255)
NOIR = (33, 33, 33)
VERT = (40, 167, 69)
JAUNE = (255, 193, 7)
ROUGE_VIF = (220, 53, 69)
ORANGE = (255, 140, 0)


class BelleprosPDF(FPDF):
    def __init__(self, org_name: str = "Bellepros"):
        super().__init__()
        self.org_name = org_name
        self.set_auto_page_break(auto=True, margin=20)
        # DejaVu for full French Unicode support
        regular = _find_dejavu_font("")
        bold = _find_dejavu_font("B")
        if regular and bold:
            self.add_font("DejaVu", "", regular, uni=True)
            self.add_font("DejaVu", "B", bold, uni=True)
            self._font_name = "DejaVu"
        else:
            # Fallback to Helvetica (built-in, limited Unicode)
            self._font_name = "Helvetica"

    def header(self):
        # Red bar at top
        self.set_fill_color(*ROUGE)
        self.rect(0, 0, 210, 8, "F")
        # Blue bar under
        self.set_fill_color(*BLEU_FONCE)
        self.rect(0, 8, 210, 2, "F")
        self.ln(14)

    def footer(self):
        self.set_y(-15)
        self.set_font(self._font_name, "", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 10, f"Console de Croissance Bellepros — {self.org_name} — Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title: str):
        self.set_font(self._font_name, "B", 16)
        self.set_text_color(*BLEU_FONCE)
        self.cell(0, 12, title, ln=True)
        # Red underline
        self.set_draw_color(*ROUGE)
        self.set_line_width(0.8)
        self.line(self.l_margin, self.get_y(), 200, self.get_y())
        self.ln(6)

    def sub_title(self, title: str):
        self.set_font(self._font_name, "B", 12)
        self.set_text_color(*BLEU_FONCE)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def body_text(self, text: str):
        self.set_font(self._font_name, "", 10)
        self.set_text_color(*NOIR)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def bullet(self, text: str, indent: float = 8):
        self.set_font(self._font_name, "", 9)
        self.set_text_color(*NOIR)
        self.cell(indent)
        bullet_x = self.get_x()
        self.cell(4, 5, "•")
        self.multi_cell(0, 5, text)
        self.ln(1)

    def colored_badge(self, text: str, color: tuple):
        self.set_fill_color(*color)
        self.set_text_color(*BLANC)
        self.set_font(self._font_name, "B", 9)
        w = self.get_string_width(text) + 8
        self.cell(w, 7, text, fill=True, align="C")
        self.set_text_color(*NOIR)


def _score_color(score: float) -> tuple:
    if score >= 70:
        return VERT
    elif score >= 50:
        return JAUNE
    return ROUGE_VIF


def _render_radar_png(assessment: Dict[str, Any]) -> bytes:
    """Render radar chart to PNG bytes."""
    names, scores = [], []
    for dim_key in assessment["dimensions_assessed"]:
        res = assessment["dimension_results"][dim_key]
        names.append(res["short"])
        scores.append(res["score"])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],
        theta=names + [names[0]],
        fill="toself",
        fillcolor="rgba(196, 30, 58, 0.25)",
        line_color="#c41e3a",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        width=500, height=400,
        margin=dict(l=60, r=60, t=30, b=30),
        paper_bgcolor="white",
    )
    return fig.to_image(format="png", engine="kaleido")


def _render_bars_png(assessment: Dict[str, Any]) -> bytes:
    """Render horizontal bar chart to PNG bytes."""
    names, scores, colors = [], [], []
    for dim_key in assessment["dimensions_assessed"]:
        res = assessment["dimension_results"][dim_key]
        names.append(res["short"])
        scores.append(res["score"])
        c = _score_color(res["score"])
        colors.append(f"rgb({c[0]},{c[1]},{c[2]})")

    fig = go.Figure(go.Bar(
        x=scores,
        y=names,
        orientation="h",
        marker_color=colors,
        text=[f"{s:.0f}%" for s in scores],
        textposition="outside",
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 105]),
        yaxis=dict(autorange="reversed"),
        width=500, height=400,
        margin=dict(l=120, r=50, t=10, b=30),
        paper_bgcolor="white",
    )
    return fig.to_image(format="png", engine="kaleido")


def _render_regions_png(assessment: Dict[str, Any]) -> bytes:
    """Render region bar chart to PNG bytes."""
    regions = assessment["regions"]
    fig = go.Figure(go.Bar(
        x=[r["name"] for r in regions],
        y=[r["score"] for r in regions],
        marker_color=["#c41e3a" if r["targeted"] else "#1e3a5f" for r in regions],
        text=[r["priority"] for r in regions],
        textposition="outside",
    ))
    fig.update_layout(
        yaxis=dict(range=[0, 105]),
        width=700, height=350,
        margin=dict(l=40, r=20, t=10, b=80),
        paper_bgcolor="white",
        xaxis_tickangle=-35,
    )
    return fig.to_image(format="png", engine="kaleido")


def _render_competitive_png(assessment: Dict[str, Any]) -> bytes:
    """Render competitive bubble chart to PNG bytes."""
    competitors = assessment["competitors"]
    fig = go.Figure()
    for comp in competitors:
        menace = comp["niveau_menace"]
        if menace == "Élevé":
            color = "#dc3545"
        elif "Moyen" in menace:
            color = "#ffc107"
        else:
            color = "#28a745"

        fig.add_trace(go.Scatter(
            x=[comp["unites_qc"]],
            y=[comp["vulnerabilite"]],
            mode="markers+text",
            marker=dict(size=max(comp["unites_qc"] / 8, 15), color=color, opacity=0.7),
            text=[comp["name"]],
            textposition="top center",
            showlegend=False,
        ))

    fig.update_layout(
        xaxis=dict(title="Unités au Québec", type="log"),
        yaxis=dict(title="Vulnérabilité (%)", range=[30, 105]),
        width=700, height=400,
        margin=dict(l=60, r=20, t=20, b=50),
        paper_bgcolor="white",
    )
    return fig.to_image(format="png", engine="kaleido")


def generate_pdf(assessment: Dict[str, Any], org_name: str = "Bellepros") -> bytes:
    """Génère le rapport PDF complet et retourne les bytes."""

    pdf = BelleprosPDF(org_name)
    pdf.alias_nb_pages()
    tier = assessment["tier"]
    overall = assessment["overall_score"]
    stars = "★" * assessment["stars"] + "☆" * (5 - assessment["stars"])

    # =====================================================================
    # PAGE 1 — COUVERTURE
    # =====================================================================
    pdf.add_page()

    # Big cover block
    pdf.ln(30)
    pdf.set_fill_color(*BLEU_FONCE)
    pdf.rect(0, 40, 210, 80, "F")

    pdf.set_y(50)
    pdf.set_font("DejaVu", "B", 28)
    pdf.set_text_color(*BLANC)
    pdf.cell(0, 15, "Console de Croissance", align="C", ln=True)
    pdf.set_font("DejaVu", "B", 22)
    pdf.cell(0, 12, org_name, align="C", ln=True)

    pdf.ln(5)
    pdf.set_font("DejaVu", "", 14)
    pdf.cell(0, 10, "Stratégie d'expansion QSR — Province de Québec", align="C", ln=True)

    pdf.set_y(130)
    pdf.set_text_color(*NOIR)
    pdf.set_font("DejaVu", "B", 18)
    pdf.cell(0, 12, f"Score Global : {overall:.0f}/100   {stars}", align="C", ln=True)
    pdf.ln(3)
    pdf.set_font("DejaVu", "", 14)
    pdf.set_text_color(*ROUGE)
    pdf.cell(0, 10, tier["label"], align="C", ln=True)
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, tier["desc"], align="C", ln=True)

    pdf.ln(15)
    pdf.set_text_color(130, 130, 130)
    pdf.set_font("DejaVu", "", 10)
    pdf.cell(0, 8, f"Rapport généré le {datetime.now().strftime('%d %B %Y à %H:%M')}", align="C", ln=True)
    pdf.cell(0, 8, f"Dimensions évaluées : {len(assessment['dimensions_assessed'])}", align="C", ln=True)

    # =====================================================================
    # PAGE 2 — SOMMAIRE EXÉCUTIF + CHARTS
    # =====================================================================
    pdf.add_page()
    pdf.section_title("Sommaire Exécutif")

    # Score table
    pdf.set_font("DejaVu", "B", 9)
    col_widths = [65, 20, 25, 80]

    # Header row
    pdf.set_fill_color(*BLEU_FONCE)
    pdf.set_text_color(*BLANC)
    pdf.cell(col_widths[0], 8, "Dimension", border=1, fill=True, align="C")
    pdf.cell(col_widths[1], 8, "Score", border=1, fill=True, align="C")
    pdf.cell(col_widths[2], 8, "Priorité", border=1, fill=True, align="C")
    pdf.cell(col_widths[3], 8, "Lacune principale", border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(*NOIR)
    for i, dim_key in enumerate(assessment["dimensions_assessed"]):
        res = assessment["dimension_results"][dim_key]
        gap = res["gaps"][0][:55] + "..." if res["gaps"] and len(res["gaps"][0]) > 55 else (res["gaps"][0] if res["gaps"] else "—")
        bg = GRIS_CLAIR if i % 2 == 0 else BLANC
        pdf.set_fill_color(*bg)
        pdf.cell(col_widths[0], 7, res["name"], border=1, fill=True)
        # Color the score cell
        sc = _score_color(res["score"])
        pdf.set_fill_color(*sc)
        pdf.set_text_color(*BLANC)
        pdf.cell(col_widths[1], 7, f"{res['score']:.0f}%", border=1, fill=True, align="C")
        pdf.set_fill_color(*bg)
        pdf.set_text_color(*NOIR)
        pdf.cell(col_widths[2], 7, res["priority"], border=1, fill=True, align="C")
        pdf.cell(col_widths[3], 7, gap, border=1, fill=True)
        pdf.ln()

    pdf.ln(8)

    # Radar chart
    pdf.sub_title("Radar de Croissance")
    try:
        radar_png = _render_radar_png(assessment)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(radar_png)
            radar_path = f.name
        pdf.image(radar_path, x=30, w=150)
        pdf.ln(5)
    except Exception:
        pdf.body_text("(Graphique radar non disponible)")

    # =====================================================================
    # PAGE 3 — SCORES DÉTAILLÉS + BARS
    # =====================================================================
    pdf.add_page()
    pdf.section_title("Scores par Dimension")

    try:
        bars_png = _render_bars_png(assessment)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(bars_png)
            bars_path = f.name
        pdf.image(bars_path, x=30, w=150)
        pdf.ln(8)
    except Exception:
        pdf.body_text("(Graphique barres non disponible)")

    # Detailed findings per dimension
    for dim_key in assessment["dimensions_assessed"]:
        res = assessment["dimension_results"][dim_key]

        # Check if we need a new page (leave room for content)
        if pdf.get_y() > 230:
            pdf.add_page()

        pdf.sub_title(f"{res['name']} — {res['score']:.0f}% ({res['priority']})")

        if res["gaps"]:
            pdf.set_font("DejaVu", "B", 9)
            pdf.cell(0, 6, "Lacunes :", ln=True)
            for g in res["gaps"]:
                pdf.bullet(g)
        if res["recommendations"]:
            pdf.set_font("DejaVu", "B", 9)
            pdf.cell(0, 6, "Recommandations :", ln=True)
            for r in res["recommendations"]:
                pdf.bullet(r)
        pdf.ln(4)

    # =====================================================================
    # PAGE — ANALYSE RÉGIONALE
    # =====================================================================
    pdf.add_page()
    pdf.section_title("Analyse Régionale — Marchés Prioritaires")

    regions = assessment["regions"]

    # Region table
    pdf.set_font("DejaVu", "B", 8)
    rcols = [45, 22, 25, 22, 25, 25, 12]
    pdf.set_fill_color(*BLEU_FONCE)
    pdf.set_text_color(*BLANC)
    for header, w in zip(["Région", "Population", "Densité QSR", "Loyer $/pi²", "Potentiel", "Priorité", "Cible"], rcols):
        pdf.cell(w, 7, header, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("DejaVu", "", 7)
    pdf.set_text_color(*NOIR)
    for i, reg in enumerate(regions):
        bg = GRIS_CLAIR if i % 2 == 0 else BLANC
        pdf.set_fill_color(*bg)
        pdf.cell(rcols[0], 6, reg["name"], border=1, fill=True)
        pdf.cell(rcols[1], 6, f"{reg['population']:,}", border=1, fill=True, align="R")
        pdf.cell(rcols[2], 6, reg["densite"], border=1, fill=True, align="C")
        pdf.cell(rcols[3], 6, f"{reg['loyer']:.0f}$", border=1, fill=True, align="C")
        pdf.cell(rcols[4], 6, reg["potentiel"], border=1, fill=True, align="C")

        # Color the priority cell
        prio = reg["priority"]
        if prio == "Prioritaire":
            pdf.set_fill_color(*VERT)
            pdf.set_text_color(*BLANC)
        elif prio == "Recommandée":
            pdf.set_fill_color(*JAUNE)
            pdf.set_text_color(*NOIR)
        elif prio == "Secondaire":
            pdf.set_fill_color(*ORANGE)
            pdf.set_text_color(*BLANC)
        else:
            pdf.set_fill_color(180, 180, 180)
            pdf.set_text_color(*BLANC)
        pdf.cell(rcols[5], 6, prio, border=1, fill=True, align="C")

        pdf.set_fill_color(*bg)
        pdf.set_text_color(*NOIR)
        pdf.cell(rcols[6], 6, "✓" if reg["targeted"] else "", border=1, fill=True, align="C")
        pdf.ln()

    pdf.ln(8)

    # Region chart
    try:
        reg_png = _render_regions_png(assessment)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(reg_png)
            reg_path = f.name
        pdf.image(reg_path, x=15, w=180)
        pdf.ln(8)
    except Exception:
        pass

    # Top 3 text
    pdf.sub_title("Top 3 Marchés Recommandés")
    medals = ["#1", "#2", "#3"]
    for i, reg in enumerate(regions[:3]):
        medal = medals[i]
        pdf.set_font("DejaVu", "B", 10)
        pdf.cell(0, 7, f"{medal} {reg['name']} — {reg['priority']}", ln=True)
        pdf.set_font("DejaVu", "", 9)
        pdf.cell(10)
        pdf.cell(0, 6, f"Population : {reg['population']:,} | Densité QSR : {reg['densite']} | Loyer : {reg['loyer']:.0f}$/pi²", ln=True)
        pdf.cell(10)
        pdf.cell(0, 6, reg["notes"], ln=True)
        pdf.ln(3)

    # =====================================================================
    # PAGE — ANALYSE CONCURRENTIELLE
    # =====================================================================
    pdf.add_page()
    pdf.section_title("Analyse Concurrentielle")

    # Competitive chart
    try:
        comp_png = _render_competitive_png(assessment)
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(comp_png)
            comp_path = f.name
        pdf.image(comp_path, x=15, w=180)
        pdf.ln(8)
    except Exception:
        pass

    # Competitor table
    pdf.set_font("DejaVu", "B", 8)
    ccols = [30, 18, 22, 50, 50]
    pdf.set_fill_color(*BLEU_FONCE)
    pdf.set_text_color(*BLANC)
    for header, w in zip(["Concurrent", "Unités", "Menace", "Force", "Faiblesse"], ccols):
        pdf.cell(w, 7, header, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("DejaVu", "", 7)
    pdf.set_text_color(*NOIR)
    for i, comp in enumerate(assessment["competitors"]):
        bg = GRIS_CLAIR if i % 2 == 0 else BLANC
        pdf.set_fill_color(*bg)
        pdf.cell(ccols[0], 6, comp["name"], border=1, fill=True)
        pdf.cell(ccols[1], 6, str(comp["unites_qc"]), border=1, fill=True, align="C")

        menace = comp["niveau_menace"]
        if menace == "Élevé":
            pdf.set_fill_color(*ROUGE_VIF)
            pdf.set_text_color(*BLANC)
        elif "Moyen" in menace:
            pdf.set_fill_color(*JAUNE)
            pdf.set_text_color(*NOIR)
        else:
            pdf.set_fill_color(*VERT)
            pdf.set_text_color(*BLANC)
        pdf.cell(ccols[2], 6, menace, border=1, fill=True, align="C")

        pdf.set_fill_color(*bg)
        pdf.set_text_color(*NOIR)
        force = comp["force"][:35] + "..." if len(comp["force"]) > 35 else comp["force"]
        faiblesse = comp["faiblesse"][:35] + "..." if len(comp["faiblesse"]) > 35 else comp["faiblesse"]
        pdf.cell(ccols[3], 6, force, border=1, fill=True)
        pdf.cell(ccols[4], 6, faiblesse, border=1, fill=True)
        pdf.ln()

    pdf.ln(6)

    # Opportunities
    pdf.sub_title("Opportunités Identifiées")
    for comp in assessment["competitors"]:
        if comp["opportunites"]:
            pdf.set_font("DejaVu", "B", 9)
            pdf.cell(0, 6, f"{comp['name']} :", ln=True)
            for opp in comp["opportunites"]:
                pdf.bullet(opp)
            pdf.ln(2)

    # =====================================================================
    # PAGE — FEUILLE DE ROUTE
    # =====================================================================
    pdf.add_page()
    pdf.section_title("Feuille de Route d'Expansion")

    roadmap = assessment["roadmap"]
    sections = [
        ("Actions Immédiates (0-3 mois) — Critique", roadmap["critique"], ROUGE_VIF),
        ("Court Terme (3-6 mois) — Priorité Élevée", roadmap["court_terme"], ORANGE),
        ("Moyen Terme (6-12 mois) — Priorité Moyenne", roadmap["moyen_terme"], JAUNE),
        ("Long Terme (12+ mois) — Amélioration Continue", roadmap["long_terme"], VERT),
    ]

    for title, items, color in sections:
        if not items:
            continue

        if pdf.get_y() > 240:
            pdf.add_page()

        # Section header with colored bar
        pdf.set_fill_color(*color)
        pdf.rect(pdf.l_margin, pdf.get_y(), 3, 8, "F")
        pdf.cell(6)
        pdf.set_font("DejaVu", "B", 11)
        pdf.set_text_color(*BLEU_FONCE)
        pdf.cell(0, 8, title, ln=True)
        pdf.ln(2)

        pdf.set_font("DejaVu", "", 9)
        pdf.set_text_color(*NOIR)
        for item in items:
            if pdf.get_y() > 270:
                pdf.add_page()
            pdf.bullet(item)

        pdf.ln(5)

    # Footer timestamp
    pdf.ln(10)
    pdf.set_font("DejaVu", "", 8)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, f"Rapport généré par la Console de Croissance Bellepros — {datetime.now().strftime('%Y-%m-%d %H:%M')}", align="C")

    return pdf.output()
