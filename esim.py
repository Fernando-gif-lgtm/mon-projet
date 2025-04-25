import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import uuid
import hashlib
import random
import time
from datetime import datetime

class eSIM:
    """Classe représentant une carte eSIM virtuelle"""
    
    def __init__(self, imsi=None, iccid=None, msisdn=None, operator=None):
        # Identifiants uniques de la carte SIM
        self.imsi = imsi or self._generate_imsi()  # International Mobile Subscriber Identity
        self.iccid = iccid or self._generate_iccid()  # Integrated Circuit Card ID
        self.msisdn = msisdn or self._generate_msisdn()  # Numéro de téléphone
        
        # Informations sur l'opérateur
        self.operator = operator or "OpérateurDemo"
        self.profile_state = "Inactive"  # État du profil: Inactive, Active, Disabled
        
        # Génération de clés d'authentification (simulées)
        self.ki = self._generate_auth_key()  # Authentication Key
        self.opc = self._generate_auth_key()  # Operator Code
        
        # Données de consommation
        self.data_usage = 0  # En Mo
        self.data_limit = 10000  # 10 Go par défaut
        
        # Historique des événements
        self.events = []
        self.log_event("Création de l'eSIM")
    
    def _generate_imsi(self):
        """Génère un IMSI valide (15 chiffres)"""
        mcc = "208"  # Code pays (France)
        mnc = "01"   # Code réseau
        msin = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        return f"{mcc}{mnc}{msin}"
    
    def _generate_iccid(self):
        """Génère un ICCID valide (19-20 chiffres)"""
        iin = "8933"  # Issuer Identification Number
        ccn = ''.join([str(random.randint(0, 9)) for _ in range(15)])
        return f"{iin}{ccn}"
    
    def _generate_msisdn(self):
        """Génère un numéro de téléphone français"""
        return f"336{''.join([str(random.randint(0, 9)) for _ in range(8)])}"
    
    def _generate_auth_key(self):
        """Génère une clé d'authentification hexadécimale"""
        return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:32]
    
    def activate(self):
        """Active le profil eSIM"""
        if self.profile_state != "Active":
            self.profile_state = "Active"
            self.log_event("Activation du profil")
            return True
        return False
    
    def deactivate(self):
        """Désactive le profil eSIM"""
        if self.profile_state != "Inactive":
            self.profile_state = "Inactive"
            self.log_event("Désactivation du profil")
            return True
        return False
    
    def disable(self):
        """Désactive définitivement le profil eSIM"""
        if self.profile_state != "Disabled":
            self.profile_state = "Disabled"
            self.log_event("Désactivation définitive du profil")
            return True
        return False
    
    def add_data_usage(self, amount):
        """Ajoute de la consommation de données"""
        self.data_usage += amount
        self.log_event(f"Consommation de {amount} Mo de données")
    
    def reset_data_usage(self):
        """Réinitialise les compteurs de consommation"""
        old_usage = self.data_usage
        self.data_usage = 0
        self.log_event(f"Réinitialisation du compteur de données (ancien: {old_usage} Mo)")
    
    def change_operator(self, new_operator):
        """Change l'opérateur de l'eSIM"""
        old_operator = self.operator
        self.operator = new_operator
        self.log_event(f"Changement d'opérateur: {old_operator} -> {new_operator}")
    
    def log_event(self, description):
        """Ajoute un événement dans l'historique"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.events.append(f"[{timestamp}] {description}")


class eSIMManagerApp:
    """Application de gestion d'eSIM avec interface graphique Tkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire eSIM")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Style
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TButton", padding=6, relief="flat", background="#3498db")
        self.style.configure("TLabel", background="#f0f0f0", font=('Helvetica', 10))
        self.style.configure("Header.TLabel", font=('Helvetica', 12, 'bold'))
        
        # Conteneur principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Liste d'eSIMs disponibles (simulées)
        self.esims = []
        self.create_demo_esims()
        
        # eSIM actuellement sélectionnée
        self.selected_esim = None
        if self.esims:
            self.selected_esim = self.esims[0]
        
        # Création de l'interface
        self.create_widgets()
        
        # Simulation de trafic de données en arrière-plan
        self.simulate_data_usage()
    
    def create_demo_esims(self):
        """Crée quelques eSIMs de démonstration"""
        esim1 = eSIM(operator="Orange")
        esim1.activate()
        esim1.add_data_usage(1250)
        
        esim2 = eSIM(operator="SFR")
        
        esim3 = eSIM(operator="Bouygues Telecom")
        esim3.activate()
        esim3.add_data_usage(450)
        
        self.esims = [esim1, esim2, esim3]
    
    def create_widgets(self):
        """Crée tous les widgets de l'interface"""
        # Cadre pour la liste des eSIMs
        self.list_frame = ttk.LabelFrame(self.main_frame, text="eSIMs disponibles", padding="10")
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Liste des eSIMs
        self.esim_listbox = tk.Listbox(self.list_frame, width=30, font=('Helvetica', 10))
        self.esim_listbox.pack(fill=tk.BOTH, expand=True)
        self.update_esim_list()
        
        # Liaison de l'événement de sélection
        self.esim_listbox.bind('<<ListboxSelect>>', self.on_esim_select)
        
        # Cadre pour les détails de l'eSIM
        self.details_frame = ttk.LabelFrame(self.main_frame, text="Détails de l'eSIM", padding="10")
        self.details_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Zone de texte pour les détails
        self.details_text = tk.Text(self.details_frame, width=50, height=15, wrap=tk.WORD, font=('Courier', 10))
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.config(state=tk.DISABLED)
        
        # Cadre pour les actions
        self.actions_frame = ttk.LabelFrame(self.main_frame, text="Actions", padding="10")
        self.actions_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Boutons d'action
        self.btn_activate = ttk.Button(self.actions_frame, text="Activer", command=self.activate_esim)
        self.btn_activate.grid(row=0, column=0, padx=5, pady=5)
        
        self.btn_deactivate = ttk.Button(self.actions_frame, text="Désactiver", command=self.deactivate_esim)
        self.btn_deactivate.grid(row=0, column=1, padx=5, pady=5)
        
        self.btn_delete = ttk.Button(self.actions_frame, text="Supprimer", command=self.disable_esim)
        self.btn_delete.grid(row=0, column=2, padx=5, pady=5)
        
        self.btn_new = ttk.Button(self.actions_frame, text="Nouvelle eSIM", command=self.create_new_esim)
        self.btn_new.grid(row=0, column=3, padx=5, pady=5)
        
        self.btn_change_operator = ttk.Button(self.actions_frame, text="Changer d'opérateur", command=self.change_operator)
        self.btn_change_operator.grid(row=0, column=4, padx=5, pady=5)
        
        self.btn_reset_data = ttk.Button(self.actions_frame, text="Réinitialiser données", command=self.reset_data)
        self.btn_reset_data.grid(row=0, column=5, padx=5, pady=5)
        
        # Cadre pour l'historique
        self.history_frame = ttk.LabelFrame(self.main_frame, text="Historique des événements", padding="10")
        self.history_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Zone de texte pour l'historique
        self.history_text = tk.Text(self.history_frame, width=80, height=10, wrap=tk.WORD, font=('Courier', 9))
        self.history_text.pack(fill=tk.BOTH, expand=True)
        self.history_text.config(state=tk.DISABLED)
        
        # Configuration du redimensionnement
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=2)
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=2)
        
        # Mise à jour de l'affichage initial
        if self.selected_esim:
            self.update_esim_details()
            self.update_history()
    
    def update_esim_list(self):
        """Met à jour la liste des eSIMs dans le listbox"""
        self.esim_listbox.delete(0, tk.END)
        for esim in self.esims:
            self.esim_listbox.insert(tk.END, f"{esim.operator} ({esim.profile_state})")
    
    def on_esim_select(self, event):
        """Gère la sélection d'une eSIM dans la liste"""
        try:
            index = self.esim_listbox.curselection()[0]
            self.selected_esim = self.esims[index]
            self.update_esim_details()
            self.update_history()
        except (IndexError, KeyError):
            pass
    
    def update_esim_details(self):
        """Met à jour l'affichage des détails de l'eSIM sélectionnée"""
        if not self.selected_esim:
            return
        
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        details = [
            f"INFORMATIONS GÉNÉRALES:",
            f"----------------------",
            f"Opérateur: {self.selected_esim.operator}",
            f"État du profil: {self.selected_esim.profile_state}",
            f"",
            f"IDENTIFIANTS:",
            f"------------",
            f"IMSI: {self.selected_esim.imsi}",
            f"ICCID: {self.selected_esim.iccid}",
            f"MSISDN (téléphone): {self.selected_esim.msisdn}",
            f"",
            f"AUTHENTIFICATION:",
            f"----------------",
            f"Clé Ki: {self.selected_esim.ki[:8]}...{self.selected_esim.ki[-8:]}",
            f"Code OPc: {self.selected_esim.opc[:8]}...{self.selected_esim.opc[-8:]}",
            f"",
            f"CONSOMMATION:",
            f"-------------",
            f"Données utilisées: {self.selected_esim.data_usage} Mo",
            f"Limite de données: {self.selected_esim.data_limit} Mo",
            f"Pourcentage utilisé: {(self.selected_esim.data_usage / self.selected_esim.data_limit) * 100:.2f}%"
        ]
        
        self.details_text.insert(tk.END, "\n".join(details))
        self.details_text.config(state=tk.DISABLED)
    
    def update_history(self):
        """Met à jour l'affichage de l'historique des événements"""
        if not self.selected_esim:
            return
        
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        for event in self.selected_esim.events:
            self.history_text.insert(tk.END, f"{event}\n")
        
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)  # Défilement automatique vers le bas
    
    def activate_esim(self):
        """Active l'eSIM sélectionnée"""
        if not self.selected_esim:
            messagebox.showinfo("Information", "Veuillez sélectionner une eSIM")
            return
        
        if self.selected_esim.activate():
            messagebox.showinfo("Activation", f"L'eSIM {self.selected_esim.operator} a été activée")
            self.update_esim_list()
            self.update_esim_details()
            self.update_history()
        else:
            messagebox.showinfo("Information", "Cette eSIM est déjà active")
    
    def deactivate_esim(self):
        """Désactive l'eSIM sélectionnée"""
        if not self.selected_esim:
            messagebox.showinfo("Information", "Veuillez sélectionner une eSIM")
            return
        
        if self.selected_esim.deactivate():
            messagebox.showinfo("Désactivation", f"L'eSIM {self.selected_esim.operator} a été désactivée")
            self.update_esim_list()
            self.update_esim_details()
            self.update_history()
        else:
            messagebox.showinfo("Information", "Cette eSIM est déjà inactive")
    
    def disable_esim(self):
        """Désactive définitivement l'eSIM sélectionnée"""
        if not self.selected_esim:
            messagebox.showinfo("Information", "Veuillez sélectionner une eSIM")
            return
        
        confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer définitivement cette eSIM ?")
        if not confirm:
            return
        
        if self.selected_esim.disable():
            messagebox.showinfo("Suppression", f"L'eSIM {self.selected_esim.operator} a été supprimée")
            self.update_esim_list()
            self.update_esim_details()
            self.update_history()
        else:
            messagebox.showinfo("Information", "Cette eSIM est déjà désactivée définitivement")
    
    def create_new_esim(self):
        """Crée une nouvelle eSIM"""
        operator = simpledialog.askstring("Nouvel opérateur", "Nom de l'opérateur :")
        if operator:
            new_esim = eSIM(operator=operator)
            self.esims.append(new_esim)
            self.selected_esim = new_esim
            self.update_esim_list()
            self.update_esim_details()
            self.update_history()
            # Sélectionner la nouvelle eSIM dans la liste
            self.esim_listbox.selection_clear(0, tk.END)
            self.esim_listbox.selection_set(len(self.esims) - 1)
    
    def change_operator(self):
        """Change l'opérateur de l'eSIM sélectionnée"""
        if not self.selected_esim:
            messagebox.showinfo("Information", "Veuillez sélectionner une eSIM")
            return
        
        new_operator = simpledialog.askstring("Changer d'opérateur", 
                                             f"Nouvel opérateur pour {self.selected_esim.operator} :")
        if new_operator:
            self.selected_esim.change_operator(new_operator)
            self.update_esim_list()
            self.update_esim_details()
            self.update_history()
    
    def reset_data(self):
        """Réinitialise le compteur de données de l'eSIM sélectionnée"""
        if not self.selected_esim:
            messagebox.showinfo("Information", "Veuillez sélectionner une eSIM")
            return
        
        self.selected_esim.reset_data_usage()
        self.update_esim_details()
        self.update_history()
        messagebox.showinfo("Données réinitialisées", "Le compteur de données a été remis à zéro")
    
    def simulate_data_usage(self):
        """Simule l'utilisation des données en arrière-plan pour les eSIMs actives"""
        for esim in self.esims:
            if esim.profile_state == "Active":
                # Consommation aléatoire entre 1 et 20 Mo
                data_amount = random.uniform(1, 20)
                esim.add_data_usage(data_amount)
        
        # Mise à jour de l'interface si nécessaire
        if self.selected_esim and self.selected_esim.profile_state == "Active":
            self.update_esim_details()
            self.update_history()
        
        # Planification de la prochaine simulation (toutes les 30 secondes)
        self.root.after(30000, self.simulate_data_usage)

        confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir désactiver définitivement cette eSIM ?")
        if confirm and self.selected_esim.disable():
            messagebox.showinfo("Désactivation", "L'eSIM a été désactivée définitivement")
            self.update_esim_list()
            self.update_esim_details()
            self.update_history()
        else:
            messagebox.showinfo("Information", "L'eSIM est déjà désactivée définitivement")

    def create_new_esim(self):
        """Crée une nouvelle eSIM"""
        operator = simpledialog.askstring("Nouvelle eSIM", "Nom de l'opérateur :")
        if operator:
            new_esim = eSIM(operator=operator)
            self.esims.append(new_esim)
            self.selected_esim = new_esim
            self.update_esim_list()
            self.update_esim_details()
            self.update_history()
            messagebox.showinfo("Succès", "Nouvelle eSIM créée avec succès")

    def change_operator(self):
        """Change l'opérateur de l'eSIM sélectionnée"""
        if not self.selected_esim:
            messagebox.showinfo("Information", "Veuillez sélectionner une eSIM")
            return
        
        new_operator = simpledialog.askstring("Changement d'opérateur", "Entrez le nouvel opérateur :")
        if new_operator:
            self.selected_esim.change_operator(new_operator)
            self.update_esim_list()
            self.update_esim_details()
            self.update_history()
            messagebox.showinfo("Succès", f"Opérateur changé pour {new_operator}")

    def reset_data(self):
        """Réinitialise la consommation de données de l'eSIM sélectionnée"""
        if not self.selected_esim:
            messagebox.showinfo("Information", "Veuillez sélectionner une eSIM")
            return
        
        self.selected_esim.reset_data_usage()
        self.update_esim_details()
        self.update_history()
        messagebox.showinfo("Succès", "Compteur de données réinitialisé")

    def simulate_data_usage(self):
        """Simule une consommation de données toutes les 10 secondes"""
        if self.selected_esim and self.selected_esim.profile_state == "Active":
            used_data = random.randint(1, 20)  # Mo consommés
            self.selected_esim.add_data_usage(used_data)
            self.update_esim_details()
            self.update_history()
        
        # Replanifie la simulation dans 10 secondes
        self.root.after(10000, self.simulate_data_usage)
       


if __name__ == "__main__":
    root = tk.Tk()
    app = eSIMManagerApp(root)
    root.mainloop()


