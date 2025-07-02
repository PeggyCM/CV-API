import json  # Pour lire et utiliser des fichiers JSON
from rich import print  # Pour afficher du texte avec des couleurs et styles
from rich.console import Console  # Pour créer un objet console personnalisé
from rich.panel import Panel  # Pour encadrer du texte dans un bloc stylisé
from rich.table import Table  # Pour créer et afficher des tableaux jolis

console = Console()  # Crée une console Rich pour afficher du contenu stylé

# Charger les données depuis le fichier JSON
with open('api.json', 'r') as f:  # Ouvre le fichier api.json en mode lecture
    data = json.load(f)  # Charge les données JSON dans un dictionnaire Python

cv = data.get('CV', {})  # Récupère l'objet principal "CV" du JSON, ou {} s'il n'existe pas

# Créer l'en-tête du CV avec nom, titre et localisation
header = f"[bold cyan]{cv.get('Nom', '')} {cv.get('Prenom', '')}[/bold cyan]\n" \
         f"[italic]{cv.get('Titre', '')} - {cv.get('SsTitre', '')}[/italic]\n" \
         f"📍 {cv.get('Ville', '')}"

# Afficher l'en-tête dans un panneau avec un titre
console.print(Panel(header, title="Mon CV", title_align="left"))

# Section des expériences professionnelles
console.print("\n[bold underline]Expériences Professionnelles :[/bold underline]")

# Boucle sur chaque expérience de la liste "Experiences"
for exp in cv.get('Experiences', []):
    # Affiche le poste occupé, la société et la période
    console.print(f"[bold]{exp.get('Emploi')}[/bold] chez [blue]{exp.get('Societe')}[/blue] ({exp.get('Periode')})")
    # Affiche la description de la mission
    console.print(f"  {exp.get('Mission')}\n")

# Section des compétences
console.print("\n[bold underline]Compétences :[/bold underline]")

# Crée un tableau avec des en-têtes pour les compétences
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Type")        # Colonne pour le type de compétence (ex : Technique, Langue)
table.add_column("Compétence")  # Colonne pour le nom ou libellé de la compétence

# Remplit le tableau avec les compétences du JSON
for comp in cv.get('Competences', []):
    table.add_row(comp.get('Type', ''), comp.get('Libelle', ''))  # Ajoute une ligne au tableau

console.print(table)  # Affiche le tableau dans la console

# Section des formations
console.print("\n[bold underline]Formations :[/bold underline]")

# Boucle sur chaque formation dans la liste "Formations"
for form in cv.get('Formations', []):
    # Affiche le nom de la formation et l'année d'obtention
    console.print(f"- [green]{form.get('Intitule')}[/green] (Obtenue en {form.get('dateObtention')})")
