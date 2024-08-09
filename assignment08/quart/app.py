from quart import Quart
from quart import render_template

from pypokemon.pokemon import Pokemon
import asyncio
import httpx
import time
import random

app = Quart(__name__)

async def get_pokemon(client, url):
    print(f"{time.ctime()} - get {url}")
    resp = await client.get(url)
    pokemon = resp.json()
    return pokemon


async def get_pokemons():
    async with httpx.AsyncClient() as client:
        rand_list = [random.randint(1, 151) for _ in range(20)]
    async with httpx.AsyncClient() as client:
        tasks = [get_pokemon(client, f'https://pokeapi.co/api/v2/pokemon/{number}') for number in rand_list]
        pokemons_json = await asyncio.gather(*tasks)

    pokemons = [Pokemon(pokemon_json) for pokemon_json in pokemons_json]
    return pokemons




@app.route('/')
async def index():
    start_time = time.perf_counter()
    pokemons = await get_pokemons()
    end_time = time.perf_counter()
    print(f"{time.ctime()} - Asynchronously get {len(pokemons)} pokemons. Time taken: {end_time-start_time} seconds")
    return await render_template('index.html', pokemons=pokemons, end_time=end_time, start_time=start_time)


if __name__ == '__main__':
    app.run(debug=True, port=50002)