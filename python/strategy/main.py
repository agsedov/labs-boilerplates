#!/usr/bin/env python3
import argparse
import sys
from common import BotLoader, GameLoader, GameResult

def main():
    parser = argparse.ArgumentParser(description='Game Bot Tournament System')
    parser.add_argument('game', help='Name of the game to play')
    parser.add_argument('--bot1', required=True, help='First bot name')
    parser.add_argument('--bot2', required=True, help='Second bot name')
    parser.add_argument('--matches', type=int, default=1, help='Number of matches to play')
    parser.add_argument('--list-games', action='store_true', help='List available games')
    parser.add_argument('--list-bots', help='List available bots for specified game')

    args = parser.parse_args()

    if args.list_games:
        games = GameLoader.list_available_games()
        print("Available games:")
        for game in games:
            print(f"  - {game}")
        return

    if args.list_bots:
        bots = BotLoader.list_available_bots(args.list_bots)
        print(f"Available bots for {args.list_bots}:")
        for bot in bots:
            print(f"  - {bot}")
        return

    # Load and run the game
    try:
        game = GameLoader.load_game(args.game)
        bot1 = BotLoader.load_bot(args.game, args.bot1, 0)
        bot2 = BotLoader.load_bot(args.game, args.bot2, 1)

        results = run_tournament(game, [bot1, bot2], args.matches)
        print_results(results)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def run_tournament(game, bots, num_matches):
    """Run multiple matches between bots"""
    results = []
    for match in range(num_matches):
        #print("match:", match)
        result = play_match(game, bots)
        results.append(result)
    return results

def play_match(game, bots):
    """Play a single match between bots"""
    game.initialize_game(len(bots))

    total_moves = 0
    while not game.state.game_over:
        current_player = game.state.current_player
        bot = bots[current_player]
        player_state = game.get_player_state(current_player)

        move = bot.make_move(game.state, player_state)

        if total_moves > 100:
            break

        if game.is_valid_move(current_player, move):
            game.apply_move(current_player, move)
            game.check_game_over()
            total_moves += 1
        else:
            # Handle invalid move (penalize or use default)
            print(f"Bot {bot.get_bot_info()['name']} made invalid move: {move}")

    result = GameResult()
    result.winner = game.state.winner
    result.moves_played = len(game.state.history)
    return result

def print_results(results):
    """Print tournament results"""
    wins = [0, 0]
    for result in results:
        if result.winner is not None:
            wins[result.winner] += 1

    print(f"Results after {len(results)} matches:")
    print(f"Bot 1 wins: {wins[0]}")
    print(f"Bot 2 wins: {wins[1]}")
    print(f"Draws: {len(results) - sum(wins)}")

if __name__ == "__main__":
    main()
