

POKEAPI_ENDPOINTS = {
    # Game related
    "version_groups": "https://pokeapi.co/api/v2/version-group/", # This APi will give us the list of all the version groups in pokemon games. We can use this to get the list of all the pokemon games and their corresponding version groups.
    "version": "https://pokeapi.co/api/v2/version/", # This API will give us the list of all the versions in pokemon games. We can use this to get the list of all the versions and their corresponding version groups.
    "generation": "https://pokeapi.co/api/v2/generation/", # This API will give us the list of all the generations in pokemon games. We can use this to get the list of all the generations and their corresponding version groups.
    "pokedex": "https://pokeapi.co/api/v2/pokedex/", # This API will give us the list of all the pokedexes in pokemon games. We can use this to get the list of all the pokedexes and their corresponding version groups.
    
    # Evolution related
    "evolution-chain": "https://pokeapi.co/api/v2/evolution-chain/", # This API will give us the evolution chain of a pokemon. We can use this to get the evolution chain of a pokemon.
    "evolution-trigger": "https://pokeapi.co/api/v2/evolution-trigger/", # This API will give us the evolution trigger of a pokemon. We can use this to get the evolution trigger of a pokemon.

    # Region
    "region": "https://pokeapi.co/api/v2/region/", # This API will give us the list of all the regions in pokemon games. We can use this to get the list of all the regions and their corresponding version groups.
    "location": "https://pokeapi.co/api/v2/location/", # This API will give us the list of all the locations in pokemon games. We can use this to get the list of all the locations and their corresponding regions.


}

class pokeapi_data_extractor:

     