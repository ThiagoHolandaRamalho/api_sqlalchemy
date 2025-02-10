import requests
from pydantic import BaseModel

class PokemonSchame(BaseModel):
    name:str
    type:str

    class Config:
        orm = True


def pegar_pokemon(id:int) -> PokemonSchame:
    payload = f"https://pokeapi.co/api/v2/pokemon/{id}"
    response = requests.get(payload)
    data = response.json()
    data_types =  data.get('types')
    pokemon_tipo =[]
    for tipo in data_types:
        pokemon_tipo.append(tipo.get('type')['name'])
    tipos_str = ','.join(pokemon_tipo)
    
    return PokemonSchame(name = data['name'],type = tipos_str)



if __name__ == '__main__':
    print(pegar_pokemon(1))
    print(pegar_pokemon(20))
    print(pegar_pokemon(32))