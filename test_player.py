
from poke_env.player.player import Player
from poke_env.environment.pokemon_type import PokemonType

class TestPlayer(Player):

    def choose_move(self, battle):
        # Print what pokemon is the opponent pokemon
        print(battle.opponent_active_pokemon)

        # Check if player is able to attack
        if battle.available_moves:
            # Find the highest base_power move among available ones
            best_move = self.damage_output(battle.available_moves, battle.opponent_active_pokemon)
            
            print("Selected move has a damage multiplier of: %s" % (PokemonType.damage_multiplier(best_move.type, battle.opponent_active_pokemon.type_1, battle.opponent_active_pokemon.type_2)))
            return self.create_order(best_move)
        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

    def damage_output(available_moves, enemyPokemon):
        best_move = None
        for move in available_moves:
            if best_move == None:
                best_move = move
            elif (PokemonType.damage_multiplier(move.type, enemyPokemon.type_1, enemyPokemon.type_2) * move.base_power) > (PokemonType.damage_multiplier(best_move.type, enemyPokemon.type_1, enemyPokemon.type_2) * move.base_power):
                best_move = move
        return best_move
        

        
        