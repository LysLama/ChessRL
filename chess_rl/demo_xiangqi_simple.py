#!/usr/bin/env python3
"""
Demo trận đấu Xiangqi đơn giản sử dụng PyFFish board
"""

import random
from game.xiangqi_pyffish_board import XiangqiPyffishBoard, XiangqiPyffishMove


def print_simple_board(fen):
    """Hiển thị bàn cờ từ FEN string"""
    print("\n" + "="*60)
    print("                BÀN CỜ XIANGQI")
    print("="*60)
    
    # Parse FEN
    parts = fen.split(' ')
    board_fen = parts[0]
    turn = parts[1]
    
    print("   a b c d e f g h i")
    print("  " + "-"*19)
    
    rows = board_fen.split('/')
    for i, row in enumerate(rows):
        rank = 10 - i
        line = f"{rank:2d}|"
        
        for char in row:
            if char.isdigit():
                for _ in range(int(char)):
                    line += " ."
            else:
                line += f" {char}"
        
        line += f" |{rank}"
        print(line)
        
        # Đường sông ở giữa
        if i == 4:
            print("  |" + "-"*17 + "|")
            print("  |   SÔNG HÀN GIỚI   |")
            print("  |" + "-"*17 + "|")
    
    print("  " + "-"*19)
    print("   a b c d e f g h i")
    
    turn_text = "🔴 Đỏ (RED)" if turn == 'w' else "⚫ Đen (BLACK)"
    print(f"\n   Lượt đi: {turn_text}")
    print("="*60)


def demo_xiangqi_simple():
    """Demo Xiangqi đơn giản với PyFFish"""
    
    print("🎮 DEMO XIANGQI - TRẬN ĐẤU MẪU")
    print("="*50)
    
    # Khởi tạo board
    board = XiangqiPyffishBoard()
    print("✅ Đã khởi tạo bàn cờ Xiangqi")
    
    # Hiển thị vị trí ban đầu
    print("\n📍 TRẠNG THÁI BAN ĐẦU:")
    print_simple_board(board.current_fen)
    
    # Lấy nước đi hợp lệ
    legal_moves = board.get_legal_moves()
    print(f"\n📊 Có {len(legal_moves)} nước đi hợp lệ")
    
    if legal_moves:
        # Hiển thị một số nước đi mẫu
        sample_moves = legal_moves[:8]
        print("🎯 Một số nước đi có thể:")
        for i, move in enumerate(sample_moves):
            print(f"   {i+1}. {move.move_str}")
        
        print("\n🚀 BẮT ĐẦU DEMO TRẬN ĐẤU...")
        input("\nNhấn Enter để bắt đầu...")
        
        # Chơi một số nước
        moves_played = 0
        max_moves = 10
        
        while moves_played < max_moves:
            # Lấy nước đi hợp lệ hiện tại
            current_moves = board.get_legal_moves()
            if not current_moves:
                print("🏁 Không còn nước đi hợp lệ! Trận đấu kết thúc.")
                break
            
            # Chọn nước đi ngẫu nhiên
            move = random.choice(current_moves)
            
            print(f"\n🔄 NƯỚC {moves_played + 1}")
            print(f"👉 Nước đi: {move.move_str}")
            
            # Thực hiện nước đi
            try:
                reward, done = board.apply_move(move)
                moves_played += 1
                
                print(f"💯 Phần thưởng: {reward}")
                print(f"🏆 Trạng thái: {'Kết thúc' if done else 'Tiếp tục'}")
                
                # Hiển thị bàn cờ sau nước đi
                print_simple_board(board.current_fen)
                
                if done:
                    print("🎉 TRẬN ĐẤU KẾT THÚC!")
                    break
                
                print(f"📊 Nước đi tiếp theo: {len(board.get_legal_moves())} khả năng")
                
                # Tạm dừng để xem
                input("Nhấn Enter để tiếp tục...")
                
            except Exception as e:
                print(f"❌ Lỗi khi thực hiện nước đi: {e}")
                break
        
        print(f"\n🏁 DEMO HOÀN TẤT!")
        print(f"📈 Tổng số nước đã đi: {moves_played}")
    
    else:
        print("❌ Không có nước đi hợp lệ nào! Có lỗi trong board setup.")


def demo_legal_moves():
    """Demo hiển thị các nước đi hợp lệ"""
    
    print("\n🔍 DEMO NƯỚC ĐI HỢP LỆ")
    print("="*40)
    
    board = XiangqiPyffishBoard()
    legal_moves = board.get_legal_moves()
    
    print(f"📊 Tổng số nước đi hợp lệ từ vị trí ban đầu: {len(legal_moves)}")
    
    # Nhóm theo loại quân
    move_groups = {}
    for move in legal_moves[:20]:  # Chỉ lấy 20 nước đầu
        piece = move.move_str[0]  # Ký tự đầu cho biết cột
        if piece not in move_groups:
            move_groups[piece] = []
        move_groups[piece].append(move.move_str)
    
    print("\n📝 NHÓM NƯỚC ĐI THEO CỘT:")
    for piece, moves in move_groups.items():
        print(f"   Cột {piece}: {', '.join(moves[:5])}")
        if len(moves) > 5:
            print(f"           ... và {len(moves)-5} nước khác")


if __name__ == "__main__":
    try:
        print("🚀 KHỞI ĐỘNG DEMO XIANGQI PYFFISH")
        
        # Demo nước đi hợp lệ trước
        demo_legal_moves()
        
        print("\n" + "="*50)
        choice = input("Bạn có muốn xem demo trận đấu? (y/n): ").lower().strip()
        
        if choice in ['y', 'yes', 'có', 'c']:
            demo_xiangqi_simple()
        else:
            print("Demo kết thúc. Cảm ơn bạn! 👋")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()