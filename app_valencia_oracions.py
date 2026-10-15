import random
import unicodedata

import streamlit as st

st.set_page_config(page_title="Repàs de Valencià", page_icon="🦄", layout="centered")

st.markdown(
    """
<style>
.stApp {background: linear-gradient(180deg,#fff0f7 0%,#f3eaff 100%);}
h1,h2,h3 {color:#c2185b;}
.caixa {background:#ffffffcc;border:2px dashed #f48fb1;border-radius:16px;
        padding:14px 18px;margin:10px 0;font-size:1.15rem;}
.estrelles {font-size:1.3rem;font-weight:700;color:#8e24aa;}
div.stButton > button {background:#ec407a;color:white;border-radius:20px;
        font-weight:700;border:none;padding:.4rem 1.2rem;}
</style>
""",
    unsafe_allow_html=True,
)

st.session_state.setdefault("fet", set())


def clau(paraula):
    """Clau d'ordenació: sense accents ni ç."""
    n = unicodedata.normalize("NFD", paraula.lower())
    return "".join(c for c in n if unicodedata.category(c) != "Mn")


def punts(k):
    if k not in st.session_state["fet"]:
        st.session_state["fet"].add(k)
        st.balloons()


def ordena(key, correcta):
    mix_key = f"mix_{key}"
    if mix_key not in st.session_state:
        mix = correcta[:]
        r = random.Random(key)
        for _ in range(30):
            r.shuffle(mix)
            if mix != correcta:
                break
        st.session_state[mix_key] = mix
    mix = st.session_state[mix_key]
    st.markdown(
        '<div class="caixa">' + " &nbsp;·&nbsp; ".join(f"<b>{w}</b>" for w in mix) + "</div>",
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    tri = []
    for i in range(len(mix)):
        with cols[i % 3]:
            tri.append(st.selectbox(f"Lloc {i + 1}", ["—"] + mix, key=f"{key}_{i}"))
    if st.button("Comprova ✅", key=f"b_{key}"):
        if "—" in tri:
            st.warning("Omple tots els llocs primer 🧚")
        elif tri == correcta:
            st.success("Molt bé! Ho has ordenat perfecte! 🦄✨")
            punts(key)
        else:
            marques = ["✅" if a == b else "❌" for a, b in zip(tri, correcta)]
            st.error("Quasi! Mira quins llocs estan bé: " + " ".join(marques))
    with st.expander("🔍 Mostra la solució"):
        st.write(" → ".join(correcta))


def pregunta(key, text, opcions, correcta, explica=""):
    r = st.radio(text, opcions, index=None, key=f"r_{key}")
    if r is not None:
        if r == correcta:
            st.success(f"Correcte! 🦄 {explica}")
            punts(key)
        else:
            st.error("Ups! Torna-ho a provar 🧚")


# ---------------------------------------------------------------- Capçalera
st.title("🦄 Repàs de Valencià 🧚")
st.caption("Oracions i ordre alfabètic · 3r de Primària · Proba de divendres 16 d'octubre")
st.markdown(
    f'<div class="estrelles">⭐ Estrelles guanyades: {len(st.session_state["fet"])}</div>',
    unsafe_allow_html=True,
)

PARTS = [
    "📖 1. Recorda: què és una oració?",
    "🧩 2. Completa la definició",
    "🌀 3. Desenreda les oracions",
    "🏞️ 4. Construeix oracions (xiquets i ecologistes)",
    "✅ 5. És una oració o no?",
    "🔤 6. Ordena alfabèticament",
    "📚 7. Llistes de paraules",
    "🌉 8. Quina accepció?",
    "✏️ 9. Escriu les teues oracions",
]
part = st.selectbox("Tria una part:", PARTS)
st.divider()

# ---------------------------------------------------------------- 1
if part == PARTS[0]:
    st.header("Què és una oració?")
    st.markdown(
        """
<div class="caixa">
Una <b>oració</b> és un <b>conjunt</b> de <b>paraules</b> ordenades que
comuniquen un <b>missatge</b> amb sentit <b>complet</b>.
</div>
<div class="caixa">
✏️ Comença amb <b>lletra majúscula</b><br>
🔚 Acaba amb un <b>punt</b> (.)<br>
💡 Les paraules estan <b>ordenades</b> i tenen <b>sentit</b><br>
🏃 Sol tindre un <b>verb</b>: diu què fa algú (tira, aguanta, netegen...)
</div>
<div class="caixa">
<b>Exemple:</b> «La xiqueta aguanta la bossa.»<br>
<b>Qui?</b> La xiqueta · <b>Què fa?</b> aguanta · <b>Què?</b> la bossa
</div>
<div class="caixa">
🔤 <b>Ordre alfabètic:</b> a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z<br>
Si la primera lletra és igual, mira la <b>segona</b>. Si també és igual, mira la <b>tercera</b>...<br>
Una paraula <b>més curta</b> va abans: <i>cama</i> → <i>camí</i> → <i>caminar</i>.
</div>
""",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------- 2
elif part == PARTS[1]:
    st.header("Completa la definició")
    st.write("Tria la paraula correcta en cada buit:")
    opcions = ["—", "missatge", "paraules", "conjunt", "complet"]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        a = st.selectbox("Buit 1", opcions, key="d1")
    with c2:
        b = st.selectbox("Buit 2", opcions, key="d2")
    with c3:
        c = st.selectbox("Buit 3", opcions, key="d3")
    with c4:
        d = st.selectbox("Buit 4", opcions, key="d4")
    st.markdown(
        f'<div class="caixa">Una oració és un <b>{a}</b> de <b>{b}</b> ordenades '
        f"que comuniquen un <b>{c}</b> amb sentit <b>{d}</b>.</div>",
        unsafe_allow_html=True,
    )
    if st.button("Comprova ✅", key="b_def"):
        if (a, b, c, d) == ("conjunt", "paraules", "missatge", "complet"):
            st.success("Perfecte! Te la saps! 🦄")
            punts("def")
        else:
            st.error("Encara no... Pensa: un ___ de ___ ordenades que comuniquen un ___ amb sentit ___ 🧚")

# ---------------------------------------------------------------- 3
elif part == PARTS[2]:
    st.header("Desenreda les oracions")
    st.write("Ordena les paraules per a formar una oració amb sentit.")
    st.subheader("Oració 1")
    ordena("des1", ["Cuidar", "el", "medi", "ambient", "és", "cosa", "de", "tots"])
    st.subheader("Oració 2")
    ordena("des2", ["Cada", "gota", "compta"])
    st.subheader("Oració 3")
    ordena("des3", ["La", "xiqueta", "arreplega", "el", "fem", "al", "parc"])
    st.subheader("Oració 4")
    ordena("des4", ["Els", "xiquets", "netegen", "el", "parc"])

# ---------------------------------------------------------------- 4
elif part == PARTS[3]:
    st.header("Construeix oracions")
    st.write("Tria una paraula de cada quadre per a fer una oració que tinga sentit.")
    c1, c2, c3 = st.columns(3)
    with c1:
        s = st.selectbox("🟩 Qui?", ["—", "El xiquet", "Tots", "La xiqueta", "Els de 3r"], key="q_s")
    with c2:
        v = st.selectbox("🟪 Què fa?", ["—", "tira", "aguanta", "som", "netegen"], key="q_v")
    with c3:
        cmp_ = st.selectbox("🟦 Què?", ["—", "ecologistes", "el parc", "la bossa", "el fem"], key="q_c")

    if "—" not in (s, v, cmp_):
        frase = f"{s} {v} {cmp_}."
        st.markdown(f'<div class="caixa">{frase}</div>', unsafe_allow_html=True)
        singular = s in ("El xiquet", "La xiqueta")
        valid = (
            (singular and v == "tira" and cmp_ in ("el fem", "la bossa"))
            or (singular and v == "aguanta" and cmp_ == "la bossa")
            or (s in ("Els de 3r", "Tots") and v == "netegen" and cmp_ == "el parc")
            or (s == "Tots" and v == "som" and cmp_ == "ecologistes")
        )
        if valid:
            st.success("Té sentit! Bona oració! 🦄")
            punts(f"q_{frase}")
        else:
            st.error("Aquesta oració no té sentit o les paraules no lliguen bé. Prova una altra combinació 🧚")

    st.divider()
    pregunta(
        "mig",
        "Què són les paraules del quadre del mig (tira, aguanta, som, netegen)?",
        ["Noms", "Verbs", "Adjectius"],
        "Verbs",
        "Els verbs diuen què fa algú o què passa.",
    )

# ---------------------------------------------------------------- 5
elif part == PARTS[4]:
    st.header("És una oració o no?")
    frases = [
        ("oc1", "La xiqueta llig un llibre.", "Sí, és una oració", "Té sentit complet."),
        ("oc2", "Els peixos de colors", "No és una oració", "Falta dir què fan els peixos."),
        ("oc3", "gat el corre jardí", "No és una oració", "Les paraules estan desordenades."),
        ("oc4", "Hui plou molt.", "Sí, és una oració", "Comunica un missatge complet."),
    ]
    for k, f, resp, exp in frases:
        st.markdown(f'<div class="caixa">{f}</div>', unsafe_allow_html=True)
        pregunta(k, "Què és?", ["Sí, és una oració", "No és una oració"], resp, exp)

# ---------------------------------------------------------------- 6
elif part == PARTS[5]:
    st.header("Ordena alfabèticament")
    st.write("Ordena aquestes paraules de l'**A** a la **Z**.")
    mots = ["aigua", "oceà", "ocell", "aire", "mar", "tortuga", "oratge", "ona", "gavina"]
    ordena("alf1", sorted(mots, key=clau))
    st.info("💡 Compte amb *oceà* i *ocell*: les tres primeres lletres són iguals. Mira la quarta!")

# ---------------------------------------------------------------- 7
elif part == PARTS[6]:
    st.header("Llistes de paraules")
    st.write("Ordena cada llista alfabèticament. Una paraula no estava al seu lloc!")
    llistes = [
        ("ll1", ["camí", "camió", "caminar", "cama", "cançó"]),
        ("ll2", ["panxa", "peix", "pernil", "pessic", "però"]),
        ("ll3", ["mapa", "massa", "melic", "mussol", "música"]),
        ("ll4", ["gat", "ganivet", "gel", "gelat", "gos"]),
    ]
    for i, (k, l) in enumerate(llistes, 1):
        st.subheader(f"Llista {i}")
        ordena(k, sorted(l, key=clau))

# ---------------------------------------------------------------- 8
elif part == PARTS[7]:
    st.header("Quina accepció?")
    st.write("Algunes paraules tenen **més d'un significat** (accepcions). Mira el diccionari!")
    st.markdown("### 🌉 Pont")
    st.write("Pensa en un pont de pedra sobre un riu.")
    pregunta(
        "pont",
        "Quina accepció correspon al pont de la foto?",
        [
            "1. Dia o dies entre setmana que se solen considerar festius pel fet de trobar-se entre dues festes.",
            "2. Construcció d'obra, de ferro, de fusta o d'un altre material que fa de via de comunicació.",
        ],
        "2. Construcció d'obra, de ferro, de fusta o d'un altre material que fa de via de comunicació.",
        "És una construcció per a creuar el riu.",
    )
    st.markdown("### ⛵ Navegar")
    st.write("Pensa en un veler sobre l'aigua.")
    pregunta(
        "navegar",
        "Quina accepció correspon a la foto del veler?",
        [
            "1. Desplaçar-se amb una embarcació per l'aigua, especialment per la mar.",
            "2. Moure's pels diversos serveis, recursos o conjunts d'informació d'un sistema informàtic.",
        ],
        "1. Desplaçar-se amb una embarcació per l'aigua, especialment per la mar.",
        "El veler navega per l'aigua.",
    )
    st.markdown("### 🖱️ Per a pensar")
    pregunta(
        "navinternet",
        "«Mon pare navega per Internet.» Quina accepció de *navegar* és?",
        ["Desplaçar-se amb una embarcació", "Moure's per un sistema informàtic"],
        "Moure's per un sistema informàtic",
        "Navegar per Internet és moure's per un sistema informàtic.",
    )

# ---------------------------------------------------------------- 9
else:
    st.header("Escriu les teues oracions")
    st.write(
        "Fer un bon ús de l'aigua no és l'única cosa que podem fer per a cuidar el nostre planeta. "
        "Escriu oracions amb altres idees i compara-les amb les del company o la companya."
    )
    st.markdown(
        """
<div class="caixa">
✅ Majúscula al principi<br>✅ Punt al final<br>✅ Té verb<br>✅ Té sentit complet
</div>
""",
        unsafe_allow_html=True,
    )
    text = st.text_area("Escriu ací les teues oracions (una per línia):", height=150)
    if st.button("Revisa ✨", key="rev"):
        linies = [l.strip() for l in text.splitlines() if l.strip()]
        if not linies:
            st.warning("Escriu alguna oració primer 🧚")
        for l in linies:
            avisos = []
            if not l[0].isupper():
                avisos.append("comença amb majúscula")
            if l[-1] not in ".!?":
                avisos.append("acaba amb un punt")
            if len(l.split()) < 3:
                avisos.append("fes-la una mica més llarga, amb sentit complet")
            if avisos:
                st.warning(f"«{l}» → Recorda: " + ", ".join(avisos) + ".")
            else:
                st.success(f"«{l}» → Molt bé! 🦄")
                punts(f"os_{l}")
    st.caption("Idees: tancar l'aixeta, reciclar, no tirar fem a terra, plantar arbres, apagar la llum...")

st.divider()
st.caption("🦄 Molta sort a la proba, Carla! 🧚")
