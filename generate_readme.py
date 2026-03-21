import requests
import os
from datetime import datetime

TOKEN    = os.environ.get('GITHUB_TOKEN')
USERNAME = 'diego-col-un'

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# ── Repos públicos ──
repos_res = requests.get(
    f'https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=updated',
    headers=headers
).json()

repos       = [r for r in repos_res if not r['fork']]
total_repos = len(repos)
total_stars = sum(r['stargazers_count'] for r in repos)

# ── Lenguajes ──
lang_count = {}
for repo in repos:
    lang = repo.get('language')
    if lang:
        lang_count[lang] = lang_count.get(lang, 0) + 1

top_langs = sorted(lang_count.items(), key=lambda x: x[1], reverse=True)[:5]

# ── Commits por año ──
commits_by_year = {}
for year in [2022, 2023, 2024, 2025]:
    res = requests.get(
        f'https://api.github.com/search/commits?q=author:{USERNAME}+author-date:{year}-01-01..{year}-12-31',
        headers={**headers, 'Accept': 'application/vnd.github.cloak-preview'}
    ).json()
    commits_by_year[year] = res.get('total_count', 0)

# ── Barras de progreso ──
def barra(pct, total=20):
    lleno = round(pct / 100 * total)
    return '█' * lleno + '░' * (total - lleno)

# ── Tabla commits ──
max_commits = max(commits_by_year.values()) if commits_by_year else 1
commit_rows = ''
for year, count in commits_by_year.items():
    pct = round(count / max_commits * 100) if max_commits > 0 else 0
    commit_rows += f'| {year} | {count} | `{barra(pct)}` |\n'

# ── Tabla lenguajes ──
lang_rows = ''
max_lang  = top_langs[0][1] if top_langs else 1
for lang, count in top_langs:
    pct = round(count / total_repos * 100)
    lang_rows += f'| {lang} | `{barra(pct)}` | {pct}% |\n'

# ── Repos recientes ──
top_repos = repos[:5]
repo_rows = ''
for r in top_repos:
    desc  = (r['description'] or 'Sin descripción')[:50]
    lang  = r['language'] or 'N/A'
    stars = r['stargazers_count']
    repo_rows += f'| [{r["name"]}]({r["html_url"]}) | {desc} | {lang} | {stars} |\n'

# ── Fecha ──
updated = datetime.utcnow().strftime('%d/%m/%Y %H:%M UTC')

# ── README ──
readme = f"""<div align="center">

![banner](https://capsule-render.vercel.app/api?type=waving&color=534AB7&height=130&section=header&text=Diego%20Fernando%20Aristiz%C3%A1bal&fontSize=30&fontColor=fff&animation=fadeIn&desc=Backend%20Developer%20%7C%20DevOps%20%7C%20UNAL%20Manizales&descSize=14&descAlignY=75)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/diego-fernando-aristizabal/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/{USERNAME})

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-777BB4?style=flat&logo=php&logoColor=white)
![Laravel](https://img.shields.io/badge/Laravel-FF2D20?style=flat&logo=laravel&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)

</div>

---

## Sobre mí

Estudiante de **Administración de Sistemas Informáticos** en la **Universidad Nacional de Colombia · ASI Manizales**.
Apasionado por el desarrollo backend, arquitectura de microservicios y DevOps.
```python
developer = {{
    "name":           "Diego Fernando Aristizábal Gutiérrez",
    "university":     "Universidad Nacional de Colombia · Manizales",
    "program":        "Administración de Sistemas Informáticos",
    "focus":          ["Backend", "DevOps", "Microservicios", "APIs REST"],
    "stack":          ["Python", "PHP", "Laravel", "Flask", "Node.js"],
    "databases":      ["MySQL", "MongoDB", "SQLite", "Firebase"],
    "certifications": ["NDG Linux Unhatched", "NDG Linux Essentials"],
    "linkedin":       "linkedin.com/in/diego-fernando-aristizabal",
}}
```

---

## Lenguajes más usados

| Lenguaje | Uso | % |
|---|---|---|
{lang_rows}
---

## Commits por año

| Año | Commits | Actividad |
|---|---|---|
{commit_rows}
---

## Proyectos recientes

| Repo | Descripción | Lenguaje | Stars |
|---|---|---|---|
{repo_rows}
---

## Certificaciones

| Certificación | Entidad |
|---|---|
| NDG Linux Unhatched | Cisco Networking Academy |
| NDG Linux Essentials | Cisco Networking Academy |

---

<div align="center">

![GitHub Stats](https://github-readme-stats.vercel.app/api?username={USERNAME}&show_icons=true&theme=tokyonight&hide_border=true&count_private=true)

![GitHub Streak](https://streak-stats.demolab.com?user={USERNAME}&theme=tokyonight&hide_border=true)

</div>

---

<div align="center">

[![LinkedIn](https://img.shields.io/badge/Conectemos%20en%20LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/diego-fernando-aristizabal/)

<sub>Actualizado automáticamente el {updated}</sub>

![footer](https://capsule-render.vercel.app/api?type=waving&color=534AB7&height=80&section=footer)

</div>
"""

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

print(f"README generado — {updated}")