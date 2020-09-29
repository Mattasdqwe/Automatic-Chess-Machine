import threading

try:
    from Motor import Motor
    from Electromagnet import Electromagnet
    software_mode = False
except ModuleNotFoundError:
    software_mode = True
import chess
import math
import copy
import bisect
import queue



class Pathing:
    piece_info = {
        # [count, total, [capture_pos1, capture_pos2...]
        'P': [0, 8, [(1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (1, 1), (1, 0)]],
        'R': [0, 2, [(0, 7), (0, 0)]],
        'N': [0, 2, [(0, 6), (0, 1)]],
        'B': [0, 2, [(0, 5), (0, 2)]],
        'Q': [0, 1, [(0, 4)]],
        'K': [0, 1, [(0, 3)]],
        'p': [0, 8, [(12, 0), (12, 1), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7)]],
        'r': [0, 2, [(13, 0), (13, 7)]],
        'n': [0, 2, [(13, 1), (13, 6)]],
        'b': [0, 2, [(13, 2), (13, 5)]],
        'q': [0, 1, [(13, 3)]],
        'k': [0, 1, [(13, 4)]]
    }

    def __init__(self):
        if not software_mode:
            self.x_motor = Motor(18, 23, 27, 2700)
            self.y_motor = Motor(4, 17, 22, 1800)
            self.electromagnet = Electromagnet()
            self.homeMotors()

        self.max_x = 13
        self.max_y = 7
        self.board_representation = [[None for x in range(self.max_x + 1)] for y in range(self.max_y + 1)]
        self.movement_speed = 1500
        self.move_pieces_speed = 1000

    # assumes board representation is already updated previously
    def makeMove(self, move):
        from_square = move.from_square
        from_x = from_square % 8 + 3
        from_y = 7 - int(from_square / 8)
        to_square = move.to_square
        to_x = to_square % 8 + 3
        to_y = 7 - int(to_square / 8)
        promotion_piece = None
        if move.promotion is not None:
            promotion_piece = chess.piece_symbol(move.promotion)
            if from_y == 1:
                promotion_piece = promotion_piece.upper()

        # captures
        capture = False
        if self.board_representation[to_y][to_x] is not None:
            capture = True
            capture_piece = self.board_representation[to_y][to_x].symbol()
            for square in self.piece_info[capture_piece][2]:
                if self.board_representation[square[1]][square[0]] is None:
                    capture_x = square[0]
                    capture_y = square[1]
                    break

        # en-passant
        en_passant = False
        if (self.board_representation[from_y][from_x] == chess.Piece.from_symbol('P')
            or self.board_representation[from_y][from_x] == chess.Piece.from_symbol('p')) \
                and from_x != to_x and capture is False:
            en_passant = True
            en_passant_from_x = to_x
            en_passant_from_y = from_y
            capture_piece = self.board_representation[en_passant_from_y][en_passant_from_x].symbol()
            for square in self.piece_info[capture_piece][2]:
                if self.board_representation[square[1]][square[0]] is None:
                    en_passant_to_x = square[0]
                    en_passant_to_y = square[1]
                    break

        # castles
        castles = False
        if not capture and not en_passant and \
                (self.board_representation[from_y][from_x] == chess.Piece.from_symbol('K') or
                 self.board_representation[from_y][from_x] == chess.Piece.from_symbol('k')) and abs(from_x - to_x) > 1:
            castles = True
            rook_from_y = from_y
            rook_to_y = from_y
            if to_x == 9:  # kingside
                rook_from_x = 10
                rook_to_x = 8
            if to_x == 5:  # queenside
                rook_from_x = 10
                rook_to_x = 8

        # promotion
        promotion = False
        if promotion_piece is not None:
            promotion = True
            pawn = self.board_representation[from_y][from_x].symbol()
            promotion_piece_exists = False
            for square in reversed(self.piece_info[promotion_piece][2]):
                if self.board_representation[square[1]][square[0]] is not None:
                    promotion_from_x = square[0]
                    promotion_from_y = square[1]
                    promotion_piece_exists = True
                    break

            for square in self.piece_info[pawn][2]:
                if self.board_representation[square[1]][square[0]] is None:
                    pawn_to_x = square[0]
                    pawn_to_y = square[1]
                    break

        if capture:
            self.findAndExecutePaths([to_x, to_y], [capture_x, capture_y])
            if promotion:
                if promotion_piece_exists:
                    self.findAndExecutePaths([from_x, from_y], [pawn_to_x, pawn_to_y])
                    self.findAndExecutePaths([promotion_from_x, promotion_from_y], [to_x, to_y])
                else:
                    self.findAndExecutePaths([from_x, from_y], [to_x, to_y])
            else:
                self.findAndExecutePaths([from_x, from_y], [to_x, to_y])
        elif en_passant:
            self.findAndExecutePaths([en_passant_from_x, en_passant_from_y], [en_passant_to_x, en_passant_to_y])
            self.findAndExecutePaths([from_x, from_y], [to_x, to_y])
        elif castles:
            self.findAndExecutePaths([from_x, from_y], [to_x, to_y])
            self.findAndExecutePaths([rook_from_x, rook_from_y], [rook_to_x, rook_to_y])
        elif promotion:
            if promotion_piece_exists:
                self.findAndExecutePaths([from_x, from_y], [pawn_to_x, pawn_to_y])
                self.findAndExecutePaths([promotion_from_x, promotion_from_y], [to_x, to_y])
            else:
                self.findAndExecutePaths([from_x, from_y], [to_x, to_y])
        else:
            self.findAndExecutePaths([from_x, from_y], [to_x, to_y])

    def findAndExecutePaths(self, initial_square, destination_square):
        top_paths = self.pathSearch(initial_square, destination_square, top_number=2)

        min_length = 2000
        min_path = None
        obstacle_paths = None
        for path in top_paths:
            possible = True
            length = path[0]
            taken_squares = [copy.deepcopy(path[1][0]), copy.deepcopy(path[1][-1])]
            free_squares = []
            non_final_squares = copy.deepcopy(path[1])
            for square in self.getDiagonalSquares(path[1]):
                non_final_squares.append(square)
            current_obstacle_paths = []
            for obstacle in path[2]:
                best_obstacle_path = self.pathSearchObstacles(initial_square=obstacle,
                                                              free_squares=free_squares,
                                                              taken_squares=taken_squares,
                                                              non_final_squares=non_final_squares)
                if best_obstacle_path is not None:
                    current_obstacle_paths.append(best_obstacle_path)
                    length += 2*best_obstacle_path[0]
                    for paths_taken in best_obstacle_path[1:]:
                        taken_squares.append(copy.deepcopy(paths_taken[-1]))
                        free_squares.append(copy.deepcopy(paths_taken[0]))
                else:
                    possible = False
                    break

            if possible and length < min_length:
                min_length = length
                min_path = path
                obstacle_paths = current_obstacle_paths

        if min_path is None:
            raise ValueError

        # obstacle paths
        if obstacle_paths is not None:
            for path_list in obstacle_paths:
                for path in path_list[2:]:
                    self.executePath(path)
                self.executePath(path_list[1])

        # main path
        self.executePath(min_path[1])

        # obstacle paths return to original position
        if obstacle_paths is not None:
            for path_list in reversed(obstacle_paths):
                self.executePath(path_list[1], reverse=True)
                for path in reversed(path_list[2:]):
                    self.executePath(path, reverse=True)

        temp = self.board_representation[initial_square[1]][initial_square[0]]
        self.board_representation[destination_square[1]][destination_square[0]] = temp
        self.board_representation[initial_square[1]][initial_square[0]] = None

    def executePath(self, path, reverse=False):
        if reverse:
            path = list(reversed(path))
        x, y = self.coordinateToSteps(path[0][0], path[0][1])

        if not software_mode:
            self.electromagnet.off()
            self.moveTo(x, y, self.movement_speed)
            self.electromagnet.on()
            for square in path[1:]:
                x, y = self.coordinateToSteps(square[0], square[1])
                self.moveTo(x, y, self.move_pieces_speed)

            self.electromagnet.off()
        else:
            print(path)

    def updateBoardRep(self, board):
        for i in range(64):
            piece = board.piece_at(i)
            self.board_representation[7 - int(i / 8)][(i % 8) + 3] = piece
            if piece is not None:
                self.piece_info[piece.symbol()][0] += 1

        extra_pieces_white = 0
        extra_pieces_black = 0
        for key in self.piece_info:
            if key in ['P', 'p']:
                continue
            for i in range(0, self.piece_info[key][1] - self.piece_info[key][0]):
                x = self.piece_info[key][2][i][0]
                y = self.piece_info[key][2][i][1]
                self.board_representation[y][x] = chess.Piece.from_symbol(key)
            if self.piece_info[key][0] > self.piece_info[key][1]:
                if key.isupper():
                    extra_pieces_white += self.piece_info[key][0] - self.piece_info[key][1]
                else:
                    extra_pieces_black += self.piece_info[key][0] - self.piece_info[key][1]

        for i in range(0, self.piece_info['P'][1] - self.piece_info['P'][0] - extra_pieces_white):
            x = self.piece_info['P'][2][i][0]
            y = self.piece_info['P'][2][i][1]
            self.board_representation[y][x] = chess.Piece.from_symbol('P')
        for i in range(0, self.piece_info['p'][1] - self.piece_info['p'][0] - extra_pieces_black):
            x = self.piece_info['p'][2][i][0]
            y = self.piece_info['p'][2][i][1]
            self.board_representation[y][x] = chess.Piece.from_symbol('p')

    def checkBoardMatch(self):
        # checks physical board to see if match
        pass

    def coordinateToSteps(self, x, y):
        start_point_x = 350
        start_point_y = 350
        steps_between_square = 100
        conversion_table = [[[start_point_x + steps_between_square*x,
                              start_point_y + steps_between_square*(self.max_y-y)]
                             for x in range(self.max_x+1)] for y in range(self.max_y+1)]
        point = conversion_table[y][x]

        return point[0], point[1]

    def moveTo(self, x, y, speed):
        if software_mode:
            return
        x_steps = abs(x - self.x_motor.getStepCount())
        x_dir = 1
        if x < self.x_motor.getStepCount():
            x_dir = -1
        y_steps = abs(y - self.y_motor.getStepCount())
        y_dir = 1
        if y < self.y_motor.getStepCount():
            y_dir = -1

        try:
            cos_theta = x_steps / (math.sqrt(x_steps ** 2 + y_steps ** 2))
            sin_theta = y_steps / (math.sqrt(x_steps ** 2 + y_steps ** 2))
            x_speed = int(speed * cos_theta)
            y_speed = int(speed * sin_theta)
        except ZeroDivisionError:
            x_speed = 0
            y_speed = 0

        x_thread = threading.Thread(target=self.x_motor.step, args=[x_steps, x_dir, x_speed])
        y_thread = threading.Thread(target=self.y_motor.step, args=[y_steps, y_dir, y_speed])

        x_thread.start()
        y_thread.start()

        x_thread.join()
        y_thread.join()

    def homeMotors(self):
        if software_mode:
            return
        self.x_motor.home()
        self.y_motor.home()

    def pathSearch(self, initial_square, destination_square, top_number=10):
        initial_square = copy.deepcopy(initial_square)
        obstruction_modifier = 3

        top_paths = []

        # path format (path_length, path_squares, obstruction_squares)
        current_paths = queue.PriorityQueue()
        current_paths.put((0, [initial_square], []))
        while len(top_paths) < top_number and not current_paths.empty():
            path = current_paths.get()
            length = path[0]
            if len(top_paths) > 0 and top_paths[0][0] < length:
                break
            squares = path[1]
            obstructions = path[2]

            for offset in [[0, -1], [0, 1], [-1, 0], [1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
                next_square = [squares[-1][0] + offset[0], squares[-1][1] + offset[1]]
                if next_square[0] < 0 or next_square[0] > self.max_x or next_square[1] < 0 or next_square[
                        1] > self.max_y:
                    continue  # out of bounds
                if next_square in squares:
                    continue

                # obstruction calculation
                next_obstructions = copy.deepcopy(obstructions)
                if self.board_representation[next_square[1]][next_square[0]] is not None:
                    next_obstructions.append([next_square[0], next_square[1]])
                if offset in [[1, 1], [1, -1], [-1, 1], [-1, -1]]:
                    if self.board_representation[next_square[1]][next_square[0] - offset[0]] is not None:
                        next_obstructions.append([next_square[0] - offset[0], next_square[1]])
                    if self.board_representation[next_square[1] - offset[1]][next_square[0]] is not None:
                        next_obstructions.append([next_square[0], next_square[1] - offset[1]])

                next_length = length + 1 + obstruction_modifier * (len(next_obstructions) - len(obstructions))
                next_squares = copy.deepcopy(squares)
                next_squares.append(next_square)

                if next_square == destination_square:
                    bisect.insort(top_paths, (next_length, next_squares, next_obstructions))
                else:
                    current_paths.put((next_length, next_squares, next_obstructions))

        return top_paths

    # free_squares: squares that have been freed with the moving of other obstacles
    # taken_squares: squares that can't be moved through being the final destination of other obstacles
    # non_final_squares: squares that can be pathed through but can't be the final square
    def pathSearchObstacles(self, initial_square, free_squares, taken_squares, non_final_squares, depth=0):
        max_depth = 3
        if depth >= max_depth:
            return None
        initial_square = copy.deepcopy(initial_square)
        top_number = 10
        top_paths = []

        # path format (path_length, path_squares, supporting_paths)
        current_paths = queue.SimpleQueue()
        current_paths.put([0, [initial_square]])

        while len(top_paths) < top_number and not current_paths.empty():
            path = current_paths.get()
            length = path[0]
            squares = path[1]
            extra_taken_squares = []
            extra_free_squares = []
            extra_taken_squares.append(copy.deepcopy(squares[0]))
            extra_non_final_squares = []
            for square in squares:
                extra_non_final_squares.append(copy.deepcopy(square))
            for supporting_path in path[2:]:
                extra_free_squares.append(copy.deepcopy(supporting_path[0]))
                extra_taken_squares.append(copy.deepcopy(supporting_path[-1]))

            for offset in [[0, -1], [0, 1], [-1, 0], [1, 0]]:
                next_square = [squares[-1][0] + offset[0], squares[-1][1] + offset[1]]
                if next_square[0] < 0 or next_square[0] > self.max_x or next_square[1] < 0 or next_square[
                        1] > self.max_y:
                    continue  # out of bounds
                if next_square in squares:
                    continue
                if next_square in taken_squares or next_square in extra_taken_squares:
                    continue

                if self.board_representation[next_square[1]][next_square[0]] is not None \
                        and next_square not in free_squares and next_square not in extra_free_squares:
                    next_free_squares = copy.deepcopy(free_squares)
                    next_taken_squares = copy.deepcopy(taken_squares)
                    next_non_final_squares = copy.deepcopy(non_final_squares)
                    for square in extra_free_squares:
                        next_free_squares.append(square)
                    for square in extra_taken_squares:
                        next_taken_squares.append(square)
                    for square in extra_non_final_squares:
                        next_non_final_squares.append(square)

                    obstacle_paths = self.pathSearchObstacles(next_square, next_free_squares, next_taken_squares,
                                                              next_non_final_squares, depth=depth + 1)
                    if obstacle_paths is None:
                        continue
                    else:
                        next_length = length + 1 + obstacle_paths[0]
                        next_path = copy.deepcopy(path)
                        next_path[0] = next_length
                        next_path[1].append(next_square)
                        for p in obstacle_paths[2:]:
                            next_path.append(p)
                        next_path.append(obstacle_paths[1])

                        if next_square not in non_final_squares:
                            bisect.insort(top_paths, next_path)
                        else:
                            current_paths.put(next_path)
                else:
                    next_length = length + 1
                    next_path = copy.deepcopy(path)
                    next_path[0] = next_length
                    next_path[1].append(next_square)
                    if next_square not in non_final_squares:
                        bisect.insort(top_paths, next_path)
                    else:
                        current_paths.put(next_path)

        if len(top_paths) > 0:
            return top_paths[0]
        else:
            return None

    @staticmethod
    def getDiagonalSquares(path):
        diagonal_squares = []
        for i, square in enumerate(path):
            if i == 0:
                continue
            x_diff = square[0] - path[i-1][0]
            y_diff = square[1] - path[i-1][1]
            if abs(x_diff) + abs(y_diff) > 1:
                diagonal_squares.append([square[0], path[i-1][1]])
                diagonal_squares.append([path[i-1][0], square[1]])
        return diagonal_squares


if __name__ == '__main__':

    p = Pathing()
    p.homeMotors()
    import time

    while True:
        k = [int(v) for v in input("enter x and y").split(' ')]
        p.moveTo(k[0], k[1], 200)

    # p.updateBoardRep(chess.Board())
    # k = p.pathSearch(initial_square=[4, 7], destination_square=[3, 5])
    # for i in k:
    #     print(i)
    #
    # x = p.pathSearchObstacles(initial_square=[4, 6], free_squares=[], taken_squares=[[4, 7]],
    #                           non_final_squares=[[4, 7], [4, 6], [4, 5], [3, 5]])
    # print(x)

    # p.makeMove(chess.Move.from_uci('f1f3'))