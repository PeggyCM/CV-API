import json  # Pour lire et manipuler des fichiers JSON
from reportlab.lib.pagesizes import letter  # Pour définir la taille de la page (format lettre)
from reportlab.pdfgen import canvas  # Pour générer un document PDF
from reportlab.lib import colors  # Pour utiliser des couleurs dans le PDF
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.units import inch

# Charger les données depuis le fichier JSON "api.json"
with open('api.json', 'r') as f:  # Ouvre le fichier en mode lecture
    data = json.load(f)  # Convertit le contenu JSON en dictionnaire Python

styles = getSampleStyleSheet()
styleN = styles['Normal']

# Récupérer la section "CV" du fichier JSON (ou un dictionnaire vide par défaut)
cv = data.get('CV', {})

# Définir le nom du fichier PDF à générer
pdf_filename = "cv_design.pdf"

# Créer une nouvelle page PDF avec le format "letter"
c = canvas.Canvas(pdf_filename, pagesize=letter)
width, height = letter

# -------- En-tête du CV --------
# Créer un style centré à partir du style Normal (méthode n°1)
style_centre_nom = ParagraphStyle(
    name='Center',
    parent=styles['Normal'],
    alignment=TA_CENTER,  # Centre le texte
    fontName="Helvetica-Bold",  # Choisir une police en gras
    fontSize=20,  # Taille du texte
    textColor=colors.blue  # Couleur du texte : bleu
)
nomComplet = (f"{cv.get('Prenom', '')} {cv.get('Nom', '')}")
x = 72  # Marge gauche (1 inch)
y = height - 36  # Marge du haut (1 inch)
largeur_max = width - 2 * 72  # Largeur de la page - marges

# Créer le paragraphe avec le texte
para = Paragraph(nomComplet, style_centre_nom)

# Wrap et dessin du paragraphe
para.wrap(largeur_max, height)
para.drawOn(c, x, y)

# Se placer pour le titre (centrage méthode n°2)
x = 72
y -= 50

titre = f"{cv.get('Titre', '')}"
sstitre = f"{cv.get('SsTitre', '')}"

# Choisir la police et la taille
c.setFillColor(colors.black)  # Texte en noir
font = "Helvetica-Bold"
font_size = 18

# Calculer la largeur du texte
titre_width = c.stringWidth(titre, font, font_size)
sstitre_width = c.stringWidth(sstitre, font, font_size)

# Positionner le texte de manière centrée
x = (letter[0] - titre_width) / 2  # letter[0] donne la largeur de la page (612 points)

# Mettre en gras et écrire le texte
c.setFont(font, font_size)
c.drawString(x, y, titre)
y -= 25
x = (letter[0] - sstitre_width) / 2  # letter[0] donne la largeur de la page (612 points)
c.drawString(x, y, sstitre)
c.setFont("Helvetica", 12)  # Revenir à une police normale, taille 12

y -= 25
x = 72

c.drawString(x, y, f"📍 {cv.get('Ville', '')}")  # Affiche la ville avec un emoji localisation
y -= 30  # Laisser un espace avant la section suivante

# -------- Section : Expériences Professionnelles --------
c.setFont("Helvetica-Bold", 14)  # Titre de section en gras, taille 14
c.setFillColor(colors.blueviolet)
c.drawString(x, y, "Expériences Professionnelles :")  # Titre de la section
y -= 15  # Espace après le titre

c.setFont("Helvetica", 12)  # Texte normal pour le contenu

# Parcourir toutes les expériences listées dans le JSON
for exp in cv.get('Experiences', []):
    c.setFillColor(colors.black)  # Texte en noir
    # Affiche le poste, la société et la période

    c.drawString(x, y, f"{exp.get('Emploi', '')} chez {exp.get('Societe', '')} ({exp.get('Periode', '')})")
    y -= 5  # Aller à la ligne suivante
    # Affiche la mission de l'expérience avec indentation
    texteMission = f"- {exp.get('Mission', '')}"
    # Créer un paragraphe avec le style normal
    para = Paragraph(texteMission, styleN)
    # Fixer la position (x,y) et la largeur max
    
    largeur_max = width - 2*inch
    # Calculer la largeur utilisée et la hauteur du paragraphe
    largeur_utilisee, hauteur_paragraphe = para.wrap(largeur_max, height)  # Définit la largeur et la hauteur max
    
    # Calculer le nombre de lignes utilisées
    nb_lignes = int(hauteur_paragraphe / 12)  # Chaque ligne a une hauteur de 12 points (taille de la police)
    
    # Positionner y au début du paragraphe (haut du texte)
    y -= 12 * nb_lignes  # Décaler 'y' pour placer le haut du paragraphe

    # Dessiner le paragraphe avec sa position (x, y)
    para.drawOn(c, x, y)
    # Ajuster la position 'y' après avoir dessiné le paragraphe (mettre un petit espace)
    y -= hauteur_paragraphe  # Laisser un peu d'espace avant la prochaine expérience
     

# -------- Section : Compétences (avec tableau coloré) --------
from reportlab.platypus import Table, TableStyle

y -= 10
c.setFont("Helvetica-Bold", 14)
c.setFillColor(colors.blueviolet)
c.drawString(x, y, "Compétences :")
y -= 10

# Préparer les données du tableau
data_table = [["Type", "Libellé"]]  # En-têtes
for comp in cv.get('Competences', []):
    data_table.append([comp.get("Type", ""), comp.get("Libelle", "")])

# Créer le tableau
table = Table(data_table, colWidths=[2.5 * inch, 3.5 * inch])

# Appliquer un style au tableau
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#3498db")),  # En-tête bleu
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Texte blanc en-tête
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
]))

# Dessiner le tableau à la position (x, y)
table.wrapOn(c, width, height)
table.drawOn(c, x, y - table._height)

# Ajuster 'y' après le tableau
y -= table._height + 20


# -------- Section : Formations --------
y -= 15
c.setFont("Helvetica-Bold", 14)  # Titre de section en gras
c.setFillColor(colors.blueviolet)  # Couleur du titre : vert
c.drawString(x, y, "Formations :")  # Titre de la section
y -= 15  # Espace après le titre

c.setFont("Helvetica", 12)  # Texte normal pour les formations

# Parcourir toutes les formations listées
for form in cv.get('Formations', []):
    c.setFillColor(colors.black)  # Texte en noir
    # Affiche l’intitulé de la formation et l’année d’obtention
    c.drawString(x, y, f"{form.get('Intitule', '')} (Obtenue en {form.get('dateObtention', '')})")
    y -= 15  # Aller à la ligne suivante

# -------- Finalisation --------
c.save()  # Enregistre et ferme le fichier PDF

# Message de confirmation dans la console
print(f"Le PDF a été généré avec succès : {pdf_filename}")
