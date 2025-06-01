# Connect 4 Minimax and Alpha-Beta (tree on 3 columns)
#
# This script:
# 1. Initializes a partially filled Connect 4 board (3 columns already placed).
# 2. Allows moves on the first 3 columns only:
#    - All players (MAX and MIN): choice among columns [0, 1, 2].
# 3. Traverses the tree at MAX_DEPTH depth with Minimax, displaying:
#    - At each node, its type (Max or Min), its "state" (move path) and possible moves.
#    - The game board at each step.
#    - For each internal node, the list of children values and the chosen value (max or min).
#    - For each leaf (terminal), the evaluation value (win/lose/draw).
# 4. Repeats the same traversal using Alpha-Beta Pruning, displaying:
#    - α and β before exploring each node.
#    - After each child, the α/β updates.
#    - Cutoffs (pruning) when α ≥ β.

import copy

# ============================================================================
# GLOBAL CONFIGURATION
# ============================================================================
MAX_DEPTH = 3  # Maximum depth of the search tree
ROWS = 6       # Board dimensions
COLUMNS = 7

# Creates a partially filled initial board:
# Columns 0, 1, 2 each have some tokens placed:
#   • column 0: (bottom→up) [-1, 1, 1]
#   • column 1: [1, -1, 1]  
#   • column 2: [1, 1, 1]
# Other columns (3, 4, 5, 6) remain empty (0).
#
# We will play only in columns 0, 1, 2 for all players.
# This gives us: 3^MAX_DEPTH potential terminal nodes.
def create_initial_board():
    board = [[0] * COLUMNS for _ in range(ROWS)]
    
    # Column 0 (index 0)
    board[5][0] = -1   # MIN at bottom
    board[4][0] = 1    # MAX
    board[3][0] = 1    # MAX

    # Column 1 (index 1)
    board[5][1] = 1    # MAX at bottom
    board[4][1] = -1   # MIN
    board[3][1] = 1    # MAX

    # Column 2 (index 2)
    board[5][2] = 1    # MAX at bottom
    board[4][2] = 1    # MAX
    board[3][2] = 1    # MAX
    
    board[5][3] = -1    #MIN at bottom

    board[5][5] = -1    # MIN at bottom
    
    board[5][6] = -1    # MIN at bottom
    board[4][6] = -1    # MIN
 

    # Columns 3, 4, 5, 6 remain empty
    return board

# (Optional) Board display function in terminal for debug.
# '.' = empty cell, 'X' = MAX (1), 'O' = MIN (-1).
def print_board(board):
    for row in board:
        print(' '.join(['.' if x == 0 else ('X' if x == 1 else 'O') for x in row]))
    print()

# Checks if a player (1 or -1) has won (4 tokens aligned).
def check_win(board, player):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == player for i in range(4)):
                return True
    # Vertical
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == player for i in range(4)):
                return True
    # Diagonal bottom-right
    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == player for i in range(4)):
                return True
    # Diagonal top-right
    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == player for i in range(4)):
                return True
    return False

# Returns the list of valid columns where we can play,
# limited to the first 3 columns only:
#   • All players (MAX and MIN) can play in columns [0, 1, 2].
#
# We also filter to keep only non-full columns (board[0][c] == 0).
def get_valid_moves(board, depth):
    cols = [0, 1, 2]  # Restriction to first 3 columns

    valid = []
    for c in cols:
        if board[0][c] == 0:
            valid.append(c)
    return valid

# Applies the player's move (1 for MAX, -1 for MIN) in column col.
# new_board is a deep copy of board.
def make_move(board, col, player):
    new_board = copy.deepcopy(board)
    for r in reversed(range(ROWS)):
        if new_board[r][col] == 0:
            new_board[r][col] = player
            break
    return new_board

# Evaluation function at a leaf:
#   +100 if MAX (1) has 4 aligned, -100 if MIN (-1) has 4 aligned, otherwise 0.
def evaluate(board):
    if check_win(board, 1):
        return 100
    if check_win(board, -1):
        return -100
    return 0

# ─────────────────────────────────────────────────────────────────────────────
#  Minimax implementation (max depth = MAX_DEPTH), with complete display.
#  Key element: 
#    • depth = 0 → this is the root node (MAX).
#    • depth = 1 → MIN.
#    • depth = 2 → MAX.
#    • depth = 3 → MIN.
#    • depth = MAX_DEPTH → terminal.
#
#  path is the list of columns played since the root (ex: [2, 1, 3, 0]).
#  state is a string "Root" or "2-1-3-0" that identifies the node.
def minimax(board, depth, path):
    indent = "  " * depth
    state = "Root" if depth == 0 else "-".join(str(x) for x in path)

    # Display board at each node
    print(f"{indent}{'='*50}")
    print(f"{indent}Node [{state}] - Current board:")
    board_lines = []
    for row in board:
        board_lines.append('  ' + indent + ' '.join(['.' if x == 0 else ('X' if x == 1 else 'O') for x in row]))
    for line in board_lines:
        print(line)
    print(f"{indent}{'='*50}")

    # If position is winning or we reach max depth → leaf
    score_win = evaluate(board)
    if depth == MAX_DEPTH or score_win != 0:
        # Leaf: display its evaluation
        print(f"{indent}Terminal [{state}], eval = {score_win}")
        return score_win

    if depth % 2 == 0:
        # MAX
        moves = get_valid_moves(board, depth)
        print(f"{indent}Max Node [{state}], moves = {moves}")
        best_val = float("-inf")
        children_vals = []
        for m in moves:
            child = make_move(board, m, 1)  # MAX plays = +1
            val = minimax(child, depth + 1, path + [m])
            children_vals.append(val)
            if val > best_val:
                best_val = val
        print(f"{indent}Max Node [{state}] children values = {children_vals}, chosen = {best_val}")
        return best_val

    else:
        # MIN
        moves = get_valid_moves(board, depth)
        print(f"{indent}Min Node [{state}], moves = {moves}")
        best_val = float("inf")
        children_vals = []
        for m in moves:
            child = make_move(board, m, -1)  # MIN plays = -1
            val = minimax(child, depth + 1, path + [m])
            children_vals.append(val)
            if val < best_val:
                best_val = val
        print(f"{indent}Min Node [{state}] children values = {children_vals}, chosen = {best_val}")
        return best_val

# ─────────────────────────────────────────────────────────────────────────────
#  Alpha-Beta implementation (same rules, same depth), with display.
#  We pass α and β to each node, and print:
#    • Before exploring a node: (α, β).
#    • After evaluating each child: α/β updates.
#    • If α ≥ β: we get a prune (cut remaining children).
def alphabeta(board, depth, path, alpha, beta):
    indent = "  " * depth
    state = "Root" if depth == 0 else "-".join(str(x) for x in path)

    # Display board at each node
    print(f"{indent}{'='*50}")
    print(f"{indent}Node [{state}] - Current board:")
    board_lines = []
    for row in board:
        board_lines.append('  ' + indent + ' '.join(['.' if x == 0 else ('X' if x == 1 else 'O') for x in row]))
    for line in board_lines:
        print(line)
    print(f"{indent}{'='*50}")

    score_win = evaluate(board)
    if depth == MAX_DEPTH or score_win != 0:
        print(f"{indent}Terminal [{state}], eval = {score_win}")
        return score_win

    if depth % 2 == 0:
        # MAX
        moves = get_valid_moves(board, depth)
        print(f"{indent}Max Node [{state}] (α={alpha}, β={beta}), moves = {moves}")
        value = float("-inf")
        for m in moves:
            child = make_move(board, m, 1)
            val = alphabeta(child, depth + 1, path + [m], alpha, beta)
            if val > value:
                value = val
            if value > alpha:
                alpha = value
            print(f"{indent}  After child {m}, Max Node [{state}] sees value = {value}, α={alpha}, β={beta}")
            if alpha >= beta:
                print(f"{indent}  Prune at Max Node [{state}] (α={alpha} ≥ β={beta})")
                break
        print(f"{indent}Max Node [{state}] returns {value}")
        return value

    else:
        # MIN
        moves = get_valid_moves(board, depth)
        print(f"{indent}Min Node [{state}] (α={alpha}, β={beta}), moves = {moves}")
        value = float("inf")
        for m in moves:
            child = make_move(board, m, -1)
            val = alphabeta(child, depth + 1, path + [m], alpha, beta)
            if val < value:
                value = val
            if value < beta:
                beta = value
            print(f"{indent}  After child {m}, Min Node [{state}] sees value = {value}, α={alpha}, β={beta}")
            if alpha >= beta:
                print(f"{indent}  Prune at Min Node [{state}] (α={alpha} ≥ β={beta})")
                break
        print(f"{indent}Min Node [{state}] returns {value}")
        return value

# ─────────────────────────────────────────────────────────────────────────────
# Functions to collect and draw the tree with all terminal states
# ─────────────────────────────────────────────────────────────────────────────

def collect_tree_nodes(board, depth, path, node_type="minimax"):
    """Collects all tree nodes and their values for final drawing"""
    nodes = []
    state = "Root" if depth == 0 else "-".join(str(x) for x in path)
    
    # Node evaluation
    score_win = evaluate(board)
    if depth == MAX_DEPTH or score_win != 0:
        # Terminal node
        nodes.append({
            'path': path.copy(),
            'state': state,
            'value': score_win,
            'type': 'terminal',
            'depth': depth
        })
        return nodes, score_win
    
    # Internal node
    if depth % 2 == 0:  # MAX
        moves = get_valid_moves(board, depth)
        best_val = float("-inf")
        children_vals = []
        for m in moves:
            child = make_move(board, m, 1)
            child_nodes, val = collect_tree_nodes(child, depth + 1, path + [m], node_type)
            nodes.extend(child_nodes)
            children_vals.append(val)
            if val > best_val:
                best_val = val
        
        nodes.append({
            'path': path.copy(),
            'state': state,
            'value': best_val,
            'type': 'max',
            'depth': depth,
            'children_values': children_vals,
            'moves': moves
        })
        return nodes, best_val
    else:  # MIN
        moves = get_valid_moves(board, depth)
        best_val = float("inf")
        children_vals = []
        for m in moves:
            child = make_move(board, m, -1)
            child_nodes, val = collect_tree_nodes(child, depth + 1, path + [m], node_type)
            nodes.extend(child_nodes)
            children_vals.append(val)
            if val < best_val:
                best_val = val
        
        nodes.append({
            'path': path.copy(),
            'state': state,
            'value': best_val,
            'type': 'min',
            'depth': depth,
            'children_values': children_vals,
            'moves': moves
        })
        return nodes, best_val

def collect_alphabeta_tree_nodes(board, depth, path, alpha, beta):
    """Collects nodes for Alpha-Beta with pruning information"""
    nodes = []
    state = "Root" if depth == 0 else "-".join(str(x) for x in path)
    
    score_win = evaluate(board)
    if depth == MAX_DEPTH or score_win != 0:
        nodes.append({
            'path': path.copy(),
            'state': state,
            'value': score_win,
            'type': 'terminal',
            'depth': depth,
            'alpha': alpha,
            'beta': beta
        })
        return nodes, score_win
    
    if depth % 2 == 0:  # MAX
        moves = get_valid_moves(board, depth)
        value = float("-inf")
        children_vals = []
        pruned = False
        explored_moves = []
        
        for m in moves:
            child = make_move(board, m, 1)
            child_nodes, val = collect_alphabeta_tree_nodes(child, depth + 1, path + [m], alpha, beta)
            nodes.extend(child_nodes)
            children_vals.append(val)
            explored_moves.append(m)
            if val > value:
                value = val
            if value > alpha:
                alpha = value
            if alpha >= beta:
                pruned = True
                break
        
        nodes.append({
            'path': path.copy(),
            'state': state,
            'value': value,
            'type': 'max',
            'depth': depth,
            'children_values': children_vals,
            'moves': moves,
            'explored_moves': explored_moves,
            'pruned': pruned,
            'alpha': alpha,
            'beta': beta
        })
        return nodes, value
    else:  # MIN
        moves = get_valid_moves(board, depth)
        value = float("inf")
        children_vals = []
        pruned = False
        explored_moves = []
        
        for m in moves:
            child = make_move(board, m, -1)
            child_nodes, val = collect_alphabeta_tree_nodes(child, depth + 1, path + [m], alpha, beta)
            nodes.extend(child_nodes)
            children_vals.append(val)
            explored_moves.append(m)
            if val < value:
                value = val
            if value < beta:
                beta = value
            if alpha >= beta:
                pruned = True
                break
        
        nodes.append({
            'path': path.copy(),
            'state': state,
            'value': value,
            'type': 'min',
            'depth': depth,
            'children_values': children_vals,
            'moves': moves,
            'explored_moves': explored_moves,
            'pruned': pruned,
            'alpha': alpha,
            'beta': beta
        })
        return nodes, value

def draw_tree(nodes, title="Game Tree"):
    """Draws the game tree with all nodes and terminal states"""
    print(f"\n{'='*80}")
    print(f"{title:^80}")
    print(f"{'='*80}")
    
    # Separate nodes by level
    levels = {}
    for node in nodes:
        depth = node['depth']
        if depth not in levels:
            levels[depth] = []
        levels[depth].append(node)
    
    # Draw level by level
    for depth in sorted(levels.keys()):
        print(f"\nLevel {depth} ({'MAX' if depth % 2 == 0 else 'MIN'}):")
        print("-" * 60)
        
        for node in levels[depth]:
            state = node['state']
            value = node['value']
            node_type = node['type']
            
            if node_type == 'terminal':
                print(f"  Terminal [{state}] = {value}")
            else:
                children_vals = node.get('children_values', [])
                moves = node.get('moves', [])
                
                if 'pruned' in node:  # Alpha-Beta
                    alpha = node.get('alpha', 'N/A')
                    beta = node.get('beta', 'N/A')
                    explored = node.get('explored_moves', [])
                    pruned = node.get('pruned', False)
                    
                    print(f"  {node_type.upper()} [{state}] (α={alpha}, β={beta}) = {value}")
                    print(f"    Possible moves: {moves}")
                    print(f"    Explored moves: {explored}")
                    print(f"    Children values: {children_vals}")
                    if pruned:
                        print(f"    >>> PRUNING PERFORMED <<<")
                else:  # Minimax
                    print(f"  {node_type.upper()} [{state}] = {value}")
                    print(f"    Moves: {moves}")
                    print(f"    Children values: {children_vals}")
        print()

def draw_terminal_states_summary(nodes):
    """Summary of all terminal states"""
    print(f"\n{'='*80}")
    print(f"{'TERMINAL STATES SUMMARY':^80}")
    print(f"{'='*80}")
    
    terminals = [node for node in nodes if node['type'] == 'terminal']
    
    # Group by value
    by_value = {}
    for terminal in terminals:
        value = terminal['value']
        if value not in by_value:
            by_value[value] = []
        by_value[value].append(terminal)
    
    print(f"Total terminal states: {len(terminals)}")
    print()
    
    for value in sorted(by_value.keys(), reverse=True):
        states = by_value[value]
        count = len(states)
        interpretation = "MAX wins" if value > 0 else "MIN wins" if value < 0 else "Draw"
        
        print(f"Value {value} ({interpretation}): {count} states")
        for state in states:
            print(f"  - Path: {state['state'] if state['state'] != 'Root' else 'Root'}")
        print()

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 1) Create initial board
    board0 = create_initial_board()

    print(f"\n=== CONFIGURATION ===")
    print(f"Maximum depth: {MAX_DEPTH}")
    print(f"Board dimensions: {ROWS}x{COLUMNS}")
    print(f"Allowed columns: [0, 1, 2]")
    print(f"=====================\n")

    print("\nInitial board (X = MAX, O = MIN):\n")
    print_board(board0)

    # 2) Execute Minimax
    print(f"\n--- Running Minimax (depth {MAX_DEPTH}) ---\n")
    minimax_value = minimax(board0, 0, [])
    print(f"\nMinimax root decision value: {minimax_value}\n")

    # 3) Execute Alpha-Beta Pruning
    print(f"\n--- Running Alpha-Beta Pruning (depth {MAX_DEPTH}) ---\n")
    alphabeta_value = alphabeta(board0, 0, [], float("-inf"), float("inf"))
    print(f"\nAlpha-Beta root decision value: {alphabeta_value}\n")

    # 4) Collect and draw complete trees
    print("\n--- Collecting data for trees ---\n")
    
    # Complete Minimax tree
    minimax_nodes, _ = collect_tree_nodes(board0, 0, [])
    draw_tree(minimax_nodes, f"COMPLETE MINIMAX TREE (DEPTH {MAX_DEPTH})")
    draw_terminal_states_summary(minimax_nodes)
    
    # Complete Alpha-Beta tree
    alphabeta_nodes, _ = collect_alphabeta_tree_nodes(board0, 0, [], float("-inf"), float("inf"))
    draw_tree(alphabeta_nodes, f"ALPHA-BETA TREE WITH PRUNING (DEPTH {MAX_DEPTH})")
    draw_terminal_states_summary(alphabeta_nodes)
    
    print(f"\n{'='*80}")
    print(f"FINAL COMPARISON (DEPTH {MAX_DEPTH})")
    print(f"{'='*80}")
    print(f"Minimax value: {minimax_value}")
    print(f"Alpha-Beta value: {alphabeta_value}")
    print(f"Minimax terminal states: {len([n for n in minimax_nodes if n['type'] == 'terminal'])}")
    print(f"Alpha-Beta terminal states: {len([n for n in alphabeta_nodes if n['type'] == 'terminal'])}")
    
    # Count pruned nodes
    pruned_nodes = len([n for n in alphabeta_nodes if n.get('pruned', False)])
    print(f"Nodes with pruning: {pruned_nodes}")
    print(f"Theoretical terminal nodes: {3**MAX_DEPTH}")
    print(f"{'='*80}")
