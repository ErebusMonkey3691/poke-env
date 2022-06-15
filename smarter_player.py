
from math import trunc

from libcst import List
from poke_env.environment.pokemon import Pokemon
from poke_env.player.player import Player
from poke_env.environment.pokemon_type import PokemonType

class SmarterGuy(Player):

    def choose_move(self, battle):
        print(battle.opponent_active_pokemon) # Print what pokemon is the opponent pokemon

        # Check if player is able to attack
        if battle.available_moves:
            # Check if can KO -- Block below
            for move in battle.available_moves:
                if self.damage_calc(move, battle.opponent_active_pokemon, battle.active_pokemon) >= self.hpCalc(battle.opponent_active_pokemon):
                    # Use KO move
                    return self.create_order(move)
            # Check for super effective moves
            move_options = []
            for move in battle.available_moves: # Cycle through each move available
                if PokemonType.damage_multiplier(move.type, battle.opponent_active_pokemon.type_1, battle.opponent_active_pokemon.type_2) > 1: # If move is super effective (multiplier > 1)
                    move_options.append(move) # Add move to move options list
            # Check if any super effective moves were found
            if move_options != []: # If so, continue to check for STAB
                return self.create_order(self.stab_check(battle.active_pokemon, move_options)) # STAB check, returning a viable move
            else: # If not, check for neutral moves
                for move in battle.available_moves: # Cycle through each move
                    move_options = []
                    if PokemonType.damage_multiplier(move.type, battle.opponent_active_pokemon.type_1, battle.opponent_active_pokemon.type_2) == 1: # If move is neutral (multiplier = 1)
                        move_options.append(move)
                if move_options != []: # If there is a neutral move
                    return self.create_order(self.stab_check(battle.active_pokemon, move_options)) # STAB check, returning a viable move
                else: # If not any neutral moves
                    print("No neutral moves. Swap module called but needs to be implemented")
                    # TEMPORARY TO FILL IN THE MISSING NEUTRAL MOVE SECTION
                    best_move = max(battle.available_moves, key=lambda move: move.base_power) # Find highest base power move
                    return self.create_order(best_move) # Use the found move

            # Find the highest base_power move among available ones
            # # # # # best_move = self.damage_output(battle.available_moves, battle.opponent_active_pokemon)
            # Debug output, testing that damage multiplier works.
            # print("Selected move has a damage multiplier of: %s" % (PokemonType.damage_multiplier(best_move.type, battle.opponent_active_pokemon.type_1, battle.opponent_active_pokemon.type_2)))
            # Use the best move found
            # # # # # return self.create_order(best_move)
        # If no attack is available, a random switch will be made
        else: # If the player is unable to attack
            return self.choose_random_move(battle)

    def stab_check(self, pokemon: Pokemon, moves): # Pokemon: the pokemon using the moves, moves: the moves to check through -> Returns a move ## Will not check for multiple STAB moves, will only choose the first one found.
        for move in moves: # Cycle through each move
            # Check if stab
            if move.type == pokemon.type_1 or move.type == pokemon.type_2:
                return move # Return move if it is stab
        # Broken from for loop, so there are no stab moves.
        # Use the strongest move from the list
        best_move = max(moves, key=lambda move : move.base_power) # Doesn't account for effectiveness in this calculation, just base power. <- should be fine as it's used in effectiveness brackets (only exception is 4x effectiveness)
        return best_move

    def damage_output(available_moves, enemyPokemon):
        best_move = None
        for move in available_moves:
            if best_move == None:
                best_move = move
            elif (PokemonType.damage_multiplier(move.type, enemyPokemon.type_1, enemyPokemon.type_2) * move.base_power) > (PokemonType.damage_multiplier(best_move.type, enemyPokemon.type_1, enemyPokemon.type_2) * move.base_power):
                best_move = move
        return best_move

    def hpCalc(self, pokemon): # Estimates opponents max HP.
        hp_base = pokemon.base_stats['hp']
        hp_estimate = ((2 * hp_base + 31) * pokemon.level) / 100 + pokemon.level + 10 # Doesn't currently account for EVs (assuming enemy has no EVs in this calc.)
        return hp_estimate

    def damage_calc(self, move, target_pokemon, current_mon): ## Theory: is currently grabbing actual stats and so the enemies stats return as None as they are not known to us.
        damage = trunc(2 * target_pokemon.level / 5) + 2      ## Make it so we estimate the enemies stats with base stats, currently not accounting for EVs.

        attack = 1
        defence = 1
        #print(current_mon.stats)
        #print(target_pokemon.stats)
        if move.category == 1:
            # order [hp, atk, def, spa, spd, spe] for Pokemon.stats list
            attack = current_mon.stats['atk'] 
            defence = self.defence_estimate(target_pokemon.base_stats['def'], target_pokemon)
        else:
            attack = current_mon.stats['spa']
            defence = self.defence_estimate(target_pokemon.base_stats['spd'], target_pokemon)
        stab = 1
        burn = 1
        if move.category == 1 and current_mon.status == 1:
            burn = 0.5
        if current_mon.type_1 == move.type or current_mon.type_2 == move.type:
            stab = 1.5
        #print(f"Damage: {damage}/n Move: {move}/n Attack: {attack}/n Defence: {defence}")
        damage = trunc(damage * move.base_power * attack / defence) 
        damage = trunc(damage / 50) + 2
        damage = trunc(damage * 0.85) # accounting for the random roll on damage, assuming a low roll
        damage = trunc(damage * stab) 
        damage = trunc(damage * PokemonType.damage_multiplier(move.type, target_pokemon.type_1, target_pokemon.type_2)) # Type bonus
        damage = trunc(damage * burn)
        return damage
        # Damage calculation only accounts for:
        #   - STAB
        #   - Type effectiveness
        #   - Burn for physical type moves
        #   - Low roll of random element
        # Damage calc. doesn't currently account for:
        #   - Critical hits
        #   - Weather bonues'
        #   - PB
        #   - Multiple targets (no effect currently as it's singles)
        #   - Other damage modifiers (such as items)
        #   - Z-Move bonus
    
    def defence_estimate(self, baseDef, pokemon): # Returns an estimate of the pokemons defence. Passed the base stat for the effective defence stat.
        # Does not account for EVs or Nature. Assumes perfect IVs and 0 EVs invested.
        defence = (2 * baseDef + 31) * pokemon.level
        defence = trunc(defence / 100) + 5
        # defence = trunc(defence * nature) <- when nature wants to be accounted for
        return defence
