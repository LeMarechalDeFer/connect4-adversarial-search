# Connect 4 Adversarial Search

An intelligent Connect 4 agent powered by Minimax and Alpha-Beta pruning algorithms. This project implements adversarial search techniques and decision tree evaluation to demonstrate strategic gameplay and optimization through pruning.

## 🎯 Overview

This project provides a comprehensive educational implementation of game theory algorithms applied to Connect 4. It demonstrates the difference between exhaustive Minimax search and optimized Alpha-Beta pruning, showing detailed decision trees and terminal state analysis.

## 🚀 Features

- **Minimax Algorithm**: Complete implementation with full tree exploration
- **Alpha-Beta Pruning**: Optimized search with branch elimination
- **Detailed Visualization**: Step-by-step algorithm execution display
- **Tree Analysis**: Complete decision tree visualization and terminal state summaries
- **Performance Comparison**: Side-by-side analysis of both algorithms
- **Educational Output**: Comprehensive logging of algorithm decisions and pruning actions

## 🎮 Game Configuration

### Board Setup
- **Dimensions**: 6 rows × 7 columns (standard Connect 4)
- **Initial State**: Partially filled board with predetermined pieces
- **Restricted Play**: Limited to first 3 columns only (columns 0, 1, 2)
- **Search Depth**: Configurable (default: 3 levels)

### Players
- **MAX Player (X)**: Maximizing player (value +1)
- **MIN Player (O)**: Minimizing player (value -1)
- **Alternating Turns**: MAX starts, then MIN, then MAX, etc.

## 🧠 Algorithms

### Minimax Algorithm
- **Complete Search**: Explores all possible game states
- **Recursive Evaluation**: Evaluates all terminal nodes
- **Perfect Play**: Assumes both players play optimally
- **Value Propagation**: Propagates values up the tree (max/min selection)

### Alpha-Beta Pruning
- **Optimized Search**: Eliminates unnecessary branches
- **Alpha-Beta Windows**: Maintains search bounds
- **Pruning Detection**: Cuts branches when α ≥ β
- **Same Result**: Guarantees identical outcome to Minimax with fewer evaluations

## 📊 Output Analysis

### Detailed Logging
- Board state at each decision node
- Available moves and chosen actions
- Value propagation through the tree
- Alpha-Beta bounds and pruning points

### Tree Visualization
- Complete decision trees for both algorithms
- Terminal state summaries
- Performance metrics comparison
- Pruning efficiency analysis

### Performance Metrics
- Number of terminal states evaluated
- Pruning effectiveness
- Algorithm execution comparison
- Theoretical vs. actual node exploration

## 🛠 Installation & Usage

### Prerequisites
```bash
python 3.11+
```

### Running the Program
```bash
python connect4.py
```

### Configuration
Modify the global configuration in `connect4.py`:
```python
MAX_DEPTH = 3    # Search depth
ROWS = 6         # Board rows
COLUMNS = 7      # Board columns
```

## 📚 Code Structure

### Core Functions

#### Game Logic
- `create_initial_board()`: Sets up the initial game state
- `check_win()`: Detects winning conditions (4 in a row)
- `get_valid_moves()`: Returns available columns for play
- `make_move()`: Applies a move to the board
- `evaluate()`: Scores terminal positions

#### Search Algorithms
- `minimax()`: Implements standard Minimax algorithm
- `alphabeta()`: Implements Alpha-Beta pruning variant
- Both functions include comprehensive logging and visualization

#### Analysis Tools
- `collect_tree_nodes()`: Gathers complete tree data for Minimax
- `collect_alphabeta_tree_nodes()`: Gathers tree data with pruning info
- `draw_tree()`: Visualizes complete decision trees
- `draw_terminal_states_summary()`: Analyzes terminal positions

## 🎓 Educational Value

### Game Theory Concepts
- **Adversarial Search**: Two-player zero-sum games
- **Minimax Theorem**: Optimal play in competitive scenarios
- **Alpha-Beta Optimization**: Pruning for efficiency

### Algorithm Analysis
- **Time Complexity**: O(b^d) for Minimax, optimized with Alpha-Beta
- **Space Complexity**: O(d) for recursive depth
- **Pruning Efficiency**: Demonstrates search space reduction

### Learning Outcomes
- Understanding adversarial search algorithms
- Comparing algorithmic optimizations
- Analyzing decision tree structures
- Evaluating algorithm performance

