"""
History module for storing and analyzing chess and xiangqi game history.
"""

import json
import os
import datetime
from typing import Dict, List, Optional, Any, Union


class GameHistory:
    """Class to represent a single game's history, including moves, metadata, and analysis."""
    
    def __init__(
        self, 
        game_id: str,
        game_type: str,
        players: Dict[str, str],
        moves: List[str],
        result: str,
        timestamp: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a game history object.
        
        Args:
            game_id: Unique identifier for the game
            game_type: Type of game ('chess' or 'xiangqi')
            players: Dictionary with player info (e.g., {'white': 'player1', 'black': 'player2'})
            moves: List of moves in standard notation
            result: Game result (e.g., '1-0', '0-1', '1/2-1/2')
            timestamp: When the game was played (ISO format)
            metadata: Additional game information
        """
        self.game_id = game_id
        self.game_type = game_type
        self.players = players
        self.moves = moves
        self.result = result
        self.timestamp = timestamp or datetime.datetime.now().isoformat()
        self.metadata = metadata or {}
        self.analysis = {}
    
    def add_analysis(self, analysis_type: str, data: Any) -> None:
        """Add analysis data to the game history."""
        self.analysis[analysis_type] = data
    
    def get_move_count(self) -> int:
        """Get the total number of moves in the game."""
        return len(self.moves)
    
    def get_game_duration(self) -> int:
        """Get the game duration in number of plies."""
        return len(self.moves)
    
    def get_winner(self) -> Optional[str]:
        """Get the winner of the game if any."""
        if self.result == '1-0':
            return self.players.get('white', 'Player 1')
        elif self.result == '0-1':
            return self.players.get('black', 'Player 2')
        else:
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert game history to dictionary."""
        return {
            'game_id': self.game_id,
            'game_type': self.game_type,
            'players': self.players,
            'moves': self.moves,
            'result': self.result,
            'timestamp': self.timestamp,
            'metadata': self.metadata,
            'analysis': self.analysis
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameHistory':
        """Create a GameHistory object from a dictionary."""
        game = cls(
            game_id=data['game_id'],
            game_type=data['game_type'],
            players=data['players'],
            moves=data['moves'],
            result=data['result'],
            timestamp=data['timestamp'],
            metadata=data.get('metadata', {})
        )
        game.analysis = data.get('analysis', {})
        return game


class HistoryManager:
    """Class to manage game histories, including storage, retrieval, and analysis."""
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize the history manager.
        
        Args:
            storage_dir: Directory where game histories are stored
        """
        self.storage_dir = storage_dir or os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Cached game histories
        self.games: Dict[str, GameHistory] = {}
    
    def add_game(self, game: GameHistory) -> str:
        """
        Add a game to the history manager.
        
        Args:
            game: The GameHistory object to add
            
        Returns:
            The ID of the added game
        """
        self.games[game.game_id] = game
        self._save_game(game)
        return game.game_id
    
    def get_game(self, game_id: str) -> Optional[GameHistory]:
        """
        Get a game by ID.
        
        Args:
            game_id: The ID of the game to retrieve
            
        Returns:
            The GameHistory object if found, None otherwise
        """
        # Check cache first
        if game_id in self.games:
            return self.games[game_id]
        
        # Try to load from storage
        filepath = os.path.join(self.storage_dir, f"{game_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                game_data = json.load(f)
            game = GameHistory.from_dict(game_data)
            self.games[game_id] = game
            return game
        
        return None
    
    def delete_game(self, game_id: str) -> bool:
        """
        Delete a game by ID.
        
        Args:
            game_id: The ID of the game to delete
            
        Returns:
            True if the game was deleted, False otherwise
        """
        if game_id in self.games:
            del self.games[game_id]
        
        filepath = os.path.join(self.storage_dir, f"{game_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    def list_games(self, game_type: Optional[str] = None) -> List[str]:
        """
        List all game IDs, optionally filtered by type.
        
        Args:
            game_type: If provided, only games of this type will be returned
            
        Returns:
            List of game IDs
        """
        game_ids = []
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                game_id = filename.replace('.json', '')
                game = self.get_game(game_id)
                if game and (game_type is None or game.game_type == game_type):
                    game_ids.append(game_id)
        return game_ids
    
    def _save_game(self, game: GameHistory) -> None:
        """
        Save a game to storage.
        
        Args:
            game: The GameHistory object to save
        """
        filepath = os.path.join(self.storage_dir, f"{game.game_id}.json")
        with open(filepath, 'w') as f:
            json.dump(game.to_dict(), f, indent=2)
    
    def analyze_game_statistics(self, game_id: str) -> Dict[str, Any]:
        """
        Analyze game statistics.
        
        Args:
            game_id: The ID of the game to analyze
            
        Returns:
            Dictionary with analysis results
        """
        game = self.get_game(game_id)
        if not game:
            return {'error': 'Game not found'}
        
        analysis = {
            'move_count': game.get_move_count(),
            'duration': game.get_game_duration(),
            'winner': game.get_winner(),
            'game_type': game.game_type
        }
        
        # Add the analysis to the game
        game.add_analysis('basic_statistics', analysis)
        self._save_game(game)
        
        return analysis
    
    def search_games(self, criteria: Dict[str, Any]) -> List[str]:
        """
        Search games by various criteria.
        
        Args:
            criteria: Dictionary with search criteria
            
        Returns:
            List of matching game IDs
        """
        matching_ids = []
        
        for game_id in self.list_games():
            game = self.get_game(game_id)
            if not game:
                continue
            
            match = True
            for key, value in criteria.items():
                if key == 'player':
                    # Special case: search for player in any position
                    player_found = False
                    for player_pos, player_name in game.players.items():
                        if value.lower() in player_name.lower():
                            player_found = True
                            break
                    if not player_found:
                        match = False
                        break
                elif key == 'result':
                    if game.result != value:
                        match = False
                        break
                elif key == 'game_type':
                    if game.game_type != value:
                        match = False
                        break
                elif key == 'date_after':
                    game_date = datetime.datetime.fromisoformat(game.timestamp)
                    if game_date < datetime.datetime.fromisoformat(value):
                        match = False
                        break
                elif key == 'date_before':
                    game_date = datetime.datetime.fromisoformat(game.timestamp)
                    if game_date > datetime.datetime.fromisoformat(value):
                        match = False
                        break
            
            if match:
                matching_ids.append(game_id)
        
        return matching_ids
    
    def export_games(self, game_ids: List[str], export_format: str = 'json') -> str:
        """
        Export games to a specific format.
        
        Args:
            game_ids: List of game IDs to export
            export_format: Format to export to ('json' or 'pgn')
            
        Returns:
            Path to the exported file
        """
        games_data = [self.get_game(game_id).to_dict() for game_id in game_ids if self.get_game(game_id)]
        
        if export_format == 'json':
            export_path = os.path.join(self.storage_dir, f"export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(export_path, 'w') as f:
                json.dump(games_data, f, indent=2)
            return export_path
        
        elif export_format == 'pgn':
            # Simple PGN export for chess games
            export_path = os.path.join(self.storage_dir, f"export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pgn")
            with open(export_path, 'w') as f:
                for game_data in games_data:
                    if game_data['game_type'] != 'chess':
                        continue  # Skip non-chess games for PGN export
                    
                    # Write PGN headers
                    f.write(f'[Event "{game_data["metadata"].get("event", "Game")}"] \n')
                    f.write(f'[Site "{game_data["metadata"].get("site", "Unknown")}"] \n')
                    f.write(f'[Date "{game_data["timestamp"].split("T")[0].replace("-", ".")}"] \n')
                    f.write(f'[White "{game_data["players"].get("white", "Player 1")}"] \n')
                    f.write(f'[Black "{game_data["players"].get("black", "Player 2")}"] \n')
                    f.write(f'[Result "{game_data["result"]}"] \n')
                    
                    # Additional metadata
                    for key, value in game_data["metadata"].items():
                        if key not in ('event', 'site'):
                            f.write(f'[{key.capitalize()} "{value}"] \n')
                    
                    f.write('\n')
                    
                    # Write moves
                    move_pairs = []
                    for i in range(0, len(game_data["moves"]), 2):
                        if i + 1 < len(game_data["moves"]):
                            move_pairs.append(f"{i//2 + 1}. {game_data['moves'][i]} {game_data['moves'][i+1]}")
                        else:
                            move_pairs.append(f"{i//2 + 1}. {game_data['moves'][i]}")
                    
                    # Format moves with line breaks
                    move_text = ' '.join(move_pairs)
                    f.write(f"{move_text} {game_data['result']}\n\n")
            
            return export_path
        
        else:
            raise ValueError(f"Unsupported export format: {export_format}")