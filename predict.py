from fastapi import APIRouter
from dataclasses import dataclass
from typing import Optional
wine_data = []
import csv

router = APIRouter()


@dataclass
class Wine:
    fixed_acidity : float
    volatile_acidity : float
    citric_acid : float
    residual_sugar : float
    chlorides : float
    free_sulfur_dioxide : float
    total_sulfur_dioxide : float
    density : float
    pH : float
    sulphates : float
    alcohol : float
    quality: Optional[int]
    id : Optional[int]
    
    def __init__(self, fixed_acidity, volatile_acidity, citric_acid, 
                residual_sugar, chlorides, free_sulfur_dioxide,
                total_sulfur_dioxide, density, pH, sulphates,
                alcohol, quality, id):
        self.fixed_acidity = float(fixed_acidity)
        self.volatile_acidity = float(volatile_acidity)
        self.citric_acid = float(citric_acid)
        self.residual_sugar = float(residual_sugar)
        self.chlorides = float(chlorides)
        self.free_sulfur_dioxide = float(free_sulfur_dioxide)
        self.total_sulfur_dioxide = float(total_sulfur_dioxide)
        self.density = float(density)
        self.pH = float(pH)
        self.sulphates = float(sulphates)
        self.alcohol = float(alcohol)
        self.quality = int(quality)
        self.id = int(id)
      

with open('./data/Wines.csv', 'r') as wine:
    lines = csv.reader(wine, delimiter=",")
    lines2 = list(lines)[1:]
    for line in lines2:
        wine_propre = Wine(*line)
        wine_data.append(wine_propre)

def predict(fixed, volatile, citric, sugar, chlo, free, total, pH, sul, alc):
    poids_fixed, poids_volatile, poids_citric, poids_sugar, poids_chlo = 0, 0, 0, 0, 0
    poids_free, poids_total, poids_pH, poids_sul, poids_alc = 0, 0, 0, 0, 0
    
    if (fixed < 4):
        poids_fixed = 1
    elif (fixed < 8):
        poids_fixed = 2
    elif (fixed < 12):
        poids_fixed = 3
    else :
        poids_fixed = 4
    
    if (volatile < 0.3):
        poids_volatile = 1
    elif (volatile < 0.6):
        poids_volatile = 2
    elif (volatile < 0.9):
        poids_volatile = 3
    elif (volatile < 1.2):
        poids_volatile = 4
    elif (volatile < 1.5):
        poids_volatile = 5
    else :
        poids_volatile = 6
    
    if (citric < 0.5):
        poids_citric = 1
    else :
        poids_citric = 2
    
    if(sugar < 2):
        poids_sugar = 1
    elif (sugar < 4):
        poids_sugar = 2
    elif(sugar < 6):
        poids_sugar = 3
    elif(sugar < 8):
        poids_sugar = 4
    elif(sugar < 10):
        poids_sugar = 5
    elif(sugar < 12):
        poids_sugar = 6
    elif(sugar < 14):
        poids_sugar = 7
    else:
        poids_sugar = 8
    
    if (chlo < 0.2):
        poids_chlo = 1
    elif (chlo < 0.4):
        poids_chlo = 2
    else :
        poids_chlo = 3
    
    if(free < 10):
        poids_free = 1
    elif (free < 20):
        poids_free = 2
    elif(free < 30):
        poids_free = 3
    elif(free < 40):
        poids_free = 4
    elif(free < 50):
        poids_free = 5
    elif(free < 60):
        poids_free = 6
    else:
        poids_free = 7
    
    if(total < 50):
        poids_total = 1
    elif (total < 100):
        poids_total = 2
    elif(total < 150):
        poids_total = 3
    elif(total < 200):
        poids_total = 4
    elif(total < 250):
        poids_total = 5
    else:
        poids_total = 6
    
    if(pH < 3.15):
        poids_pH = 1
    elif (pH < 3.55):
        poids_pH = 2
    else : 
        poids_pH = 1
    
    if(sul < 0.5):
        poids_sul = 1
    elif (sul < 1):
        poids_sul = 2
    elif (sul < 1.5):
        poids_sul = 3
    else :
        poids_sul = 4
    
    if(alc < 9.5):
        poids_alc = 1
    elif (alc < 10.6):
        poids_alc = 2
    elif(alc < 11.7):
        poids_alc = 3
    elif(alc < 12.8):
        poids_alc = 4
    elif(alc < 13.9):
        poids_alc = 5
    else:
        poids_alc = 6
    
    note = poids_fixed - poids_volatile + poids_citric + (poids_sugar*2) - poids_chlo + poids_free - poids_total + (poids_pH*2) - poids_sul + poids_alc
    if (note >= 10):
        note = 8
    return note

def get(wine: Wine):
    note_max, alc_max = 0, 0
    taille = len(wine)
    tab_index = []
    wine_best = []
    ind = 0
    for i in range(taille):
        if(wine[i].quality > note_max):
            note_max = wine[i].quality
    for j in range(taille):
        if(wine[j].quality == note_max):
            tab_index.append(j)
    if(len(tab_index) > 1):
        for index in tab_index:
            wine_best.append(wine[index].alcohol)
        for i in range(len(wine_best)):
            if(wine_best[i] > alc_max):
                alc_max = wine_best[i]
        for j in range(len(wine_best)):
            if(wine_best[j] == alc_max):
                ind = j
    else :
        ind = 0
    index = tab_index[ind]
    wine_return = Wine(wine[index].fixed_acidity, wine[index].volatile_acidity, wine[index].citric_acid, wine[index].residual_sugar, wine[index].chlorides, 
    wine[index].free_sulfur_dioxide, wine[index].total_sulfur_dioxide, wine[index].density,wine[index].pH, wine[index].sulphates, wine[index].alcohol, wine[index].quality, 0)
    return wine_return

@router.post("/predict/")
async def read_predict(wine : Wine):
    note = predict(wine.fixed_acidity, wine.volatile_acidity, wine.citric_acid, wine.residual_sugar, wine.chlorides, wine.free_sulfur_dioxide, wine.total_sulfur_dioxide, 
    wine.pH, wine.sulphates, wine.alcohol)
    return {"Note du vin selon les caractéristiques données : ": note}


@router.get("/predict/")
async def read_predict():
    wine_best = get(wine_data)
    return {"Le meilleur vin de la liste a les caractéristiques suivantes : " : wine_best}
