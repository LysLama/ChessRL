"""
Move module - Representation of a chess move with immutable properties
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, Tuple


@dataclass(frozen=True)
class Move:
    """
    Immutable representation of a chess move.
    
    This class is designed to be hashable and immutable, making it suitable
    for use as dictionary keys or in sets.
    
    Attributes:
        from_sq: The starting square (0-63)
        to_sq: The destination square (0-63)
        promotion: The piece type for promotion (if applicable)
        metadata: Additional information about the move
    """
    from_sq: int
    to_sq: int
    promotion: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_uci(cls, uci_str: str) -> 'Move':
        """
        Create a Move object from UCI string notation.
        
        Args:
            uci_str: UCI format move string (e.g., "e2e4", "e7e8q")
            
        Returns:
            Move object
        """
        # Convert file and rank to square index
        def square_to_index(file: str, rank: str) -> int:
            file_idx = ord(file) - ord('a')
            rank_idx = int(rank) - 1
            return rank_idx * 8 + file_idx
        
        # Parse the UCI string
        from_file, from_rank = uci_str[0], uci_str[1]
        to_file, to_rank = uci_str[2], uci_str[3]
        
        from_sq = square_to_index(from_file, from_rank)
        to_sq = square_to_index(to_file, to_rank)
        
        # Check for promotion piece
        promotion = None
        if len(uci_str) == 5:
            promotion_map = {'q': 5, 'r': 4, 'b': 3, 'n': 2}
            promotion = promotion_map.get(uci_str[4].lower(), None)
        
        return cls(from_sq=from_sq, to_sq=to_sq, promotion=promotion)
    
    def to_uci(self) -> str:
        """
        Convert Move to UCI string notation.
        
        Returns:
            UCI format move string
        """
        # Convert square index to file and rank
        def index_to_square(index: int) -> Tuple[str, str]:
            rank = index // 8 + 1
            file = chr(ord('a') + (index % 8))
            return file, str(rank)
        
        from_file, from_rank = index_to_square(self.from_sq)
        to_file, to_rank = index_to_square(self.to_sq)
        
        uci = from_file + from_rank + to_file + to_rank
        
        # Add promotion piece if applicable
        if self.promotion:
            promotion_map = {5: 'q', 4: 'r', 3: 'b', 2: 'n'}
            uci += promotion_map.get(self.promotion, '')
        
        return uci
    
    def __str__(self) -> str:
        """String representation of the move."""
        return self.to_uci()