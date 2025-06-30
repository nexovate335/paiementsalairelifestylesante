# pourcentages_reels.py

POURCENTAGES = {
    'CONSULTATION GENERALE': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
    'CONSULTATION ORL': {
        'maison': 60,
        'acteur': 40,
    },
    'CERTIFICAT MEDICAL': {
        'maison': 70,
        'acteur': 30,
    },
    'ECHOGRAPHIE': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
    'HOSPITALISATION': {
        'maison': 70,
        'acteur': 30,
    },
    'IVA/IVL': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
    'MONITORAGE': {
        'maison': 60,
        'acteur': 40,
    },
    'LABORATOIRE': {
        'maison': 80,
        'acteurs_global': 20,
        'sous_repartition': {
            'prescripteur': 30,
            'technicien': 45,
            'preleveur': 15,
            'assistante_labo': 10,
        }
    },
    'LABO TRIOS': {
        'maison': 80,
        'acteurs_global': 20,
        'sous_repartition': {
            'preleveur': 40,
            'prescripteur': 60,
        }
    },
    'PANSEMENT': {
        'maison': 60,
        'acteur': 40,
    },
    'PHARMACIE': {
        'maison': 80,
        'sous_repartition': {
            'controleur': 4,
            'vendeur': 10,
            'prescripteur': 6,
        }
    },
    'VACCIN': {
        'maison': 70,
        'acteurs_global': 30,
        'sous_repartition': {
            'acteur1': 40,
            'acteur2': 40,
            'acteur3': 20,
        }
    },
    'ACCOUCHEMENT': {
        'maison': 65,
        'sous_repartition': {
            'medecin': 15,
            'sf': 10,
            'aide': 5,
            'pediatre': 5,
        }
    },
    'CESARIENNE': {
        'maison': 65,
        'acteurs_global': 35,
        'sous_repartition': {
            'chirurgien': 28,
            'aide': 15,
            'anesthesiste': 21,
            'panseur': 10,
            'instrumentiste': 10,
            'pediatre': 8,
            'sf': 8,
        }
    },
    'CURE HERNIE': {
        'maison': 50,
        'sous_repartition': {
            'chirurgien': 80,
            'aide': 15,
            'panseur': 5,
        }
    },
    'VARICOCELE': {
        'maison': 50,
        'sous_repartition': {
            'chirurgien': 80,
            'aide': 15,
            'panseur': 5,
        }
    },
    'MYOMECTOMIE': {
        'maison': 75,
        'sous_repartition': {
            'chirurgien': 45,
            'anesthesiste': 28,
            'aide': 17,
            'instrumentiste': 5,
            'panseur': 5,
        }
    },
    'HERNIE OMBILICALE': {
        'maison': 70,
        'sous_repartition': {
            'chirurgien': 60,
            'aide': 30,
            'panseur': 10,
        }
    },
    'POLYPE': {
        'maison': 70,
        'sous_repartition': {
            'chirurgien': 60,
            'aide': 30,
            'panseur': 10,
        }
    },
    'SHT': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
    'SONO HYSTEROGRAPHIE': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
    'IVG': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
    'HVV': {
        'maison': 75,
        'sous_repartition': {
            'chirurgien': 40,
            'anesthesiste': 25,
            'aide': 23,
            'instrumentiste': 6,
            'panseur': 6,
        }
    },
    'HVH': {
        'maison': 75,
        'sous_repartition': {
            'chirurgien': 45,
            'anesthesiste': 28,
            'aide': 17,
            'instrumentiste': 5,
            'panseur': 5,
        }
    },
    'PYRACIDECTOMIE': {
        'maison': 70,
        'sous_repartition': {
            'chirurgien': 15,
            'instrumentiste': 3.5,
            'panseur': 3.5,
            'aide': 8,
        }
    },
    'NODULECTOMIE SEIN': {
        'maison': 70,
        'sous_repartition': {
            'chirurgien': 15,
            'instrumentiste': 3.5,
            'panseur': 3.5,
            'aide': 8,
        }
    },
    'ACTES ORL': {
        'maison': 40,
        'acteur': 60,
    },
    'CONISATION': {
        'maison': 70,
        'sous_repartition': {
            'chirurgien': 15,
            'instrumentiste': 3.5,
            'panseur': 3.5,
            'aide': 8,
        }
    },
    'MALE ABDOMINALE': {
        'maison': 75,
        'sous_repartition': {
            'chirurgien': 45,
            'anesthesiste': 28,
            'aide': 17,
            'instrumentiste': 5,
            'panseur': 5,
        }
    },
    'EVENTRATION': {
        'maison': 70,
        'sous_repartition': {
            'chirurgien': 60,
            'aide': 30,
            'panseur': 10,
        }
    },
    'TPI': {
        'maison': 75,
        'sous_repartition': {
            'chirurgien': 45,
            'anesthesiste': 28,
            'aide': 17,
            'instrumentiste': 5,
            'panseur': 5,
        }
    },
    'MANCHESTER': {
        'maison': 75,
        'sous_repartition': {
            'chirurgien': 45,
            'anesthesiste': 28,
            'aide': 17,
            'instrumentiste': 5,
            'panseur': 5,
        }
    },
    'CIRCONCISION': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
    'BARTHOLINITE': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
    'SYNECHIE': {
        'maison': 70,
        'sous_repartition': {
            'chirurgien': 60,
            'aide': 30,
            'panseur': 10,
        }
    },
    'CATPOTOMIE': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
    'CAUTHERISATION': {
        'maison': 70,
        'sous_repartition': {
            'chirurgien': 60,
            'aide': 30,
            'panseur': 10,
        }
    },
    'CERCLAGE': {
        'maison': 70,
        'acteur': 25,
        'aide': 5,
    },
}
