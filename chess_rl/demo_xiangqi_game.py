#!/usr/bin/env python3
"""
Demo trận đấu Xiangqi với hiển thị bàn cờ chi tiết và tương tác
"""

import random
from environments.xiangqi_env import XiangqiEnv
from game.xiangqi_pyffish_board import XiangqiPyffishBoard, XiangqiPyffishMove


def print_xiangqi_board_visual(board_str):
    """Hiển thị bàn cờ Xiangqi một cách trực quan"""
    
    print("\n" + "="*50)
    print("           BÀN CỜ XIANGQI")
    print("="*50)
    
    # Hiển thị board string có sẵn với một số trang trí
    lines = board_str.strip().split('\n')
    for line in lines:
        if line.strip():
            # Thêm viền cho board
            if any(c in line for c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']):
                print(f"   {line}")
            else:
                print(f"     {line}")
    
    print("\n   🔴 = Quân đỏ (Red)    ⚫ = Quân đen (Black)")
    print("="*50)


def explain_move(move_str):
    """Giải thích nước đi"""
    from_pos = move_str[:2]
    to_pos = move_str[2:]
    
    # Chuyển đổi tọa độ
    from_col = chr(ord('a') + ord(from_pos[0]) - ord('a'))
    from_row = from_pos[1]
    to_col = chr(ord('a') + ord(to_pos[0]) - ord('a'))
    to_row = to_pos[1]
    
    return f"Đi từ {from_col}{from_row} đến {to_col}{to_row}"


def demo_xiangqi_game():
    """Demo một trận đấu Xiangqi hoàn chỉnh"""
    
    print("\n" + "🎯"*20)
    print("      DEMO TRẬN ĐẤU XIANGQI")
    print("🎯"*20)
    
    # Khởi tạo môi trường Xiangqi
    env = XiangqiEnv()
    observation, info = env.reset()
    
    # Hiển thị bàn cờ ban đầu
    print("\n📍 VỊ TRÍ BAN ĐẦU:")
    board_str = info["board_str"]
    print_xiangqi_board_visual(board_str)
    
    print(f"\n🎮 Lượt đi: {'Đỏ (Red)' if info['turn'] == 'red' else 'Đen (Black)'}")
    print(f"📊 Số nước đi hợp lệ: {len(info['legal_moves'])}")
    
    step = 0
    max_steps = 20  # Giới hạn số bước để demo
    
    while step < max_steps:
        step += 1
        
        # Lấy danh sách nước đi hợp lệ
        legal_moves = info["legal_moves"]
        if not legal_moves:
            print("\n🏁 Không còn nước đi hợp lệ! Ván cờ kết thúc.")
            break
        
        # Chọn một nước đi ngẫu nhiên
        action = random.choice(range(len(legal_moves)))
        
        # Thực hiện nước đi
        observation, reward, terminated, truncated, info = env.step(action)
        
        # Lấy thông tin nước đi
        move = env.action_to_move(action)
        move_str = str(move)
        
        print(f"\n🔄 BƯỚC {step}")
        print(f"👉 Nước đi: {move_str} ({explain_move(move_str)})")
        print(f"🎯 Lượt: {'Đỏ (Red)' if step % 2 == 1 else 'Đen (Black)'}")
        
        # Hiển thị bàn cờ sau nước đi
        print_xiangqi_board_visual(info["board_str"])
        
        print(f"🏆 Phần thưởng: {reward}")
        print(f"📊 Nước đi tiếp theo: {len(info.get('legal_moves', []))} khả năng")
        
        if terminated:
            print(f"\n🎉 GAME OVER! Kết quả: {info.get('result', 'Không xác định')}")
            break
        elif truncated:
            print(f"\n⏰ Ván cờ bị cắt ngắn do quá số bước tối đa.")
            break
        
        # Tạm dừng để dễ theo dõi
        print("\n" + "-"*30)
        input("Nhấn Enter để tiếp tục...")
    
    print(f"\n🏁 DEMO HOÀN TẤT!")
    print(f"📈 Tổng số bước: {step}")
    print(f"📊 Trạng thái cuối: {'Kết thúc' if terminated else 'Đang chơi'}")


def demo_xiangqi_environment():
    """Demo môi trường Xiangqi cơ bản"""
    
    print("\n" + "🔧"*20)
    print("   DEMO MÔI TRƯỜNG XIANGQI")
    print("🔧"*20)
    
    # Khởi tạo environment
    env = XiangqiEnv()
    print("✅ Đã khởi tạo XiangqiEnv")
    
    # Reset environment
    obs, info = env.reset()
    print(f"✅ Đã reset environment")
    print(f"📊 Observation shape: {obs.shape}")
    print(f"🎯 Turn: {info['turn']}")
    print(f"📝 Board: Available")
    print(f"🔢 Legal moves: {len(info['legal_moves'])}")
    
    # Thử một vài nước đi
    print(f"\n🎮 Thử 3 nước đi ngẫu nhiên:")
    
    for i in range(3):
        legal_moves = info["legal_moves"]
        if not legal_moves:
            break
            
        action = random.choice(range(len(legal_moves)))
        obs, reward, done, truncated, info = env.step(action)
        
        print(f"  Bước {i+1}: Action {action}, Reward {reward}, Done {done}")
        print(f"          Legal moves: {len(info.get('legal_moves', []))}")
        
        if done or truncated:
            break


if __name__ == "__main__":
    print("🚀 KHỞI ĐỘNG DEMO XIANGQI")
    
    try:
        # Demo môi trường trước
        demo_xiangqi_environment()
        
        # Hỏi người dùng có muốn xem demo trận đấu không
        print("\n" + "="*50)
        choice = input("Bạn có muốn xem demo trận đấu chi tiết? (y/n): ").lower().strip()
        
        if choice in ['y', 'yes', 'có', 'c']:
            demo_xiangqi_game()
        else:
            print("Demo kết thúc. Cảm ơn bạn! 👋")
            
    except Exception as e:
        print(f"❌ Lỗi trong quá trình demo: {e}")
        print("Vui lòng kiểm tra lại cài đặt môi trường.")