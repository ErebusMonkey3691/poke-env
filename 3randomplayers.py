# -*- coding: utf-8 -*-
import asyncio
from poke_env.player.random_player import RandomPlayer
from poke_env.player.utils import cross_evaluate
from tabulate import tabulate

async def main():
    # Create three random players
    players = [
        RandomPlayer(max_concurrent_battles=10) for _ in range(3)
    ]
    cross_evaluation = await cross_evaluate(players, n_challenges=20)
    # Tabulating
    # Defines a header for displaying the results
    table = [["-"] + [p.username for p in players]]

    # Adds one line per player with corresponding results
    for p_1, results in cross_evaluation.items():
        table.append([p_1] + [cross_evaluation[p_1][p_2] for p_2 in results])

    # Displays results in a nicely formatted table.
    print(tabulate(table))

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())



    