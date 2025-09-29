#!/usr/bin/env python3
"""
UI Match Viewer for Chess and Xiangqi.

Features:
- Render boards (Chess 8x8, Xiangqi 9x10) with Unicode pieces
- Auto-play Random vs Random until termination
- Optional "Require Checkmate" mode that restarts games until checkmate occurs
- Controls: Start/Pause, Reset, Game selector, Speed, Require Mate

Note: Random play can be long; require-mate mode may restart many games.
"""

import random
import tkinter as tk
from tkinter import ttk
from typing import Optional, Tuple, Any

from game.chess_board import ChessBoard
from game.xiangqi_pyffish_board import (
    XiangqiPyffishBoard,
    XiangqiPyffishMove,
)
import chess


# -------------------- Rendering helpers --------------------

CHESS_UNICODE = {
    (chess.PAWN, True): "♙",
    (chess.KNIGHT, True): "♘",
    (chess.BISHOP, True): "♗",
    (chess.ROOK, True): "♖",
    (chess.QUEEN, True): "♕",
    (chess.KING, True): "♔",
    (chess.PAWN, False): "♟",
    (chess.KNIGHT, False): "♞",
    (chess.BISHOP, False): "♝",
    (chess.ROOK, False): "♜",
    (chess.QUEEN, False): "♛",
    (chess.KING, False): "♚",
}

XIANGQI_UNICODE = {
    'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '將', 'c': '砲', 'p': '卒',
    'R': '俥', 'N': '傌', 'B': '相', 'A': '仕', 'K': '帥', 'C': '炮', 'P': '兵'
}


class ChessRenderer:
    def __init__(self, canvas: tk.Canvas, cell: int = 64, margin: int = 20):
        self.canvas = canvas
        self.cell = cell
        self.margin = margin

    def board_size(self) -> Tuple[int, int]:
        return 8, 8

    def draw(self, board: Any, last_move: Optional[Any] = None):
        self.canvas.delete("all")
        cols, rows = self.board_size()
        w = cols * self.cell
        h = rows * self.cell
        # Draw squares
        for r in range(rows):
            for c in range(cols):
                x0 = c * self.cell
                y0 = r * self.cell
                x1 = x0 + self.cell
                y1 = y0 + self.cell
                color = "#EEEED2" if (r + c) % 2 == 0 else "#769656"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, width=0)

        # Highlight last move
        if last_move is not None:
            fr = 7 - (last_move.from_square // 8)
            fc = last_move.from_square % 8
            tr = 7 - (last_move.to_square // 8)
            tc = last_move.to_square % 8
            for (rr, cc) in [(fr, fc), (tr, tc)]:
                x0 = cc * self.cell
                y0 = rr * self.cell
                x1 = x0 + self.cell
                y1 = y0 + self.cell
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="#F6F669", width=3)

        # Draw pieces
        for sq in chess.SQUARES:
            piece = board.board.piece_at(sq)
            if piece:
                rr, cc = divmod(sq, 8)
                rr = 7 - rr
                sym = CHESS_UNICODE[(piece.piece_type, piece.color)]
                x = cc * self.cell + self.cell // 2
                y = rr * self.cell + self.cell // 2
                self.canvas.create_text(x, y, text=str(sym), font=("Segoe UI Symbol", self.cell // 2))


class XiangqiRenderer:
    def __init__(self, canvas: tk.Canvas, cell: int = 56, margin: int = 20, colorize: bool = True):
        self.canvas = canvas
        self.cell = cell
        self.margin = margin
        self.colorize = colorize

    def board_size(self) -> Tuple[int, int]:
        return 9, 10

    def _parse_move_str(self, move_str: str) -> Optional[Tuple[int, int, int, int]]:
        """Parse 'h3h10' into (f_col, f_row, t_col, t_row) using 0-based rows (top=0)."""
        if not move_str or len(move_str) < 4:
            return None
        i = 0
        if not move_str[i].isalpha():
            return None
        f_col = ord(move_str[i].lower()) - ord('a')
        i += 1
        j = i
        while j < len(move_str) and move_str[j].isdigit():
            j += 1
        if j == i:
            return None
        try:
            f_rank = int(move_str[i:j])
        except ValueError:
            return None
        i = j
        if i >= len(move_str) or not move_str[i].isalpha():
            return None
        t_col = ord(move_str[i].lower()) - ord('a')
        i += 1
        if i >= len(move_str):
            return None
        try:
            t_rank = int(move_str[i:])
        except ValueError:
            return None
        f_row = 10 - f_rank
        t_row = 10 - t_rank
        return f_col, f_row, t_col, t_row

    def draw(self, board: Any, last_move: Optional[Any] = None):
        self.canvas.delete("all")
        cols, rows = self.board_size()
        # We draw lines within a padded area so stones sit at intersections.
        pad = self.margin
        W = (cols - 1) * self.cell + pad * 2
        H = (rows - 1) * self.cell + pad * 2

        # Resize canvas if needed
        self.canvas.config(width=W, height=H)

        # Background
        self.canvas.create_rectangle(0, 0, W, H, fill="#F8F5E1", width=0)

        # Helper to convert grid (file, rank index) to pixel coordinates (intersection points)
        def pt(c, r):
            return pad + c * self.cell, pad + r * self.cell

        # River gap between ranks 4 and 5 (index 4 and 5). We'll draw two horizontal blocks.
        river_top_y = pad + 4 * self.cell
        river_bottom_y = pad + 5 * self.cell
        self.canvas.create_rectangle(pad - self.cell*0.35, river_top_y, W - pad + self.cell*0.35, river_bottom_y, fill="#CFE8FF", width=0)
        # River text (centered)
        self.canvas.create_text(W/2, (river_top_y + river_bottom_y)/2, text="楚河   漢界", font=("Segoe UI Symbol", int(self.cell*0.5)), fill="#4A4A4A")

        line_color = "#6B6157"

        # Horizontal lines: ranks 0..4 and 5..9 (skip the river crossing)
        for r in range(rows):
            if r == 5:  # skip drawing a line across the river center
                continue
            y = pad + r * self.cell
            self.canvas.create_line(pad, y, W - pad, y, fill=line_color)

        # Vertical lines: files 0..8 all through, but break at river gap (draw two segments)
        for c in range(cols):
            x = pad + c * self.cell
            # Top segment (ranks 0..4)
            self.canvas.create_line(x, pad, x, pad + 4 * self.cell, fill=line_color)
            # Bottom segment (ranks 5..9)
            self.canvas.create_line(x, pad + 5 * self.cell, x, pad + 9 * self.cell, fill=line_color)

        # Palace diagonals: top (ranks 0..2, files 3..5) and bottom (ranks 7..9)
        # Top
        self.canvas.create_line(*pt(3, 0), *pt(5, 2), fill=line_color)
        self.canvas.create_line(*pt(5, 0), *pt(3, 2), fill=line_color)
        # Bottom
        self.canvas.create_line(*pt(3, 7), *pt(5, 9), fill=line_color)
        self.canvas.create_line(*pt(5, 7), *pt(3, 9), fill=line_color)

        # Optional star points (炮 & 兵 positions) - small dots near standard coordinates
        star_radius = 3
        star_points = [
            (1, 2), (7, 2), (0, 3), (2, 3), (4, 3), (6, 3), (8, 3),
            (1, 7), (7, 7), (0, 6), (2, 6), (4, 6), (6, 6), (8, 6)
        ]
        for (cx, cy) in star_points:
            x, y = pt(cx, cy)
            self.canvas.create_oval(x - star_radius, y - star_radius, x + star_radius, y + star_radius, fill=line_color, outline=line_color)

        # Highlight last move
        if last_move is not None:
            parsed = self._parse_move_str(last_move.move_str)
            if parsed is not None:
                f_col, f_row, t_col, t_row = parsed
                for (cc, rr) in [(f_col, f_row), (t_col, t_row)]:
                    cx, cy = pt(cc, rr)
                    r = self.cell * 0.42
                    self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, outline="#F6B26B", width=3)

        # Draw pieces from FEN at intersections
        board_part = board.current_fen.split(' ')[0]
        ranks = board_part.split('/')
        for row_idx, row in enumerate(ranks):
            file_idx = 0
            for ch in row:
                if ch.isdigit():
                    file_idx += int(ch)
                else:
                    sym = XIANGQI_UNICODE.get(ch, ch)
                    cx, cy = pt(file_idx, row_idx)
                    # Stone base (disc)
                    disc_r = self.cell * 0.42
                    # Color scheme: neutral disc always; optionally red vs black text.
                    is_red = ch.isupper()
                    fill_color = "#FDFBF4"  # unified neutral background
                    if self.colorize:
                        txt_color = "#B00000" if is_red else "#111111"
                    else:
                        txt_color = "#222222"
                    self.canvas.create_oval(cx - disc_r, cy - disc_r, cx + disc_r, cy + disc_r, fill=fill_color, outline=line_color, width=2)
                    self.canvas.create_text(cx, cy, text=str(sym), fill=txt_color, font=("Segoe UI Symbol", int(self.cell * 0.42)))
                    file_idx += 1


# -------------------- Controller --------------------

class MatchViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Match Viewer - Chess & Xiangqi")
        self.resizable(False, False)

        # Controls
        ctl = ttk.Frame(self)
        ctl.pack(side=tk.TOP, fill=tk.X, padx=8, pady=6)

        ttk.Label(ctl, text="Game:").pack(side=tk.LEFT)
        self.game_var = tk.StringVar(value="chess")
        game_sel = ttk.Combobox(ctl, textvariable=self.game_var, values=["chess", "xiangqi"], width=10, state="readonly")
        game_sel.pack(side=tk.LEFT, padx=6)
        game_sel.bind("<<ComboboxSelected>>", lambda e: self.reset_game())

        self.require_mate = tk.BooleanVar(value=True)
        ttk.Checkbutton(ctl, text="Require Checkmate", variable=self.require_mate).pack(side=tk.LEFT, padx=6)

        # Colorize (red vs black) enabled by default for Xiangqi
        self.colorize_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(ctl, text="Colorize", variable=self.colorize_var, command=self._on_colorize_toggle).pack(side=tk.LEFT, padx=6)

        ttk.Label(ctl, text="Speed (ms):").pack(side=tk.LEFT, padx=(12, 2))
        self.speed_var = tk.IntVar(value=600)
        spd = ttk.Scale(ctl, from_=100, to=1500, orient=tk.HORIZONTAL, command=lambda v: None)
        spd.set(self.speed_var.get())
        spd.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=6)
        # tie scale updates to var when moving
        spd.bind("<ButtonRelease-1>", lambda e: self.speed_var.set(int(spd.get())))

        self.start_btn = ttk.Button(ctl, text="Start", command=self.toggle_run)
        self.start_btn.pack(side=tk.LEFT, padx=6)

        ttk.Button(ctl, text="Reset", command=self.reset_game).pack(side=tk.LEFT, padx=6)

        # Status
        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(self, textvariable=self.status_var).pack(side=tk.TOP, fill=tk.X, padx=8)

        # Canvas
        # Start with a canvas big enough for Xiangqi (will be resized by renderer)
        self.canvas = tk.Canvas(self, width=9*56 + 40, height=10*56 + 40, bg="white")
        self.canvas.pack(padx=8, pady=8)

        # State
        self.running = False
        self.after_id = None
        self.move_count = 0
        self.last_move = None
        self.board = None  # type: ignore[assignment]
        self.renderer = None  # type: ignore[assignment]

        # Initialize first game
        self._init_game()

    # ------------- Game lifecycle -------------
    def _init_game(self):
        game = self.game_var.get()
        if game == "chess":
            self.board = ChessBoard()
            self.renderer = ChessRenderer(self.canvas, cell=64)
            self.canvas.config(width=8*64, height=8*64)
        else:
            self.board = XiangqiPyffishBoard()
            self.renderer = XiangqiRenderer(self.canvas, cell=56, colorize=self.colorize_var.get())
            self.canvas.config(width=9*56, height=10*56)
        self.move_count = 0
        self.last_move = None
        rend: Any = self.renderer
        rend.draw(self.board, self.last_move)
        self.status_var.set(f"{game.title()} started. Require mate: {self.require_mate.get()}")

    def reset_game(self):
        self.stop()
        self._init_game()

    def _on_colorize_toggle(self):
        # Only affects Xiangqi; if current renderer is Xiangqi, update flag and redraw
        if isinstance(self.renderer, XiangqiRenderer):
            self.renderer.colorize = self.colorize_var.get()
            self.renderer.draw(self.board, self.last_move)

    def toggle_run(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def start(self):
        self.running = True
        self.start_btn.config(text="Pause")
        self._schedule_next()

    def stop(self):
        self.running = False
        self.start_btn.config(text="Start")
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    # ------------- Move logic -------------
    def _schedule_next(self):
        if not self.running:
            return
        delay = max(50, int(self.speed_var.get()))
        self.after_id = self.after(delay, self._step_once)

    def _step_once(self):
        game = self.game_var.get()
        # Check end conditions
        brd0: Any = self.board
        if brd0 is not None and brd0.is_game_over():
            # Determine if checkmate required and satisfied
            if game == "chess" and isinstance(brd0, ChessBoard):
                is_mate = brd0.board.is_checkmate()
            else:
                res = brd0.get_result()
                is_mate = res.get('termination') == 'checkmate'

            if self.require_mate.get() and not is_mate:
                # Restart a new game searching for a checkmate result
                self.status_var.set("Game ended not by mate. Restarting...")
                self._init_game()
                self._schedule_next()
                return
            # End
            msg = "Checkmate!" if is_mate else "Game over (non-mate)."
            self.status_var.set(f"{msg} Moves: {self.move_count}")
            rend2: Any = self.renderer
            rend2.draw(self.board, self.last_move)
            self.stop()
            return

        # Pick a random legal move and apply
        if game == "chess":
            brd: Any = self.board
            legal = brd.get_legal_moves()
            if not legal:
                # Should be covered by is_game_over, but guard anyway
                self.status_var.set("No legal moves.")
                self.stop()
                return
            mv = random.choice(legal)
            brd.apply_move(mv)
            self.last_move = mv
        else:
            brd2: Any = self.board
            legal = brd2.get_legal_moves()
            if not legal:
                self.status_var.set("No legal moves.")
                self.stop()
                return
            mv = random.choice(legal)
            brd2.apply_move(mv)
            self.last_move = mv

        self.move_count += 1
        rend3: Any = self.renderer
        rend3.draw(self.board, self.last_move)
        self.status_var.set(f"Moves: {self.move_count}")
        self._schedule_next()


def main():
    app = MatchViewer()
    app.mainloop()


if __name__ == "__main__":
    main()
