# -*- coding: utf-8 -*-
"""
Système de Calcul de Superficie - Division AT Kasaï Central
Conçu pour un usage administratif officiel.
Architecture : KivyMD (UI), Matplotlib (Cartographie), ReportLab (PDF), Numpy/Math (Calculs)
"""

import os
import sys
import math
import tempfile
import datetime
import random

# Désactiver complètement le logging pour éviter les problèmes d'exécution
import logging
logging.getLogger().setLevel(logging.CRITICAL + 1)
logging.disable(logging.CRITICAL + 1)

# Variables d'environnement pour Kivy
os.environ['KIVY_LOG_MODE'] = 'NONE'
os.environ['KIVY_WINDOW'] = 'sdl2'

# Configuration stricte de la fenêtre Kivy (doit précéder les autres imports Kivy)
from kivy.config import Config
Config.set('graphics', 'width', '700')
Config.set('graphics', 'height', '650')
Config.set('graphics', 'resizable', True)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand') # Désactive le red circle du multitouch

# Désactiver le logging Kivy spécifiquement
Config.set('kivy', 'log_level', 'critical')
Config.set('kivy', 'log_enable', '0')

# Isolement du backend Matplotlib pour éviter les conflits de threads avec la boucle Kivy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.utils import get_color_from_hex

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar

# Imports ReportLab pour la génération du PDF officiel
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ==============================================================================
# STRUCTURE UI (Kivy Language)
# ==============================================================================
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<PointRow>:
    size_hint_y: None
    height: "48dp"
    md_bg_color: get_color_from_hex("#FFFFFF")
    radius: [5, 5, 5, 5]
    padding: "10dp"
    spacing: "10dp"
    
    MDLabel:
        text: root.point_id
        size_hint_x: 0.2
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#1F2937")
        bold: True
    MDLabel:
        text: root.x_val
        size_hint_x: 0.35
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#1F2937")
    MDLabel:
        text: root.y_val
        size_hint_x: 0.35
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#1F2937")
    MDIconButton:
        icon: "delete"
        size_hint_x: 0.1
        theme_text_color: "Custom"
        text_color: 1, 0, 0, 1
        on_release: app.remove_point(root.index)

MDFloatLayout:
    md_bg_color: get_color_from_hex("#F5F5F5")
    
    MDBoxLayout:
        orientation: "vertical"
        
        # EN-TÊTE OFFICIEL
        MDBoxLayout:
            size_hint_y: None
            height: "70dp"
            md_bg_color: get_color_from_hex("#1E3A8A")
            padding: "20dp"
            
            MDLabel:
                text: "SYSTÈME DE CALCUL DE SUPERFICIE - DIVISION AT KASAÏ CENTRAL"
                font_style: "H6"
                bold: True
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                halign: "center"
                
        # CORPS DE L'APPLICATION
        MDBoxLayout:
            orientation: "horizontal"
            padding: "20dp"
            spacing: "20dp"
            
            # COLONNE GAUCHE : IDENTIFICATION ET SAISIE
            MDBoxLayout:
                orientation: "vertical"
                size_hint_x: 0.45
                spacing: "15dp"
                
                MDLabel:
                    text: "1. Identification du Terrain"
                    font_style: "Subtitle1"
                    bold: True
                    size_hint_y: None
                    height: "30dp"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#1F2937")
                
                MDTextField:
                    id: project_name
                    hint_text: "Nom du projet"
                    max_text_length: 100
                    mode: "rectangle"
                    
                MDTextField:
                    id: owner_name
                    hint_text: "Propriétaire / Demandeur"
                    max_text_length: 100
                    mode: "rectangle"
                    
                MDTextField:
                    id: location_field
                    hint_text: "Localisation"
                    text: "Kananga"
                    mode: "rectangle"
                    readonly: True
                    on_focus: if self.focus: app.menu_location.open()
                    
                MDTextField:
                    id: utm_zone
                    hint_text: "Zone UTM"
                    text: "33S"
                    mode: "rectangle"
                    readonly: True
                    
                MDLabel:
                    text: "2. Saisie des Coordonnées UTM"
                    font_style: "Subtitle1"
                    bold: True
                    size_hint_y: None
                    height: "30dp"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#1F2937")
                    
                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: "10dp"
                    size_hint_y: None
                    height: "60dp"
                    
                    MDTextField:
                        id: input_x
                        hint_text: "X (Easting)"
                        mode: "rectangle"
                        input_filter: "float"
                        
                    MDTextField:
                        id: input_y
                        hint_text: "Y (Northing)"
                        mode: "rectangle"
                        input_filter: "float"
                        
                MDRaisedButton:
                    text: "AJOUTER LE POINT"
                    md_bg_color: get_color_from_hex("#1E3A8A")
                    size_hint_x: 1
                    on_release: app.add_point()
                    
                Widget: # Spacer
                    
            # COLONNE DROITE : LISTE ET ACTIONS
            MDBoxLayout:
                orientation: "vertical"
                size_hint_x: 0.55
                spacing: "10dp"
                
                MDLabel:
                    text: "Points Enregistrés"
                    font_style: "Subtitle1"
                    bold: True
                    size_hint_y: None
                    height: "30dp"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#1F2937")
                    
                # En-tête de la liste
                MDBoxLayout:
                    size_hint_y: None
                    height: "30dp"
                    padding: ["10dp", "0dp", "10dp", "0dp"]
                    md_bg_color: get_color_from_hex("#E5E7EB")
                    
                    MDLabel:
                        text: "POINT"
                        size_hint_x: 0.2
                        bold: True
                        font_size: "12sp"
                    MDLabel:
                        text: "X (EASTING)"
                        size_hint_x: 0.35
                        bold: True
                        font_size: "12sp"
                    MDLabel:
                        text: "Y (NORTHING)"
                        size_hint_x: 0.35
                        bold: True
                        font_size: "12sp"
                    MDLabel:
                        text: "ACTION"
                        size_hint_x: 0.1
                        bold: True
                        font_size: "12sp"
                        
                # Conteneur des points
                ScrollView:
                    MDBoxLayout:
                        id: points_container
                        orientation: "vertical"
                        adaptive_height: True
                        spacing: "5dp"
                        
                MDFlatButton:
                    text: "VIDER LA LISTE"
                    theme_text_color: "Custom"
                    text_color: 1, 0, 0, 1
                    pos_hint: {"center_x": .5}
                    on_release: app.confirm_clear_points()
                    
                Widget:
                    size_hint_y: None
                    height: "20dp"
                    
                MDRaisedButton:
                    text: "GÉNÉRER LE RAPPORT OFFICIEL"
                    font_style: "H6"
                    md_bg_color: get_color_from_hex("#1E3A8A")
                    size_hint_x: 1
                    size_hint_y: None
                    height: "60dp"
                    on_release: app.generate_report()
'''

# ==============================================================================
# LOGIQUE MÉTIER ET COMPOSANTS
# ==============================================================================

class PointRow(MDBoxLayout):
    """Composant UI pour une ligne de coordonnée dans la liste."""
    point_id = StringProperty("")
    x_val = StringProperty("")
    y_val = StringProperty("")
    index = NumericProperty(0)

class ApplicationDivisionAT(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.points_data = [] # Structure: [{'x': float, 'y': float}]
        self.dialog = None
        self.temp_pdf_path = ""
        self.final_pdf_path = ""
        
        # Configuration Couleurs KivyMD (pour éléments de base)
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

    def build(self):
        Window.clearcolor = get_color_from_hex("#F5F5F5")
        self.root = Builder.load_string(KV)
        self.setup_dropdown()
        return self.root

    def setup_dropdown(self):
        locations = ["Kananga", "Tshikapa", "Ilebo", "Mweka", "Demba", "Dimbelenge"]
        menu_items = [
            {
                "text": loc,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=loc: self.set_location(x),
            } for loc in locations
        ]
        self.menu_location = MDDropdownMenu(
            caller=self.root.ids.location_field,
            items=menu_items,
            width_mult=4,
        )

    def set_location(self, text_item):
        self.root.ids.location_field.text = text_item
        self.menu_location.dismiss()
        # Tous sont 33S selon le cahier des charges
        self.root.ids.utm_zone.text = "33S"

    def show_error(self, message):
        from kivy.clock import Clock
        from kivy.uix.label import Label
        
        # Création manuelle d'un snackbar compatible KivyMD 1.2.0
        error_label = Label(
            text=message,
            color=(1, 1, 1, 1),
            font_size='14sp',
            size_hint_y=None,
            height=40,
            text_size=(None, None),
            halign='center',
            valign='middle',
            background_color=(0.725, 0.11, 0.11, 1),
            canvas_before=None
        )
        
        # Ajout à l'écran principal
        self.root.add_widget(error_label)
        
        # Retrait automatique après 3 secondes
        Clock.schedule_once(lambda dt: self.root.remove_widget(error_label), 3)

    # --- GESTION DES POINTS ---

    def add_point(self):
        str_x = self.root.ids.input_x.text.strip()
        str_y = self.root.ids.input_y.text.strip()
        
        if not str_x or not str_y:
            self.show_error("Format de coordonnées incorrect (champs vides).")
            return
            
        try:
            val_x = float(str_x)
            val_y = float(str_y)
        except ValueError:
            self.show_error("Format de coordonnées incorrect (valeurs numériques requises).")
            return
            
        self.points_data.append({'x': val_x, 'y': val_y})
        self.refresh_points_ui()
        
        # Réinitialisation champs
        self.root.ids.input_x.text = ""
        self.root.ids.input_y.text = ""
        self.root.ids.input_x.focus = True

    def remove_point(self, index):
        if 0 <= index < len(self.points_data):
            self.points_data.pop(index)
            self.refresh_points_ui()

    def confirm_clear_points(self):
        if not self.points_data:
            return
        if not self.dialog:
            self.dialog = MDDialog(
                text="Voulez-vous vraiment supprimer tous les points saisis ?",
                buttons=[
                    MDFlatButton(
                        text="ANNULER",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="CONFIRMER",
                        md_bg_color=get_color_from_hex("#B91C1C"),
                        on_release=self.execute_clear_points
                    ),
                ],
            )
        self.dialog.open()

    def execute_clear_points(self, *args):
        self.points_data = []
        self.refresh_points_ui()
        if self.dialog:
            self.dialog.dismiss()

    def refresh_points_ui(self):
        container = self.root.ids.points_container
        container.clear_widgets()
        for i, point in enumerate(self.points_data):
            row = PointRow(
                point_id=f"P{i+1}",
                x_val=f"{point['x']:,.2f}".replace(',', ' '),
                y_val=f"{point['y']:,.2f}".replace(',', ' '),
                index=i
            )
            container.add_widget(row)

    # --- CALCULS MATHÉMATIQUES (Shoelace / Distance Euclidienne) ---

    def calculate_metrics(self):
        n = len(self.points_data)
        area = 0.0
        perimeter = 0.0
        
        for i in range(n):
            j = (i + 1) % n
            # Formule de Shoelace pour la surface
            area += self.points_data[i]['x'] * self.points_data[j]['y']
            area -= self.points_data[j]['x'] * self.points_data[i]['y']
            
            # Distance Euclidienne pour le périmètre
            dx = self.points_data[j]['x'] - self.points_data[i]['x']
            dy = self.points_data[j]['y'] - self.points_data[i]['y']
            perimeter += math.hypot(dx, dy)
            
        area = abs(area) / 2.0
        hectares = area / 10000.0
        return area, hectares, perimeter

    # --- GÉNÉRATION DES RAPPORTS ---

    def generate_report(self):
        # 1. Validation de l'UI
        nom_projet = self.root.ids.project_name.text.strip()
        proprietaire = self.root.ids.owner_name.text.strip()
        
        if not nom_projet:
            self.show_error("Veuillez saisir le nom du projet")
            return
        if not proprietaire:
            self.show_error("Veuillez saisir le nom du propriétaire")
            return
        if len(self.points_data) < 3:
            self.show_error("Minimum trois points sont requis pour le calcul d'une superficie")
            return

        # 2. Calculs
        area_m2, area_ha, perim_m = self.calculate_metrics()

        # 3. Préparation Dossier et Fichiers
        doc_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'Rapports_Division_AT_KasaiCentral')
        os.makedirs(doc_dir, exist_ok=True)
        
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d")
        time_str = now.strftime("%H%M%S")
        safe_proj_name = "".join([c for c in nom_projet if c.isalpha() or c.isdigit() or c==' ']).rstrip()
        safe_proj_name = safe_proj_name.replace(' ', '_')
        
        ref_id = f"REF-{date_str}-{random.randint(100,999)}"
        filename = f"RAPPORT_{safe_proj_name}_{date_str}_{time_str}.pdf"
        self.final_pdf_path = os.path.join(doc_dir, filename)
        
        # 4. Génération Graphique Matplotlib
        temp_img_fd, temp_img_path = tempfile.mkstemp(suffix='.png')
        os.close(temp_img_fd)
        self.generate_plot(temp_img_path)

        # 5. Génération PDF
        data_dict = {
            'projet': nom_projet,
            'ref': ref_id,
            'loc': self.root.ids.location_field.text,
            'prop': proprietaire,
            'zone': self.root.ids.utm_zone.text,
            'date': now.strftime("%d/%m/%Y"),
            'heure': now.strftime("%H:%M:%S"),
            'area_m2': area_m2,
            'area_ha': area_ha,
            'perim_m': perim_m
        }
        
        try:
            self.build_pdf(self.final_pdf_path, temp_img_path, data_dict)
            self.show_success_dialog(area_m2, area_ha, perim_m)
        except Exception as e:
            self.show_error(f"Erreur lors de la création du PDF : {str(e)}")
        finally:
            # Nettoyage fichier temporaire graphique
            if os.path.exists(temp_img_path):
                try:
                    os.remove(temp_img_path)
                except:
                    pass

    def generate_plot(self, filepath):
        """Génère le graphique planimétrique professionnel et épuré."""
        import math
        
        # Configuration professionnelle du graphique
        plt.rcParams['font.family'] = 'Arial'
        plt.rcParams['font.size'] = 10
        
        fig, ax = plt.subplots(figsize=(12, 9))
        fig.patch.set_facecolor('white')
        
        # Fermeture du polygone pour le tracé
        xs = [p['x'] for p in self.points_data] + [self.points_data[0]['x']]
        ys = [p['y'] for p in self.points_data] + [self.points_data[0]['y']]
        
        # Tracé professionnel simple du polygone
        ax.plot(xs, ys, color='#003366', linestyle='-', linewidth=2, marker='o', markersize=8, 
                markerfacecolor='#CC0000', markeredgecolor='#990000', markeredgewidth=1)
        ax.fill(xs, ys, color='#003366', alpha=0.1)
        
        # Annotations simples des points
        for i, p in enumerate(self.points_data):
            ax.annotate(f'P{i+1}', (p['x'], p['y']), textcoords="offset points", 
                       xytext=(0,15), ha='center', fontsize=10, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='white', edgecolor='#003366', linewidth=1))
        
        # Annotations des distances sur les segments
        for i in range(len(self.points_data)):
            j = (i + 1) % len(self.points_data)
            x1, y1 = self.points_data[i]['x'], self.points_data[i]['y']
            x2, y2 = self.points_data[j]['x'], self.points_data[j]['y']
            
            # Calcul du point milieu pour l'annotation
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            # Calcul de la distance
            distance = math.hypot(x2 - x1, y2 - y1)
            
            # Annotation de la distance
            ax.annotate(f'{distance:.1f}m', (mid_x, mid_y), textcoords="offset points",
                       xytext=(0,-10), ha='center', fontsize=9, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', edgecolor='orange', linewidth=1, alpha=0.8))
        
        # Titre professionnel
        ax.set_title("PLAN DE SITUATION DU TERRAIN", fontsize=16, fontweight='bold', 
                   pad=20, color='#003366')
        ax.set_xlabel("COORDONNÉE X (Easting) en mètres", fontsize=12, fontweight='bold')
        ax.set_ylabel("COORDONNÉE Y (Northing) en mètres", fontsize=12, fontweight='bold')
        ax.set_aspect('equal', adjustable='datalim')
        ax.grid(True, linestyle='--', alpha=0.3, color='gray')
        
        # Personnalisation de l'apparence
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
        plt.close(fig)

    def build_pdf(self, pdf_path, img_path, data):
        """Construit le document PDF officiel de 3 pages via ReportLab."""
        import math
        from reportlab.platypus import PageBreak
        
        # Configuration professionnelle du document
        doc = SimpleDocTemplate(
            pdf_path, 
            pagesize=A4, 
            rightMargin=2.5*cm, 
            leftMargin=2.5*cm, 
            topMargin=2.5*cm, 
            bottomMargin=2.5*cm
        )
        elements = []
        styles = getSampleStyleSheet()
        
        # Styles professionnels améliorés
        title_style = ParagraphStyle(
            'TitleAdmin', 
            parent=styles['Heading1'], 
            alignment=TA_CENTER, 
            fontSize=16, 
            leading=20, 
            fontName='Times-Bold', 
            textColor=colors.HexColor('#003366'),
            spaceAfter=20
        )
        
        subtitle_style = ParagraphStyle(
            'Subtitle',
            parent=styles['Heading2'],
            alignment=TA_CENTER,
            fontSize=14,
            leading=16,
            fontName='Times-Bold',
            textColor=colors.HexColor('#CC0000'),
            spaceAfter=15
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=11,
            leading=13,
            fontName='Times-Roman',
            textColor=colors.black,
            spaceAfter=8
        )
        
        header_style = ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontSize=10,
            leading=12,
            fontName='Times-Bold',
            textColor=colors.black,
            spaceAfter=5
        )
        
        legal_style = ParagraphStyle(
            'Legal',
            parent=styles['Normal'], 
            fontSize=9, 
            leading=10,
            alignment=TA_CENTER, 
            textColor=colors.grey,
            fontName='Times-Roman'
        )
        
        # ===========================================
        # PAGE 1: EN-TÊTE ET INFORMATIONS GÉNÉRALES
        # ===========================================
        
        # 1. En-tête institutionnel professionnel avec image
        header_img = Image('C:\\Users\\israel\\Documents\\PLAN\\header.jpeg', width=16*cm, height=3*cm)
        header_img.hAlign = 'CENTER'
        elements.append(header_img)
        elements.append(Spacer(1, 15))
        
        # Ligne de séparation
        from reportlab.lib.units import mm
        from reportlab.platypus import HRFlowable
        elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.black))
        elements.append(Spacer(1, 20))
        
        # 2. Titre du document
        elements.append(Paragraph("AVIS DE CONFORMITE", subtitle_style))
        elements.append(Spacer(1, 25))
        
        # 3. Tableau Identification professionnel concis
        data_ident = [
            ['RÉFÉRENCE', data['ref']],
            ['PROJET', data['projet']],
            ['DEMANDEUR', data['prop']],
            ['LOCALITÉ', data['loc']],
            ['DATE', data['date']]
        ]
        
        t_ident = Table(data_ident, colWidths=[4.5*cm, 7.5*cm])
        t_ident.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (0,-1), 'Times-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        elements.append(t_ident)
        elements.append(Spacer(1, 25))
        
        # 5. Tableau Coordonnées simple
        coord_data = [['POINT', 'X (EASTING)', 'Y (NORTHING)']]
        
        for i in range(len(self.points_data)):
            x1 = self.points_data[i]['x']
            y1 = self.points_data[i]['y']
            
            coord_data.append([
                f"P{i+1}", 
                f"{x1:,.0f}".replace(',', ' '), 
                f"{y1:,.0f}".replace(',', ' ')
            ])
        
        t_coord = Table(coord_data, colWidths=[2.5*cm, 4.5*cm, 4.5*cm])
        t_coord.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.black),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 11),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        elements.append(t_coord)
        elements.append(Spacer(1, 25))
        
        # 5. Tableau Distances entre points
        dist_data = [['SEGMENT', 'DISTANCE (m)']]
        
        for i in range(len(self.points_data)):
            j = (i + 1) % len(self.points_data)
            x1 = self.points_data[i]['x']
            y1 = self.points_data[i]['y']
            x2 = self.points_data[j]['x']
            y2 = self.points_data[j]['y']
            
            distance = math.hypot(x2 - x1, y2 - y1)
            dist_data.append([
                f"P{i+1} - P{j+1}", 
                f"{distance:,.2f}".replace(',', ' ')
            ])
        
        t_dist = Table(dist_data, colWidths=[3.5*cm, 3.5*cm])
        t_dist.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.black),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 11),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        elements.append(t_dist)
        elements.append(Spacer(1, 25))
        
        # 4. Tableau Résultats principal
        res_data = [
            ['SURFACE (m²)', f"{data['area_m2']:,.0f}".replace(',', ' ')],
            ['SUPERFICIE (ha)', f"{data['area_ha']:,.2f}".replace(',', ' ')],
            ['PÉRIMÈTRE (m)', f"{data['perim_m']:,.0f}".replace(',', ' ')]
        ]
        
        t_res = Table(res_data, colWidths=[5*cm, 5*cm])
        t_res.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.black),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Times-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        elements.append(t_res)
        elements.append(Spacer(1, 30))
        
        # Footer page 1
        elements.append(PageBreak())
        
        # ===========================================
        # PAGE 2: PLAN GRAPHIQUE DÉTAILLÉ
        # ===========================================
        
        # Titre section graphique
        elements.append(Paragraph("PLAN SITUATION", subtitle_style))
        elements.append(Spacer(1, 25))
        
        # Image Graphique professionnelle
        img = Image(img_path, width=16*cm, height=10*cm)
        img.hAlign = 'CENTER'
        elements.append(img)
        elements.append(Spacer(1, 30))
        
        # Footer page 2
        elements.append(PageBreak())
        
        # ===========================================
        # PAGE 3: VALIDATIONS OFFICIELLES
        # ===========================================
        
        # Titre section signatures
        elements.append(Paragraph("VALIDATIONS OFFICIELLES", subtitle_style))
        elements.append(Spacer(1, 40))
        
        # Texte de présentation officiel
        presentation_text = """<b>LE PRÉSENT DOCUMENT ATTESTE OFFICIELLEMENT</b><br/><br/>
        Le calcul de superficie ci-dessus a été réalisé selon les normes topographiques en vigueur 
        et les techniques de calcul reconnues par l'Administration Publique.<br/><br/>
        Les résultats présentés dans ce rapport sont garantis par l'autorité compétente 
        et constituent la référence officielle pour toutes les procédures administratives."""
        
        elements.append(Paragraph(presentation_text, normal_style))
        elements.append(Spacer(1, 50))
        
        elements.append(Paragraph("<b>Fait à Kananga, le</b> " + data['date'], header_style))
        elements.append(Spacer(1, 50))
        
        # Signatures officielles améliorées
        sig_data = [
            [Paragraph("<b>LE CHEF DE DIVISION</b><br/>" +
                     "Aménagement du Territoire<br/>" +
                     "Gouvernement Provincial<br/>" +
                     "Kasaï Central<br/><br/>" +
                     "<b>Moise Mukaya Tshijuke</b>", header_style), 
             Paragraph("<b>LE RESPONSABLE TECHNIQUE</b><br/>" +
                     "Service Topographie<br/>" +
                     "Division AT<br/><br/>" +
                     "<b>Israel NTALU</b>", header_style)]
        ]
        
        t_sig = Table(sig_data, colWidths=[8*cm, 8*cm])
        t_sig.setStyle(TableStyle([
            ('ALIGN', (0,0), (0,-1), 'LEFT'),
            ('ALIGN', (1,0), (1,-1), 'RIGHT'),
            ('FONTNAME', (0,0), (-1,-1), 'Times-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 11),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]))
        elements.append(t_sig)
        elements.append(Spacer(1, 60))
        
        # Mentions légales officielles
        elements.append(HRFlowable(width="100%", thickness=2, lineCap='round', color=colors.black))
        elements.append(Spacer(1, 20))
        
        legal_text = """<b>CACHET ET SIGNATURE OBLIGATOIRES</b><br/><br/>
        Document officiel de la Division provinciale de l'amenagement du territoire 
        du Kasaï Central<br/>
        Valeur juridique : Conforme aux dispositions administratives en vigueur<br/>
        Numéro de référence : """ + data['ref'] + """<br/>
        Date d'émission : """ + data['date'] + """ """ + data['heure']
        
        elements.append(Paragraph(legal_text, legal_style))
        elements.append(Spacer(1, 20))
        
        # Footer officiel
        footer_text = ("<b>DOCUMENT OFFICIEL - GOUVERNEMENT PROVINCIAL KASAÏ CENTRAL</b><br/>"
                     "Division de l'Aménagement du Territoire - Service Topographie et Cartographie")
        
        elements.append(Paragraph(footer_text, ParagraphStyle(
            'FooterGov', 
            parent=legal_style, 
            textColor=colors.HexColor('#003366'), 
            fontName='Times-Bold',
            fontSize=9,
            alignment=TA_CENTER
        )))
        
        # Construction finale du document
        doc.build(elements)

    def show_success_dialog(self, area, ha, perim):
        msg = f"Surface : {area:,.2f} m²\nSuperficie : {ha:,.4f} ha\nPérimètre : {perim:,.2f} m\n\nFichier enregistré sous :\n{self.final_pdf_path}"
        msg = msg.replace(',', ' ')
        
        if self.dialog:
            self.dialog.dismiss()
            
        self.dialog = MDDialog(
            title="Rapport Généré avec Succès",
            text=msg,
            buttons=[
                MDFlatButton(
                    text="FERMER",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="OUVRIR LE DOSSIER",
                    md_bg_color=get_color_from_hex("#1E3A8A"),
                    on_release=lambda x: self.open_folder()
                ),
            ],
        )
        self.dialog.open()

    def open_folder(self):
        folder = os.path.dirname(self.final_pdf_path)
        if sys.platform == 'win32':
            os.startfile(folder)
        elif sys.platform == 'darwin':
            os.system(f'open "{folder}"')
        else:
            os.system(f'xdg-open "{folder}"')
        self.dialog.dismiss()

if __name__ == "__main__":
    ApplicationDivisionAT().run()