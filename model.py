from fastapi import APIRouter
from predict import Wine
import csv
wine_data = []
router = APIRouter()

with open('./data/Wines.csv', 'r') as wine:
    lines = csv.reader(wine, delimiter=",")
    lines2 = list(lines)[1:]
    for line in lines2:
        wine_propre = Wine(*line)
        wine_data.append(wine_propre)

@router.post("/model/retrain/")
async def retrain():
    return {"retrain": "The model has been retrained !!!"}

@router.put("/model/")
async def add_data(data: Wine):
    wine_data.append(data)
    return {"La base de données a été mise à jour en ajoutant : " : data}
