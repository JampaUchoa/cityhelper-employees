from typing import Optional

from fastapi import FastAPI
import requests
import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "working"}


@app.post("/solicitar-servico")
def read_root(latitude: float, longitude: float):
    # Procura por processos abertos
    r = requests.get('http://localhost:8000/api/solicitation/?processo_situacao=aberto')
    # Define prioridade por data de processo
    open_solicitations = r.json()["results"]
    if (len(open_solicitations) == 0):
        return {"message": "NO_SOLICITATION"}
    print(open_solicitations)
    highest_priority = None
    highest_priority_score = None

    for sol in open_solicitations:
        if not highest_priority:
            highest_priority = sol
            highest_priority_score = calculate_priority(latitude, longitude, sol)
        else:
            score = calculate_priority(latitude, longitude, sol)
            if score > highest_priority_score:
                highest_priority = sol
                highest_priority_score = score
    
    # Envia para o backend que usuario vai fazer o serviço
    r = requests.patch(f'http://localhost:8000/api/solicitation/{highest_priority["id"]}/', data = {'processo_situacao':'execucao'})
    # Retorna servico a ser feito
    return highest_priority

@app.post("/cancelar-servico")
def read_root(servico_id: int):
    pass

@app.post("/concluir-servico")
def read_root(servico_id: int):
    # ENVIAR ORDEM DE SERVICO CONCLUIDA
    r = requests.patch(f'http://localhost:8000/api/solicitation/{servico_id}/', data = {'processo_situacao':'concluido', 'processo_data_conclusao': str(datetime.datetime.now())})
    print(r.json())

    return {"success": True}


def calculate_priority(lat, lon, sol):

    # Quanto mais perto mais prioridade
    score_distance = 2 / distance_harversine(lat, lon, sol['latitude'], sol['longitude'])
    # Quanto mais dias passarem maior a prioridade
    score_time = 0
    if sol['solicitacao_data']:
        sol_data = sol['solicitacao_data']
        sol_data = datetime.datetime.strptime(sol_data, '%Y-%m-%dT%H:%M:%S.%f')
        time_delta = datetime.datetime.now() - sol_data
        score_time = time_delta.total_seconds() / (3600 * 24)
    
    return score_distance + score_time

def distance_harversine(lat1, lon1, lat2, lon2):
    from math import sin, cos, sqrt, atan2, radians

    # radius of earth in kilometers
    R = 6373.0

    lat1 = radians(52.2296756)
    lon1 = radians(21.0122287)
    lat2 = radians(52.406374)
    lon2 = radians(16.9251681)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# GET WORK
# GET AVAILABLE TODO


# MARK WORK AS COMPLETED
