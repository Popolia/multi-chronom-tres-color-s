#!/usr/bin/env python3
"""
Gestionnaire de lignes - multi-chronomètres colorés
-----------------------------------------------------
- Chaque ligne a : une couleur, un compteur, un chronomètre indépendant
- Bouton unique Play/Pause par ligne pour lancer/mettre en pause le chrono
- Bouton Reset avec confirmation avant de remettre le chrono et le compteur à zéro
- Bouton "+" pour ajouter autant de lignes que voulu, avec choix de couleur
- Chaque ligne peut être modifiée (couleur, suppression) même en cours
"""

import tkinter as tk
from tkinter import colorchooser, messagebox
import time
import sys
import ctypes
import json
import os

# Cache la fenêtre console (cmd) sous Windows si le script est lancé
# avec python.exe au lieu de pythonw.exe / --windowed
if sys.platform == "win32":
    try:
        console_window = ctypes.windll.kernel32.GetConsoleWindow()
        if console_window != 0:
            ctypes.windll.user32.ShowWindow(console_window, 0)  # 0 = SW_HIDE
    except Exception:
        pass


def dossier_appli():
    """Dossier où se trouve le script ou l'exe (marche en .py et en .exe compilé)."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


SAVE_PATH = os.path.join(dossier_appli(), "sauvegarde_lignes.json")
ICON_PATH = os.path.join(dossier_appli(), "assets", "logo.png")

# Palette reprise du logo
BG_DARK = "#1e2327"
BG_CARD = "#2b3238"
BG_CARD_HOVER = "#333b42"
TEXT_LIGHT = "#f4f6f7"
TEXT_MUTED = "#9aa3ab"
ACCENT_RED = "#e74c3c"
ACCENT_BLUE = "#3498db"
ACCENT_GREEN = "#2ecc71"


class Ligne:
    """Une ligne = couleur + compteur + chronomètre indépendant."""

    _next_id = 1

    def __init__(self, app, parent_frame, couleur="#3498db", nom=None, compteur=0, elapsed=0.0, forced_id=None):
        self.app = app
        if forced_id is not None:
            self.id = forced_id
            Ligne._next_id = max(Ligne._next_id, forced_id + 1)
        else:
            self.id = Ligne._next_id
            Ligne._next_id += 1

        self.couleur = couleur
        self.nom = nom if nom else f"Ligne {self.id}"
        self.compteur = compteur
        self.elapsed = elapsed          # secondes déjà écoulées (accumulées)
        self.running = False
        self.start_time = None
        self._after_job = None

        self.frame = tk.Frame(
            parent_frame, bg=BG_CARD, padx=12, pady=10,
            highlightbackground=self.couleur, highlightthickness=2, bd=0
        )
        self.frame.pack(fill="x", pady=5, padx=6)

        self._build_ui()
        self._refresh_color()
        self._refresh_time_label()

    # ---------- UI ----------
    def _build_ui(self):
        # Pastille couleur (cliquable pour changer)
        self.color_btn = tk.Button(
            self.frame, width=3, height=1, relief="flat", bd=0,
            cursor="hand2", command=self.choisir_couleur
        )
        self.color_btn.grid(row=0, column=0, rowspan=2, padx=(0, 12))

        self.nom_label = tk.Label(
            self.frame, text=self.nom, font=("Segoe UI", 11, "bold"),
            bg=BG_CARD, fg=TEXT_LIGHT, cursor="hand2"
        )
        self.nom_label.grid(row=0, column=1, sticky="w")
        self.nom_label.bind("<Double-Button-1>", self.editer_nom)

        # Compteur
        tk.Label(
            self.frame, text="Compteur :", bg=BG_CARD, fg=TEXT_MUTED, font=("Segoe UI", 9)
        ).grid(row=1, column=1, sticky="w")
        self.compteur_label = tk.Label(
            self.frame, text=str(self.compteur), font=("Consolas", 12, "bold"),
            bg=BG_CARD, fg=TEXT_LIGHT, width=4
        )
        self.compteur_label.grid(row=1, column=2, sticky="w")
        tk.Button(
            self.frame, text="-", width=2, relief="flat", bd=0, cursor="hand2",
            bg=BG_DARK, fg=TEXT_LIGHT, activebackground=ACCENT_RED, activeforeground=TEXT_LIGHT,
            command=self.decrementer
        ).grid(row=1, column=3, padx=2)
        tk.Button(
            self.frame, text="+", width=2, relief="flat", bd=0, cursor="hand2",
            bg=BG_DARK, fg=TEXT_LIGHT, activebackground=ACCENT_GREEN, activeforeground=TEXT_LIGHT,
            command=self.incrementer
        ).grid(row=1, column=4, padx=2)

        # Chrono
        self.time_label = tk.Label(
            self.frame, text="00:00:00", font=("Consolas", 18, "bold"),
            bg=BG_CARD, fg=TEXT_LIGHT, width=9
        )
        self.time_label.grid(row=0, column=5, rowspan=2, padx=18)

        self.play_btn = tk.Button(
            self.frame, text="Démarrer", width=10, relief="flat", bd=0, cursor="hand2",
            bg=ACCENT_GREEN, fg="white", activebackground="#27ae60", activeforeground="white",
            command=self.toggle_play
        )
        self.play_btn.grid(row=0, column=6, padx=4, pady=2)

        tk.Button(
            self.frame, text="Reset", width=8, relief="flat", bd=0, cursor="hand2",
            bg=BG_DARK, fg=TEXT_LIGHT, activebackground=ACCENT_BLUE, activeforeground="white",
            command=self.demander_reset
        ).grid(row=1, column=6, padx=4, pady=2)

        tk.Button(
            self.frame, text="✕", width=2, relief="flat", bd=0, cursor="hand2",
            bg=BG_CARD, fg=ACCENT_RED, activebackground=ACCENT_RED, activeforeground="white",
            command=self.supprimer
        ).grid(row=0, column=7, rowspan=2, padx=(18, 0))

    def _refresh_color(self):
        self.color_btn.config(bg=self.couleur, activebackground=self.couleur)
        self.frame.config(highlightbackground=self.couleur, highlightcolor=self.couleur)

    def editer_nom(self, event=None):
        entry = tk.Entry(
            self.frame, font=("Segoe UI", 11, "bold"), width=15,
            bg=BG_DARK, fg=TEXT_LIGHT, insertbackground=TEXT_LIGHT, relief="flat"
        )
        entry.insert(0, self.nom)
        entry.select_range(0, "end")
        entry.grid(row=0, column=1, sticky="w")
        entry.focus_set()

        def valider(event=None):
            nouveau = entry.get().strip()
            if nouveau:
                self.nom = nouveau
                self.nom_label.config(text=self.nom)
            entry.destroy()
            self.app.sauvegarder()

        entry.bind("<Return>", valider)
        entry.bind("<FocusOut>", valider)

    def choisir_couleur(self):
        rgb, hexcolor = colorchooser.askcolor(color=self.couleur, title=f"Couleur de la ligne {self.id}")
        if hexcolor:
            self.couleur = hexcolor
            self._refresh_color()
            self.app.sauvegarder()

    # ---------- Compteur ----------
    def incrementer(self):
        self.compteur += 1
        self.compteur_label.config(text=str(self.compteur))
        self.app.sauvegarder()

    def decrementer(self):
        self.compteur = max(0, self.compteur - 1)
        self.compteur_label.config(text=str(self.compteur))
        self.app.sauvegarder()

    # ---------- Chrono ----------
    def toggle_play(self):
        if self.running:
            self._pause()
        else:
            self._start()
        self.app.sauvegarder()

    def _start(self):
        self.running = True
        self.start_time = time.time()
        self.play_btn.config(text="Pause", bg=ACCENT_RED, activebackground="#c0392b")
        self._tick()

    def _pause(self):
        self.running = False
        if self.start_time is not None:
            self.elapsed += time.time() - self.start_time
        self.start_time = None
        self.play_btn.config(text="Démarrer", bg=ACCENT_GREEN, activebackground="#27ae60")
        if self._after_job is not None:
            self.frame.after_cancel(self._after_job)
            self._after_job = None
        self._refresh_time_label()

    def _tick(self):
        if self.running:
            self._refresh_time_label()
            self._after_job = self.frame.after(200, self._tick)

    def _temps_total(self):
        if self.running and self.start_time is not None:
            return self.elapsed + (time.time() - self.start_time)
        return self.elapsed

    def _refresh_time_label(self):
        total = int(self._temps_total())
        h, rem = divmod(total, 3600)
        m, s = divmod(rem, 60)
        self.time_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")

    def demander_reset(self):
        if messagebox.askyesno(
            "Confirmer le reset",
            f"Remettre à zéro le chrono et le compteur de la ligne {self.id} ?"
        ):
            self._pause()
            self.elapsed = 0.0
            self.compteur = 0
            self.compteur_label.config(text="0")
            self._refresh_time_label()
            self.app.sauvegarder()

    def supprimer(self):
        if messagebox.askyesno("Supprimer la ligne", f"Supprimer définitivement la ligne {self.id} ?"):
            self._pause()
            self.frame.destroy()
            self.app.lignes.remove(self)
            self.app.sauvegarder()

    # ---------- Sauvegarde ----------
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "couleur": self.couleur,
            "compteur": self.compteur,
            "elapsed": self._temps_total(),
        }


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Chronomètres Colorés")
        self.root.geometry("820x540")
        self.root.configure(bg=BG_DARK)

        # Icône de la fenêtre (remplace la plume tkinter par défaut)
        if os.path.exists(ICON_PATH):
            try:
                self._icon_img = tk.PhotoImage(file=ICON_PATH)
                self.root.iconphoto(True, self._icon_img)
            except Exception:
                pass

        # Barre du haut
        top = tk.Frame(root, bg=BG_DARK, pady=10)
        top.pack(fill="x")
        tk.Button(
            top, text="+ Ajouter une ligne", font=("Segoe UI", 10, "bold"),
            relief="flat", bd=0, cursor="hand2",
            command=self.ajouter_ligne, bg=ACCENT_GREEN, fg="white",
            activebackground="#27ae60", activeforeground="white",
            padx=10, pady=4
        ).pack(side="left", padx=12)

        # Zone scrollable pour les lignes
        container = tk.Frame(root, bg=BG_DARK)
        container.pack(fill="both", expand=True, padx=6, pady=4)

        canvas = tk.Canvas(container, highlightthickness=0, bg=BG_DARK)
        scrollbar = tk.Scrollbar(
            container, orient="vertical", command=canvas.yview,
            bg=BG_CARD, troughcolor=BG_DARK, activebackground=ACCENT_BLUE, bd=0
        )
        self.lignes_frame = tk.Frame(canvas, bg=BG_DARK)

        self.lignes_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.lignes_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Molette souris
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-e.delta / 120), "units"))

        self.lignes = []
        self.palette = ["#e74c3c", "#3498db", "#2ecc71", "#f1c40f", "#9b59b6", "#1abc9c"]

        if not self.charger():
            # Aucune sauvegarde trouvée : 3 lignes de départ (couleur 1, 2, 3)
            for i in range(3):
                self.ajouter_ligne(couleur=self.palette[i % len(self.palette)])

        # Sauvegarde automatique à la fermeture de la fenêtre
        self.root.protocol("WM_DELETE_WINDOW", self.fermer)

    def ajouter_ligne(self, couleur=None, nom=None, compteur=0, elapsed=0.0, forced_id=None):
        if couleur is None:
            couleur = self.palette[len(self.lignes) % len(self.palette)]
        ligne = Ligne(
            self, self.lignes_frame, couleur=couleur,
            nom=nom, compteur=compteur, elapsed=elapsed, forced_id=forced_id
        )
        self.lignes.append(ligne)
        self.sauvegarder()

    # ---------- Sauvegarde / chargement ----------
    def sauvegarder(self):
        try:
            data = {"lignes": [l.to_dict() for l in self.lignes]}
            with open(SAVE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erreur de sauvegarde : {e}")

    def charger(self):
        """Retourne True si une sauvegarde a été trouvée et chargée."""
        if not os.path.exists(SAVE_PATH):
            return False
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Erreur de lecture de la sauvegarde : {e}")
            return False

        lignes_data = data.get("lignes", [])
        if not lignes_data:
            return False

        for ld in lignes_data:
            self.ajouter_ligne_silencieuse(
                couleur=ld.get("couleur", "#3498db"),
                nom=ld.get("nom"),
                compteur=ld.get("compteur", 0),
                elapsed=ld.get("elapsed", 0.0),
                forced_id=ld.get("id"),
            )
        return True

    def ajouter_ligne_silencieuse(self, couleur, nom, compteur, elapsed, forced_id):
        """Comme ajouter_ligne mais sans déclencher une sauvegarde (utilisé au chargement)."""
        ligne = Ligne(
            self, self.lignes_frame, couleur=couleur,
            nom=nom, compteur=compteur, elapsed=elapsed, forced_id=forced_id
        )
        self.lignes.append(ligne)

    def fermer(self):
        self.sauvegarder()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
