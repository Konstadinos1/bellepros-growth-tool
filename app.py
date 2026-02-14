"""
app.py — Console de Croissance Bellepros — Interface Web Streamlit.

Lancer avec :  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import re
import unicodedata
from typing import Dict, Any, List

from questionnaire import QUESTIONS, default_answers
from assessor import run_assessment
from report_generator import generate_report
from pdf_generator import generate_pdf
from config import DIMENSIONS, ALL_DIMENSION_KEYS, QUEBEC_REGIONS, COMPETITORS

# ---------------------------------------------------------------------------
# Config page
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Bellepros — Console de Croissance",
    page_icon="🍟",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3a5f 0%, #c41e3a 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #c41e3a;
    }
</style>
""", unsafe_allow_html=True)


def _safe_download_basename(name: str) -> str:
    normalized = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", normalized.strip().lower()).strip("_")
    return slug or "organisation"


def main():
    st.markdown("""
    <div class="main-header">
        <h1>🍟 Console de Croissance Bellepros</h1>
        <p>Stratégie d'expansion QSR — Province de Québec</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.image("https://img.icons8.com/emoji/96/french-fries-emoji.png", width=80)
    st.sidebar.header("⚙️ Configuration")
    org_name = st.sidebar.text_input("Nom de l'organisation", value="Bellepros")

    st.sidebar.subheader("Dimensions à évaluer")
    selected_dims = []
    for key, info in DIMENSIONS.items():
        if st.sidebar.checkbox(info["short"], value=True, key=f"dim_{key}"):
            selected_dims.append(key)

    use_defaults = st.sidebar.button("🚀 Démo Rapide (Réponses par défaut)")

    # State management
    if use_defaults:
        st.session_state["answers"] = default_answers()
        st.session_state["step"] = "results"

    if "step" not in st.session_state:
        st.session_state["step"] = "questionnaire"
    if "answers" not in st.session_state:
        st.session_state["answers"] = {}

    if st.session_state["step"] == "questionnaire":
        render_questionnaire()
    elif st.session_state["step"] == "results":
        render_results(org_name, selected_dims)


def render_questionnaire():
    st.header("📋 Questionnaire Stratégique")
    st.markdown("Répondez aux questions suivantes pour obtenir votre diagnostic de croissance personnalisé.")

    # Group questions by section
    sections = {
        "🏢 Identité & Vision": ["nb_unites", "objectif_5ans", "regions_cibles"],
        "⚙️ Opérations": ["sop_niveau", "temps_service", "controle_qualite"],
        "💰 Finances & Modèle Franchise": ["ventes_moyennes", "marge_nette", "financement", "modele_franchise"],
        "🎯 Marque & Positionnement": ["notoriete", "reseaux_sociaux", "differenciateur"],
        "🍔 Menu & Produits": ["menu_engineering", "poutine_strategie"],
        "📱 Technologie": ["techno_niveau"],
        "👥 Équipe & Culture": ["roulement", "formation"],
        "🚚 Approvisionnement": ["fournisseurs"],
        "📜 Réglementation QC": ["conformite_qc"],
        "🏆 Concurrence & Auto-évaluation": ["positionnement_prix", "maturite_globale"],
    }

    question_map = {q.qid: q for q in QUESTIONS}
    answers = {}

    with st.form("questionnaire_form"):
        for section_name, qids in sections.items():
            st.subheader(section_name)
            for qid in qids:
                q = question_map.get(qid)
                if not q:
                    continue

                st.markdown(f"**{q.text}**")
                if q.help_text:
                    st.caption(q.help_text)

                if q.answer_type == "multi":
                    options = {opt["label"]: opt["value"] for opt in q.options}
                    selected = st.multiselect(
                        "Sélectionnez tout ce qui s'applique",
                        options=list(options.keys()),
                        key=f"q_{q.qid}",
                    )
                    answers[q.qid] = [options[s] for s in selected]

                elif q.answer_type == "single":
                    options = {opt["label"]: opt["value"] for opt in q.options}
                    choice = st.radio(
                        "Choisissez une option :",
                        options=list(options.keys()),
                        key=f"q_{q.qid}",
                    )
                    answers[q.qid] = options[choice] if choice else None

                elif q.answer_type == "scale":
                    answers[q.qid] = st.slider(
                        "Évaluez de 1 à 5",
                        min_value=1, max_value=5, value=3,
                        key=f"q_{q.qid}",
                    )

                st.divider()

        submitted = st.form_submit_button(
            "🔍 Lancer l'Évaluation",
            type="primary",
            use_container_width=True,
        )
        if submitted:
            st.session_state["answers"] = answers
            st.session_state["step"] = "results"
            st.rerun()


def render_results(org_name: str, selected_dims: List[str]):
    answers = st.session_state.get("answers", {})
    if not answers:
        st.warning("Aucune réponse trouvée. Veuillez remplir le questionnaire.")
        if st.button("← Retour au questionnaire"):
            st.session_state["step"] = "questionnaire"
            st.rerun()
        return

    assessment = run_assessment(answers, selected_dims if selected_dims else None)
    tier = assessment["tier"]
    overall = assessment["overall_score"]
    stars_str = "★" * assessment["stars"] + "☆" * (5 - assessment["stars"])

    # =====================================================================
    # HEADER METRICS
    # =====================================================================
    st.header(f"📊 Diagnostic de Croissance — {org_name}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Score Global", f"{overall:.0f}/100")
    col2.metric("Niveau", tier["label"])
    col3.metric("Étoiles", stars_str)
    col4.metric("Dimensions", len(assessment["dimensions_assessed"]))

    st.info(f"**{tier['label']}** — {tier['desc']}")
    st.divider()

    # =====================================================================
    # TABS
    # =====================================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Vue d'ensemble",
        "🗺️ Carte d'expansion",
        "🏆 Analyse concurrentielle",
        "📋 Feuille de route",
        "📑 Détails par dimension",
    ])

    # --- TAB 1: VUE D'ENSEMBLE ---
    with tab1:
        col_radar, col_bars = st.columns([1, 1])

        with col_radar:
            st.subheader("Radar de Croissance")
            render_radar(assessment)

        with col_bars:
            st.subheader("Scores par Dimension")
            render_dimension_bars(assessment)

        st.divider()
        st.subheader("Matrice des Lacunes")
        render_gap_matrix(assessment)

    # --- TAB 2: CARTE D'EXPANSION ---
    with tab2:
        st.subheader("🗺️ Marchés Prioritaires au Québec")
        render_region_analysis(assessment)

    # --- TAB 3: ANALYSE CONCURRENTIELLE ---
    with tab3:
        st.subheader("🏆 Positionnement vs Concurrents QSR")
        render_competitive(assessment)

    # --- TAB 4: FEUILLE DE ROUTE ---
    with tab4:
        st.subheader("📋 Feuille de Route d'Expansion")
        render_roadmap(assessment)

    # --- TAB 5: DÉTAILS ---
    with tab5:
        st.subheader("📑 Analyse Détaillée par Dimension")
        for dim_key in assessment["dimensions_assessed"]:
            res = assessment["dimension_results"][dim_key]
            color = "🟢" if res["score"] >= 70 else "🟡" if res["score"] >= 50 else "🔴"
            with st.expander(f"{color} {res['name']} — {res['score']:.0f}% ({res['priority']})"):
                if res["gaps"]:
                    st.markdown("**Lacunes :**")
                    for g in res["gaps"]:
                        st.markdown(f"- ⚠️ {g}")
                if res["recommendations"]:
                    st.markdown("**Recommandations :**")
                    for r in res["recommendations"]:
                        st.markdown(f"- 💡 {r}")

    st.divider()

    # Downloads
    report_md = generate_report(assessment, org_name=org_name)

    safe_org = _safe_download_basename(org_name)
    col_pdf, col_md, col_new = st.columns(3)
    with col_pdf:
        with st.spinner("Génération du PDF..."):
            pdf_bytes = bytes(generate_pdf(assessment, org_name=org_name))
        st.download_button(
            "📥 Télécharger le Rapport PDF",
            data=pdf_bytes,
            file_name=f"bellepros_croissance_{safe_org}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary",
        )
    with col_md:
        st.download_button(
            "📄 Télécharger en Markdown",
            data=report_md,
            file_name=f"bellepros_croissance_{safe_org}.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with col_new:
        if st.button("🔄 Nouvelle Évaluation", use_container_width=True):
            st.session_state["step"] = "questionnaire"
            st.session_state["answers"] = {}
            st.rerun()


# =========================================================================
# VISUALIZATION COMPONENTS
# =========================================================================

def render_radar(assessment: Dict[str, Any]):
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
        fillcolor="rgba(196, 30, 58, 0.2)",
        line_color="#c41e3a",
        name="Score",
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=400,
        margin=dict(l=40, r=40, t=20, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_dimension_bars(assessment: Dict[str, Any]):
    data = []
    for dim_key in assessment["dimensions_assessed"]:
        res = assessment["dimension_results"][dim_key]
        color = "#28a745" if res["score"] >= 70 else "#ffc107" if res["score"] >= 50 else "#dc3545"
        data.append({"Dimension": res["short"], "Score": res["score"], "color": color})

    df = pd.DataFrame(data)
    fig = go.Figure(go.Bar(
        x=df["Score"],
        y=df["Dimension"],
        orientation="h",
        marker_color=df["color"],
        text=[f"{s:.0f}%" for s in df["Score"]],
        textposition="outside",
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 105], title="Score (%)"),
        yaxis=dict(autorange="reversed"),
        height=400,
        margin=dict(l=10, r=40, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_gap_matrix(assessment: Dict[str, Any]):
    cols = st.columns(5)
    for i, dim_key in enumerate(assessment["dimensions_assessed"]):
        res = assessment["dimension_results"][dim_key]
        col = cols[i % 5]
        pct = res["score"]
        if pct >= 70:
            col.success(f"**{res['short']}**\n\n{pct:.0f}%")
        elif pct >= 50:
            col.warning(f"**{res['short']}**\n\n{pct:.0f}%")
        else:
            col.error(f"**{res['short']}**\n\n{pct:.0f}%")


def render_region_analysis(assessment: Dict[str, Any]):
    regions = assessment["regions"]

    # Summary table
    df = pd.DataFrame([
        {
            "Région": r["name"],
            "Population": f"{r['population']:,}",
            "Densité QSR": r["densite"],
            "Loyer moy. $/pi²": f"{r['loyer']:.0f}$",
            "Potentiel": r["potentiel"],
            "Priorité": r["priority"],
            "Ciblée": "✅" if r["targeted"] else "",
        }
        for r in regions
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # Bar chart of region scores
    fig = go.Figure(go.Bar(
        x=[r["name"] for r in regions],
        y=[r["score"] for r in regions],
        marker_color=["#c41e3a" if r["targeted"] else "#1e3a5f" for r in regions],
        text=[r["priority"] for r in regions],
        textposition="outside",
    ))
    fig.update_layout(
        title="Score de Priorité par Région",
        yaxis=dict(range=[0, 105], title="Score"),
        xaxis=dict(title=""),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Top 3 recommendations
    st.subheader("🎯 Top 3 Marchés Recommandés")
    for i, reg in enumerate(regions[:3], 1):
        emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        st.markdown(f"""
        {emoji} **{reg['name']}** — {reg['priority']}
        - Population : {reg['population']:,}
        - Densité QSR : {reg['densite']}
        - Loyer moyen : {reg['loyer']:.0f}$/pi²
        - {reg['notes']}
        """)


def render_competitive(assessment: Dict[str, Any]):
    competitors = assessment["competitors"]

    # Bubble chart
    fig = go.Figure()
    for comp in competitors:
        color = "#dc3545" if comp["niveau_menace"] == "Élevé" else "#ffc107" if "Moyen" in comp["niveau_menace"] else "#28a745"
        fig.add_trace(go.Scatter(
            x=[comp["unites_qc"]],
            y=[comp["vulnerabilite"]],
            mode="markers+text",
            marker=dict(size=max(comp["unites_qc"] / 8, 15), color=color, opacity=0.7),
            text=[comp["name"]],
            textposition="top center",
            name=comp["name"],
            hovertemplate=(
                f"<b>{comp['name']}</b><br>"
                f"Unités QC : {comp['unites_qc']}<br>"
                f"Vulnérabilité : {comp['vulnerabilite']}%<br>"
                f"Force : {comp['force']}<br>"
                f"Faiblesse : {comp['faiblesse']}"
            ),
        ))

    fig.update_layout(
        title="Carte Concurrentielle — Taille vs Vulnérabilité",
        xaxis=dict(title="Nombre d'unités au Québec", type="log"),
        yaxis=dict(title="Vulnérabilité aux forces de Bellepros (%)", range=[30, 105]),
        showlegend=False,
        height=450,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Opportunity table
    st.subheader("Opportunités Concurrentielles")
    for comp in competitors:
        if comp["opportunites"]:
            with st.expander(f"{comp['name']} ({comp['niveau_menace']}) — {len(comp['opportunites'])} opportunité(s)"):
                st.markdown(f"**Force :** {comp['force']}")
                st.markdown(f"**Faiblesse :** {comp['faiblesse']}")
                for opp in comp["opportunites"]:
                    st.markdown(f"- 🎯 {opp}")


def render_roadmap(assessment: Dict[str, Any]):
    roadmap = assessment["roadmap"]

    if roadmap["critique"]:
        st.markdown("### 🔴 Actions Immédiates (0-3 mois) — Critique")
        for item in roadmap["critique"]:
            st.checkbox(item, key=f"rm_c_{item[:30]}")

    if roadmap["court_terme"]:
        st.markdown("### 🟠 Court Terme (3-6 mois) — Priorité Élevée")
        for item in roadmap["court_terme"]:
            st.checkbox(item, key=f"rm_ct_{item[:30]}")

    if roadmap["moyen_terme"]:
        st.markdown("### 🟡 Moyen Terme (6-12 mois) — Priorité Moyenne")
        for item in roadmap["moyen_terme"]:
            st.checkbox(item, key=f"rm_mt_{item[:30]}")

    if roadmap["long_terme"]:
        st.markdown("### 🟢 Long Terme (12+ mois) — Amélioration Continue")
        for item in roadmap["long_terme"]:
            st.checkbox(item, key=f"rm_lt_{item[:30]}")

    if not any(roadmap.values()):
        st.success("Aucune lacune majeure identifiée — maintenir les pratiques actuelles!")


if __name__ == "__main__":
    main()
