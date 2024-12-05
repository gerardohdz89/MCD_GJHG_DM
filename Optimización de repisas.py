from gurobipy import Model, GRB
import pandas as pd

df = pd.read_csv('C:/Users/gerar/OneDrive - Universidad Autonoma de Nuevo León/Maestría/3er tetramestre/IO/Juegos.csv')

juegos = df['Nombre del juego']  
medida = df['Ancho']  
cantidad = [1]*len(juegos) 
repisas = ["R1","R2","R3"]             
medida_repisas = [20,20,20]

model = Model("Aprovechamiento_de_repisas")

x = model.addVars(juegos, repisas, vtype=GRB.INTEGER, name="x")

model.setObjective(sum(x[i, t] * medida[idx] for idx, i in enumerate(juegos) for t in repisas), GRB.MAXIMIZE)

for t_idx, t in enumerate(repisas):
    model.addConstr(sum(x[i, t] * medida[idx] for idx, i in enumerate(juegos)) <= medida_repisas[t_idx], f"Medida_{t}")

for idx, i in enumerate(juegos):
    model.addConstr(sum(x[i, t] for t in repisas) <= cantidad[idx], f"Disponibilidad_{i}")

model.optimize()

if model.status == GRB.OPTIMAL:
    print("Solución óptima:")
    for t in repisas:
        print(f"\nRepisa {t}:")
        for i in juegos:
            if x[i,t].x > 0:
                print(f"  Acomodar {x[i, t].x:.0f} unidades del juego {i}")
        espacio_utilizado = sum(x[i, t].x * medida[idx] for idx, i in enumerate(juegos)) #for t in repisas)
        print(f"\nEspacio total utilizado: {espacio_utilizado:.2f}")
else:
    print("No se encontró solución óptima.")

