# -*- coding: utf-8 -*-
import asyncio
import time

from poke_env.player.player import Player
from poke_env.player.random_player import RandomPlayer
from poke_env.environment.pokemon_type import PokemonType
from poke_env.player.utils import cross_evaluate
from tabulate import tabulate
from smarter_player import SmarterGuy

class MaxDamagePlayer(Player):
    
    def choose_move(self, battle):
        # If the player is able to attack, attack
        if battle.available_moves:
            # Find the highest base_power move among available ones
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)
        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)

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

    def damage_output(self, available_moves, enemyPokemon):
        best_move = None
        for move in available_moves:
            if best_move == None:
                best_move = move
            elif (PokemonType.damage_multiplier(move.type, enemyPokemon.type_1, enemyPokemon.type_2) * move.base_power) > (PokemonType.damage_multiplier(best_move.type, enemyPokemon.type_1, enemyPokemon.type_2) * move.base_power):
                best_move = move
        return best_move

async def main():
    start = time.time()

    # Create players.
    random_player = RandomPlayer(
    battle_format="gen8randombattle"
    )
    max_damage_player = MaxDamagePlayer(
        battle_format="gen8randombattle"
    )
    test_player = TestPlayer(
        battle_format="gen8randombattle"
    )
    smarter_player = SmarterGuy(
        battle_format="gen8randombattle"
    )

    # await smarter_player.battle_against(max_damage_player, n_battles=1)
    # print(
    #     "Max damage player won %d / 100 battles against random player [this took %f seconds]"
    #     % (
    #         smarter_player.n_won_battles, time.time() - start
    #     )
    # )

    players = [max_damage_player, test_player, smarter_player]

    cross_evaluation = await cross_evaluate(players, n_challenges=500)
    
    table = [["-"] + [p.username for p in players]]

    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])

    print(tabulate(table))

    test_player = TestPlayer(
        battle_format="gen8randombattle"
    )
    
    # await test_player.accept_challenges(None,1)
    # print()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())