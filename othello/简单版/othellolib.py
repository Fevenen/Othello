import time
import sys
import random

BLACK, WHITE, EMPTY = -1, 1, 0

if "idlelib" in sys.modules:
    BLACK_PIECE = " ● "
    WHITE_PIECE = " ○ "
    EMPTY_PIECE = " □ "
    END_ROW = " "
else:
    # 使用 Emoji 表示棋盘，BG_EMPTY 设置背景色为绿色，BG_RESET 是重置背景色
    BG_EMPTY, BG_RESET = "\x1b[42m", "\x1b[0m"
    BLACK_PIECE = f"{BG_EMPTY}⚫️{BG_RESET}"
    EMPTY_PIECE = f"{BG_EMPTY}🟩{BG_RESET}"
    WHITE_PIECE = f"{BG_EMPTY}⚪️{BG_RESET}"
    END_ROW = f"{BG_EMPTY} {BG_RESET}"


def stone(piece):
    """
    棋子的 Emoji 显示
    参数: 棋子类型(piece): -1, 0, 1, 对应黑棋、空棋、白棋
    """
    stone_coes = [
        BLACK_PIECE,
        EMPTY_PIECE,
        WHITE_PIECE,
    ]
    return stone_coes[piece + 1]


def init_board(n=8):
    """
    创建棋盘并设置初始的 4 枚棋子
    参数: 棋盘规格(n)
    """
    board = [[EMPTY for _ in range(n)] for _ in range(n)]

    C0, C1 = n // 2, n // 2 - 1
    board[C0][C0], board[C1][C1] = WHITE, WHITE  # White
    board[C1][C0], board[C0][C1] = BLACK, BLACK  # Black

    return board


def display_board(board, sleep=0):
    """
    显示棋盘状态
    参数: 棋盘(board), 暂停时间(sleep)
    """
    print("   A  B  C  D   E  F  G  H")
    for i, row in enumerate(board):
        print(i + 1, end=" ")
        for piece in row:
            print(stone(piece), end=" ")
        print()
    if sleep > 0:
        time.sleep(sleep)


def is_valid_position(row, col, n=8):
    """
    判断位置是否在棋盘内
    """
    return 0 <= row < n and 0 <= col < n


def is_valid_move(board, row, col, piece):
    if not is_valid_position(row, col):
        return False
    if board[row][col]!= EMPTY:
        return False

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        opponent_sequence = []
        while is_valid_position(r, c):
            if board[r][c] == EMPTY:
                break
            elif board[r][c] == piece:
                # 若找到己方棋子且中间有对方棋子序列，则可翻转
                if len(opponent_sequence) > 0:
                    return True
                else:
                    break
            else:
                opponent_sequence.append((r, c))
            r += dr
            c += dc
    return False


def do_move(board, row, col, piece):
    """
    执行移动并翻转棋子
    """
    board[row][col] = piece
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        to_flip = []
        r, c = row + dr, col + dc
        while is_valid_position(r, c):
            if board[r][c] == EMPTY:
                break
            elif board[r][c] == piece:
                for fr, fc in to_flip:
                    board[fr][fc] = piece
                break
            else:
                to_flip.append((r, c))
            r += dr
            c += dc


def move_input(board, piece, name):
    """
    返回玩家下一手的位置(row, col)。
    参数: 棋盘(board), 棋子类型(piece), 玩家名称(name)
    """
    while True:
        move = input(f"{name}, 请输入要放置棋子的位置（例如：E4），输入? 查看可放置位置：")
        if move == "?":
            show_available_moves(board, piece)
            continue
        col = ord(move[0].upper()) - ord('A')
        row = int(move[1]) - 1
        if is_valid_move(board, row, col, piece):
            return row, col
        else:
            print("无效的移动，请重新输入。")


def show_available_moves(board, piece):
    """
    显示可放置棋子的位置
    """
    available_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_valid_move(board, row, col, piece):
                available_moves.append((row, col))
    if available_moves:
        print("可放置棋子的位置：")
        for move in available_moves:
            row, col = move
            print(f"{chr(col + ord('A'))}{row + 1}", end=" ")
        print()
    else:
        print("当前没有可放置棋子的位置。")


def move_random(board, piece, name):
    """
    随机从可放置棋子的位置中选择一个
    """
    available_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if is_valid_move(board, row, col, piece):
                available_moves.append((row, col))
    if available_moves:
        return random.choice(available_moves)
    else:
        return None


def create_player(name, move):
    """
    创建玩家
    参数: 玩家名称(name), 玩家使用的选择下一步位置的函数(move)
    """
    if move == move_input:
        piece = BLACK
    else:
        piece = WHITE
    return {'name': name,'move': move, 'piece': piece}


def count_pieces(board):
    """
    统计棋盘上黑白棋子数量
    """
    black_count = sum(row.count(BLACK) for row in board)
    white_count = sum(row.count(WHITE) for row in board)
    return black_count, white_count


def is_game_over(board):
    return all(board[row][col]!= EMPTY for row in range(len(board)) for col in range(len(board[0]))) or \
           (not any(is_valid_move(board, row, col, BLACK) for row in range(len(board)) for col in range(len(board[0]))) and
            not any(is_valid_move(board, row, col, WHITE) for row in range(len(board)) for col in range(len(board[0]))))


def game(player1, player2, n=8):
    """
    游戏入口函数。
    参数: 两个玩家, 其中 player1 执黑, player2 执白.
    """
    board = init_board()
    display_board(board)
    current_player = player1
    while True:
        # 获取玩家移动
        move = current_player['move'](board, current_player['piece'], current_player['name'])
        if move is None:
            print(f"{current_player['name']} 没有合法移动，跳过回合。")
            current_player = player2 if current_player == player1 else player1
            continue
        row, col = move
        do_move(board, row, col, current_player['piece'])
        display_board(board)
        if is_game_over(board):
            winner = determine_winner(board)
            print(f"游戏结束，获胜者是：{winner}")
            break
        current_player = player2 if current_player == player1 else player1


def determine_winner(board):
    """
    确定游戏获胜者
    """
    black_count, white_count = count_pieces(board)
    if black_count > white_count:
        return "黑方"
    elif white_count > black_count:
        return "白方"
    else:
        return "平局"
