# Web-View-Automation
> Web automation script via third-party website — Educational purposes only

---

## Description

Ce projet Python illustre des techniques d'automatisation web à l'aide de 
Selenium WebDriver. Il simule l'interaction d'un utilisateur avec une 
interface web tierce dans un cadre de démonstration technique.

---

## Fonctionnement global

Le script exécute un cycle automatisé structuré comme suit :
- Accès à la page du service
- Insertion d'une URL dans un champ de saisie
- Soumission de la demande
- Attente du traitement (compte à rebours)
- Vérification du succès de l'opération
- Gestion du délai imposé (cooldown)
- Répétition du processus après une pause

---

## Architecture du script

**Initialisation**
- Configuration du système de logs
- Définition des paramètres principaux

**Création du navigateur — `make_driver()`**
- Instance Chrome via Selenium
- Support du mode headless
- Options de discrétion pour les tests

**Interaction avec la page**
- Fermeture des popups
- Localisation et remplissage du champ de saisie
- Soumission du formulaire

**Gestion du cooldown**
- Détection du message de temporisation
- Extraction et respect du délai imposé

**Boucle principale — `main()`**
- Exécution continue
- Pause entre chaque cycle
- Arrêt manuel uniquement

---

## Prérequis

- Python 3.x
- Google Chrome installé
- ChromeDriver compatible avec votre version de Chrome

---

## Installation
```bash
pip install selenium webdriver-manager
```

## Exécution
```bash
python main.py
```

---

## Avertissement légal / Legal Notice

Ce projet est publié **uniquement à des fins éducatives** dans le cadre 
de la démonstration de techniques d'automatisation web (Selenium WebDriver).

**L'auteur interdit expressément toute utilisation visant à :**
- Contourner les Conditions Générales d'Utilisation de tout service en ligne
- Manipuler artificiellement des métriques ou statistiques
- Automatiser des actions sur des systèmes tiers sans autorisation explicite
- Violer toute législation applicable, notamment le **Code pénal français 
  (art. 323-1 et suivants)** relatif aux atteintes aux systèmes de traitement 
  automatisé de données

**Responsabilité :**  
L'auteur décline toute responsabilité quant aux usages détournés de ce projet.  
En utilisant ce code, l'utilisateur reconnaît en assumer l'**entière 
responsabilité légale et civile**.

Ce projet ne fournit, n'héberge, ni ne contrôle aucun service tiers.  
Il illustre uniquement des mécanismes d'interaction avec des interfaces web.

> *This software is provided for educational purposes only.  
> Any misuse is strictly prohibited and solely the responsibility 
> of the end user.*

---

## License

Proprietary — See [LICENSE](./LICENSE) for details.  
(c) 2026 voidseeker66. All rights reserved.

---

⭐ Si ce projet t'a été utile dans ton apprentissage, laisse une star !
