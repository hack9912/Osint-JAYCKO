import streamlit as st
import requests
import hashlib

st.set_page_config(
    page_title="OSIN – Jaycko 🇫🇷",
    page_icon="🕵️",
    layout="wide"
)

st.title("🕵️ OSINT – By JAYCKO-_-")
st.caption("Données publiques uniquement – 100 % légal")

# ================= UTILITAIRES =================
def osint_score(email=False, pseudo_sites=0, adult=False, pdf=False, justice=False):
    score = 0
    if email: score += 15
    if pseudo_sites >= 5: score += 20
    if adult: score += 10
    if pdf: score += 20
    if justice: score += 25

    if score >= 70:
        level = "🔴 ÉLEVÉ"
    elif score >= 40:
        level = "🟠 MOYEN"
    else:
        level = "🟢 FAIBLE"

    return score, level

def generate_report(content):
    report = "\n".join(content)
    st.download_button("📄 Télécharger le rapport OSINT", report, file_name="rapport_osint.txt")

def generate_usernames(base):
    variants = set()
    years = ["1990","1995","2000","2005","2010","2020"]
    symbols = ["_", ".", "-", ""]
    for y in years:
        for s in symbols:
            variants.add(f"{base}{s}{y}")
            variants.add(f"{base}{y}")
    variants.add(base.lower())
    variants.add(base.upper())
    variants.add(base.capitalize())
    variants.add(f"{base}_officiel")
    variants.add(f"real{base}")
    return list(variants)

def fake_profile_score(found_sites, age_unknown=True):
    score = 0
    if found_sites < 3: score += 30
    if age_unknown: score += 20
    if score >= 40:
        return "⚠️ Profil suspect"
    return "✅ Profil crédible"

# ================= MENU =================
module = st.selectbox(
    "Choisis un module",
    [
        "🔑 Email Check",
        "👤 Pseudo MEGA Scan",
        "🌐 IP OSINT",
        "🧑 Nom & Prénom OSINT",
        "⚖️ Justice & Affaires publiques",
        "🖼️ Image OSINT",
        "📂 Documents publics",
        "🏢 Entreprise OSINT",
        "🕰️ Historique Web"
    ]
)

report_data = []

# ================= EMAIL =================
if module == "🔑 Email Check":
    st.subheader("Email OSINT (public)")
    email = st.text_input("Adresse email")
    if st.button("Analyser"):
        if not email:
            st.error("Email requis")
        else:
            md5 = hashlib.md5(email.strip().lower().encode()).hexdigest()
            links = [
                f"https://www.gravatar.com/avatar/{md5}",
                f"https://www.google.com/search?q={email}",
                f"https://github.com/search?q={email}",
                f"https://pastebin.com/search?q={email}"
            ]
            for l in links:
                st.markdown(f"- {l}")
                report_data.append(l)
            score, level = osint_score(email=True)
            st.info(f"Score OSINT email : {score} ({level})")
            generate_report(report_data)

# ================= PSEUDO =================
elif module == "👤 Pseudo MEGA Scan":
    st.subheader("Pseudo MEGA OSINT")
    username = st.text_input("Pseudo")
    if st.button("Scanner"):
        if not username:
            st.error("Pseudo requis")
        else:
            sites = {
                "GitHub": f"https://github.com/{username}",
                "Twitter / X": f"https://twitter.com/{username}",
                "Instagram": f"https://instagram.com/{username}",
                "TikTok": f"https://www.tiktok.com/@{username}",
                "Reddit": f"https://www.reddit.com/user/{username}",
                "Steam": f"https://steamcommunity.com/id/{username}",
                "Pinterest": f"https://www.pinterest.com/{username}",
                # adultes
                "Pornhub": f"https://www.pornhub.com/users/{username}",
                "Xvideos": f"https://www.xvideos.com/profiles/{username}",
                "XNXX": f"https://www.xnxx.com/profile/{username}",
                "OnlyFans": f"https://onlyfans.com/{username}",
                "ManyVids": f"https://www.manyvids.com/Profile/{username}/"
            }
            found_sites = 0
            adult_found = False
            for site, url in sites.items():
                try:
                    r = requests.get(url, timeout=5)
                    if r.status_code == 200:
                        st.success(f"✅ {site}")
                        st.markdown(url)
                        found_sites += 1
                        if site in ["Pornhub","Xvideos","XNXX","OnlyFans","ManyVids"]:
                            adult_found = True
                    else:
                        st.warning(f"❌ {site}")
                except:
                    st.error(f"⚠️ {site} inaccessible")
                report_data.append(f"{site}: {url}")
            score, level = osint_score(pseudo_sites=found_sites, adult=adult_found)
            st.info(f"Score OSINT pseudo : {score} ({level})")
            generate_report(report_data)

# ================= IP =================
elif module == "🌐 IP OSINT":
    st.subheader("IP OSINT")
    ip = st.text_input("Adresse IP")
    if st.button("Analyser IP"):
        if not ip:
            st.error("IP requise")
        else:
            try:
                r = requests.get(f"http://ip-api.com/json/{ip}").json()
                st.json(r)
                report_data.append(str(r))
            except:
                st.error("Erreur de connexion")

# ================= NOM PRENOM =================
elif module == "🧑 Nom & Prénom OSINT":
    st.subheader("Nom & Prénom – OSINT public")
    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")
    ville = st.text_input("Ville (optionnel)")
    metier = st.text_input("Métier (optionnel)")
    if st.button("Rechercher"):
        if not prenom or not nom:
            st.error("Nom et prénom requis")
        else:
            queries = [
                f"{prenom} {nom}",
                f"{nom} {prenom}",
                f"{prenom[0]}. {nom}"
            ]
            if ville: queries.append(f"{prenom} {nom} {ville}")
            if metier: queries.append(f"{prenom} {nom} {metier}")
            platforms = {
                "Google": "https://www.google.com/search?q=",
                "LinkedIn": "https://www.linkedin.com/search/results/all/?keywords=",
                "Facebook": "https://www.facebook.com/search/top/?q=",
                "GitHub": "https://github.com/search?q=",
                "PDF": "https://www.google.com/search?q=filetype:pdf+"
            }
            for q in queries:
                st.markdown(f"### 🔎 {q}")
                for name, base in platforms.items():
                    link = base + q.replace(" ","+")
                    st.markdown(f"- [{name}]({link})")
                    report_data.append(link)
            generate_report(report_data)

# ================= JUSTICE =================
elif module == "⚖️ Justice & Affaires publiques":
    st.subheader("Justice & Affaires publiques (OSINT légal)")
    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")
    ville = st.text_input("Ville (optionnel)")
    if st.button("Rechercher affaires"):
        if not prenom or not nom:
            st.error("Nom et prénom requis")
        else:
            base = f"{prenom} {nom}"
            if ville: base += f" {ville}"
            searches = {
                "Google": f"https://www.google.com/search?q={base}",
                "PDF judiciaires": f"https://www.google.com/search?q=filetype:pdf+{base}",
                "Légifrance": f"https://www.legifrance.gouv.fr/recherche?text={prenom}+{nom}",
                "Presse": f"https://www.google.com/search?q={base}+procès+tribunal"
            }
            for name, url in searches.items():
                st.markdown(f"- [{name}]({url})")
                report_data.append(url)
            generate_report(report_data)

# ================= IMAGE =================
elif module == "🖼️ Image OSINT":
    image = st.file_uploader("Upload une image")
    if image:
        st.image(image)
        st.markdown("- Google Images")
        st.markdown("- Yandex Images")
        st.markdown("- TinEye")
        st.info("EXIF possible si image originale")

# ================= DOCUMENTS =================
elif module == "📂 Documents publics":
    keyword = st.text_input("Nom / Email / Pseudo")
    if st.button("Rechercher documents"):
        urls = [
            f"https://www.google.com/search?q=filetype:pdf+{keyword}",
            f"https://www.google.com/search?q=filetype:doc+{keyword}",
            f"https://www.google.com/search?q=filetype:xls+{keyword}"
        ]
        for u in urls:
            st.markdown(f"- {u}")
            report_data.append(u)
        generate_report(report_data)

# ================= ENTREPRISE =================
elif module == "🏢 Entreprise OSINT":
    name = st.text_input("Nom entreprise")
    if st.button("Rechercher"):
        urls = [
            f"https://www.pappers.fr/recherche?q={name}",
            f"https://www.societe.com/cgi-bin/search?champs={name}",
            f"https://www.google.com/search?q={name}+annonce+légale"
        ]
        for u in urls:
            st.markdown(f"- {u}")
            report_data.append(u)
        generate_report(report_data)

# ================= WAYBACK =================
elif module == "🕰️ Historique Web":
    url = st.text_input("URL ou profil")
    if st.button("Voir historique"):
        st.markdown(f"https://web.archive.org/cite/{url}")
        report_data.append(f"Wayback: {url}")
        generate_report(report_data)

# ================= FOOTER =================
st.markdown("---")
st.caption("Créé par Jaycko 🇫🇷 – OSINT")
