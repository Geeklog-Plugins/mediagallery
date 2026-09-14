from pathlib import Path
import re

english = Path('language/english_utf-8.php').read_text(encoding='utf-8')
french_path = Path('language/french_france_utf-8.php')
french = french_path.read_text(encoding='utf-8').rstrip() + '\n\n'

m = re.search(r"\$LANG_MG04\s*=\s*array\s*\((.*?)\n\);", english, re.S)
if not m:
    raise SystemExit('LANG_MG04 not found')

entries = []
for line in m.group(1).splitlines():
    mm = re.match(r"\s*'([^']+)'\s*=>\s*'((?:\\'|[^'])*)'", line)
    if mm:
        entries.append((mm.group(1), mm.group(2).replace("\\'", "'")))

exact = {
    'Photo Properties':'Propriétés de la photo','Aperture Value':'Ouverture','Shutter Speed Value':'Vitesse d’obturation',
    'Focal Length':'Distance focale','Artist':'Artiste','Battery Level':'Niveau de batterie','Bits Per Sample':'Bits par échantillon',
    'Blur Warning':'Avertissement de flou','Brightness':'Luminosité','Camera ID':'ID de l’appareil','Camera Serial Number':'Numéro de série de l’appareil',
    'Color':'Couleur','Color Mode':'Mode couleur','Color Space':'Espace colorimétrique','Component Configuration':'Configuration des composantes',
    'Compressed Bits Per Pixel':'Bits compressés par pixel','Compression':'Compression','Contrast':'Contraste','Copyright':'Droits d’auteur',
    'Custom Functions':'Fonctions personnalisées','Date/Time':'Date/heure','Digital Zoom':'Zoom numérique','Digital Zoom Ratio':'Rapport de zoom numérique',
    'Exposure Bias':'Correction d’exposition','Exposure Index':'Indice d’exposition','Exposure Mode':'Mode d’exposition','Exposure Program':'Programme d’exposition',
    'File Source':'Source du fichier','Firmware Version':'Version du micrologiciel','Flash Bias':'Correction du flash','Flash Details':'Détails du flash',
    'Flash Energy':'Énergie du flash','Flash Mode':'Mode flash','Flash Setting':'Réglage du flash','Flash Strength':'Puissance du flash',
    'Focal Plane Resolution Unit':'Unité de résolution du plan focal','Focal Plane X Resolution':'Résolution X du plan focal',
    'Focal Plane Y Resolution':'Résolution Y du plan focal','Focal Units':'Unités de focale','Focus':'Mise au point','Focus Mode':'Mode de mise au point',
    'Focus Warning':'Avertissement de mise au point','Gain Control':'Contrôle du gain','Image Adjustment':'Réglage de l’image',
    'Image Description':'Description de l’image','Image History':'Historique de l’image','Image Length':'Hauteur de l’image',
    'Image Number':'Numéro de l’image','Image Sharpening':'Netteté de l’image','Image Size':'Taille de l’image','Image Type':'Type d’image',
    'Image Width':'Largeur de l’image','Interlace':'Entrelacement','Interoperability Index':'Indice d’interopérabilité',
    'Interoperability Version':'Version d’interopérabilité','Related Image File Format':'Format du fichier image associé',
    'Related Image Length':'Hauteur de l’image associée','Related Image Width':'Largeur de l’image associée','JPEG Tables':'Tables JPEG',
    'JPeg IF Byte Count':'Nombre d’octets JPEG IF','JPeg IF Offset':'Décalage JPEG IF','JPeg Quality':'Qualité JPEG',
    'Light Source':'Source lumineuse','Long Focal Length':'Distance focale longue','Macro':'Macro','Make':'Fabricant',
    'Manual Focus Distance':'Distance de mise au point manuelle','Max Aperture Value':'Ouverture maximale','Metering Mode':'Mode de mesure',
    'Model':'Modèle','Noise':'Bruit','Noise Reduction':'Réduction du bruit','Orientation':'Orientation','Owner Name':'Nom du propriétaire',
    'Photometric Interpretation':'Interprétation photométrique','Photoshop Settings':'Paramètres Photoshop','Picture Info':'Informations sur l’image',
    'Picture Mode':'Mode image','Planar Configuration':'Configuration planaire','Predictor':'Prédicteur','Primary Chromaticities':'Chromaticités primaires',
    'Quality':'Qualité','Reference Black/White':'Référence noir/blanc','Related Sound File':'Fichier audio associé','Resolution Unit':'Unité de résolution',
    'Rows Per Strip':'Lignes par bande','Samples Per Pixel':'Échantillons par pixel','Saturation':'Saturation','Scene Capture Mode':'Mode de prise de vue',
    'Scene Type':'Type de scène','Security Classification':'Classification de sécurité','Self Timer':'Retardateur','Self Timer Mode':'Mode retardateur',
    'Sensing Method':'Méthode de détection','Sequence Number':'Numéro de séquence','Sharpness':'Netteté','Short Focal Length':'Distance focale courte',
    'Slow Sync':'Synchronisation lente','Software':'Logiciel','Software Release':'Version du logiciel','Spatial Frequency Response':'Réponse en fréquence spatiale',
    'Special Mode':'Mode spécial','Spectral Sensitivity':'Sensibilité spectrale','Strip Byte Counts':'Nombre d’octets par bande',
    'Strip Offsets':'Décalages des bandes','Subfile Type':'Type de sous-fichier','Subject Distance':'Distance du sujet','Subject Location':'Position du sujet',
    'Subsec Time':'Temps en sous-secondes','Subsec Time (Digitized)':'Temps en sous-secondes (numérisé)',
    'Subsec Time (Original)':'Temps en sous-secondes (original)','Tile Byte Counts':'Nombre d’octets par tuile','Tile Length':'Hauteur de tuile',
    'Tile Offsets':'Décalages des tuiles','Tile Width':'Largeur de tuile','Time Zone Offset':'Décalage du fuseau horaire','Tone':'Tonalité',
    'Transfer Function':'Fonction de transfert','User Comment':'Commentaire utilisateur','Version':'Version','White Balance':'Balance des blancs',
    'White Point':'Point blanc','X Resolution':'Résolution X','Y Resolution':'Résolution Y','EXIF Image Height':'Hauteur d’image EXIF',
    'EXIF Image Width':'Largeur d’image EXIF','IPTC: Supplemental Categories':'IPTC : catégories supplémentaires','IPTC: Keywords':'IPTC : mots-clés',
    'IPTC: Caption':'IPTC : légende','IPTC: Caption Writer':'IPTC : auteur de la légende','IPTC: Headline':'IPTC : titre',
    'IPTC: Special Instructions':'IPTC : instructions spéciales','IPTC: Category':'IPTC : catégorie','IPTC: Byline':'IPTC : auteur',
    'IPTC: Byline Title':'IPTC : fonction de l’auteur','IPTC: Credit':'IPTC : crédit','IPTC: Source':'IPTC : source',
    'IPTC: Copyright Notice':'IPTC : mention de droits d’auteur','IPTC: Object Name':'IPTC : nom de l’objet','IPTC: City':'IPTC : ville',
    'IPTC: Province State':'IPTC : province/région','IPTC: Country Name':'IPTC : pays','IPTC: Original Transmission Reference':'IPTC : référence de transmission originale',
    'IPTC: Date Created':'IPTC : date de création','IPTC: Copyright Flag':'IPTC : indicateur de droits d’auteur','IPTC: Time Created':'IPTC : heure de création',
    'Bulb':'Pose B','Normal (0 deg)':'Normale (0°)','Mirrored':'Miroir','Upsidedown':'Retournée','Upsidedown Mirrored':'Retournée en miroir',
    '90 deg CW Mirrored':'90° horaire en miroir','90 deg CCW':'90° antihoraire','90 deg CCW Mirrored':'90° antihoraire en miroir','90 deg CW':'90° horaire',
    'No Unit':'Sans unité','Inch':'Pouce','Centimeter':'Centimètre','Center of Pixel Array':'Centre de la matrice de pixels','Datum Point':'Point de référence',
    'Manual':'Manuel','Program':'Programme','Aperature Priority':'Priorité ouverture','Shutter Priority':'Priorité vitesse','Program Creative':'Programme créatif',
    'Program Action':'Programme action','Portrait':'Portrait','Landscape':'Paysage','Unknown':'Inconnu','Average':'Moyenne',
    'Center Weighted Average':'Moyenne pondérée centrale','Spot':'Spot','Multi-Spot':'Multi-spot','Multi-Segment':'Multizone','Partial':'Partielle','Other':'Autre',
    'Unknown or Auto':'Inconnu ou automatique','Daylight':'Lumière du jour','Flourescent':'Fluorescent','Tungsten':'Tungstène','Standard Light A':'Lumière standard A',
    'Standard Light B':'Lumière standard B','Standard Light C':'Lumière standard C','Uncalibrated':'Non calibré','No Compression':'Sans compression',
    'JPEG Compression':'Compression JPEG','Not Defined':'Non défini','Digital Still Camera':'Appareil photo numérique','Directly Photographed':'Photographié directement',
    'One Chip Color Area Sensor':'Capteur couleur mono-puce','Two Chip Color Area Sensor':'Capteur couleur à deux puces',
    'Three Chip Color Area Sensor':'Capteur couleur à trois puces','Color Sequential Area Sensor':'Capteur couleur séquentiel surfacique',
    'Trilinear Sensor':'Capteur trilinéaire','Color Sequential Linear Sensor':'Capteur couleur séquentiel linéaire','Monochrome':'Monochrome',
    'Flash did not fire':'Flash non déclenché','Flash Fired':'Flash déclenché','Strobe return light not detected':'Retour du flash non détecté',
    'Strobe returned light detected':'Retour du flash détecté','No flash function':'Aucune fonction flash',
}

# Flash descriptions and generic photographic phrases.
def translate(value):
    if value in exact:
        return exact[value]
    v = value
    flash_repl = [
        ('Flash fired, compulsory flash mode, red-eye reduction mode, return light not detected','Flash déclenché, mode forcé, réduction des yeux rouges, retour non détecté'),
        ('Flash fired, compulsory flash mode, red-eye reduction mode, return light detected','Flash déclenché, mode forcé, réduction des yeux rouges, retour détecté'),
        ('Flash fired, auto mode, return light not detected, red-eye reduction mode','Flash déclenché, mode auto, retour non détecté, réduction des yeux rouges'),
        ('Flash fired, auto mode, return light detected, red-eye reduction mode','Flash déclenché, mode auto, retour détecté, réduction des yeux rouges'),
        ('Flash fired, compulsory flash mode, return light not detected','Flash déclenché, mode forcé, retour non détecté'),
        ('Flash fired, compulsory flash mode, return light detected','Flash déclenché, mode forcé, retour détecté'),
        ('Flash fired, auto mode, return light not detected','Flash déclenché, mode auto, retour non détecté'),
        ('Flash fired, auto mode, return light detected','Flash déclenché, mode auto, retour détecté'),
        ('Flash fired, red-eye reduction mode, return light not detected','Flash déclenché, réduction des yeux rouges, retour non détecté'),
        ('Flash fired, red-eye reduction mode, return light detected','Flash déclenché, réduction des yeux rouges, retour détecté'),
        ('Flash fired, compulsory flash mode, red-eye reduction mode','Flash déclenché, mode forcé, réduction des yeux rouges'),
        ('Flash fired, auto mode, red-eye reduction mode','Flash déclenché, mode auto, réduction des yeux rouges'),
        ('Flash fired, red-eye reduction mode','Flash déclenché, réduction des yeux rouges'),
        ('Flash fired, compulsory flash mode','Flash déclenché, mode forcé'),
        ('Flash did not fire, compulsory flash mode','Flash non déclenché, mode forcé'),
        ('Flash did not fire, auto mode','Flash non déclenché, mode auto'),
        ('Flash fired, auto mode','Flash déclenché, mode auto'),
    ]
    for a,b in flash_repl:
        if v == a:
            return b
    replacements = [
        (' Warning',' - avertissement'),(' Position',' - position'),(' Selected',' sélectionné'),(' Used',' utilisé'),
        (' Sensitivity',' - sensibilité'),(' Mode',' - mode'),(' Settings',' - paramètres'),(' Setting',' - réglage'),
        (' Resolution',' - résolution'),(' Distance',' - distance'),(' Length',' - longueur'),(' Width',' - largeur'),(' Height',' - hauteur'),
        (' Offset',' - décalage'),(' Offsets',' - décalages'),(' Count',' - nombre'),(' Counts',' - nombres'),(' Source',' - source'),
        (' Description',' - description'),(' Number',' - numéro'),(' Ratio',' - rapport'),(' Configuration',' - configuration'),(' Index',' - indice'),
        (' Value',' - valeur'),(' Level',' - niveau'),(' Strength',' - puissance'),(' Energy',' - énergie'),(' Program',' - programme'),
        (' Method',' - méthode'),(' Classification',' - classification'),(' Comment',' - commentaire'),(' Functions',' - fonctions'),
    ]
    for a,b in replacements:
        v = v.replace(a,b)
    return v

assignments = ['// Complete EXIF/IPTC localization']
for key, value in entries:
    fr = translate(value).replace('\\', '\\\\').replace("'", "\\'")
    assignments.append("$LANG_MG04['%s'] = '%s';" % (key, fr))

french += '\n'.join(assignments) + '\n'

# Keep last direct assignment for every LANG_MG key.
lines = french.splitlines()
last = {}
for i, line in enumerate(lines):
    mm = re.match(r"\$(LANG_MG\d+)\['([^']+)'\]\s*=", line)
    if mm:
        last[(mm.group(1), mm.group(2))] = i
out = []
for i, line in enumerate(lines):
    mm = re.match(r"\$(LANG_MG\d+)\['([^']+)'\]\s*=", line)
    if mm and last[(mm.group(1), mm.group(2))] != i:
        continue
    out.append(line)
french_path.write_text('\n'.join(out) + '\n', encoding='utf-8')
print('Generated LANG_MG04 assignments:', len(entries))
