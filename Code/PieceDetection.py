try:
    from SensorArray import SensorArray
    software_mode = False
except ModuleNotFoundError:
    software_mode = True
import time


class PieceDetection:

    NO_MOVE = 0
    ILLEGAL_MOVE = 1

    def __init__(self):
        if not software_mode:
            self.sensor_array_1 = SensorArray(0x20)
            self.sensor_array_2 = SensorArray(0x21)
            self.sensor_array_3 = SensorArray(0x22)
            self.sensor_array_4 = SensorArray(0x23)

        self.frames = []
        self.break_monitoring = False

    def detect(self):
        frame = [[False for _ in range(8)] for _ in range(8)]

        if not software_mode:
            array_1 = self.sensor_array_1.detect()
            array_2 = self.sensor_array_2.detect()
            array_3 = self.sensor_array_3.detect()
            array_4 = self.sensor_array_4.detect()

            for i, a in enumerate([array_1, array_2, array_3, array_4]):
                for j in range(7, -1, -1):
                    frame[7-j][i*2] = a[j]
                for j in range(15, 7, -1):
                    frame[15-j][i*2 + 1] = a[j]

        self.frames.append(frame)

    def difference(self, i1, i2):
        frame1 = self.frames[i1]
        frame2 = self.frames[i2]

        differences = []

        for x in range(8):
            for y in range(8):
                if frame1[y][x] != frame2[y][x]:
                    if frame1[y][x]:
                        differences.append([x, y, False])
                    else:
                        differences.append([x, y, True])

        return differences

    def monitor(self):
        events = []

        initial_frame = len(self.frames) - 1
        if initial_frame < 0:
            self.detect()
            initial_frame = 0
        previous_frame = initial_frame

        minimum_events = 2
        settling_time = 1
        detection_period = 0.1
        settling_frames = settling_time/detection_period
        illegal_redemption = 4/detection_period

        identical_frame_count = 0
        while len(events) < minimum_events or identical_frame_count < settling_frames\
                or (self.constructMove(events) == self.ILLEGAL_MOVE and identical_frame_count < illegal_redemption):
            if self.break_monitoring:
                self.break_monitoring = False
                return None
            self.detect()

            current_frame = len(self.frames) - 1
            differences = self.difference(previous_frame, current_frame)
            if len(differences) == 0:
                identical_frame_count += 1
            else:
                identical_frame_count = 0

            for d in differences:
                d.append(current_frame)
                events.append(d)

            time.sleep(detection_period)

        return events

    def constructMove(self, events):

        events_by_square = {}
        squares = []

        for e in events:
            square_coords = e[0:2]
            square = str(square_coords)

            if square not in events_by_square:
                events_by_square[square] = []
                squares.append(square_coords)
            events_by_square[square].append(e)

        place_squares = []  # squares that only have a piece put on
        pick_squares = []  # squares that only have a piece taken off
        capture_squares = []  # squares that have a piece taken off and put back on

        for square in squares:
            square_events = events_by_square[str(square)]

            direction = 0
            initial_direction = square_events[0][2]
            for e in square_events:
                placed = e[2]
                if placed:
                    direction += 1
                else:
                    direction -= 1

            if direction == 0 and initial_direction is False:
                capture_squares.append(square)
            elif direction > 0:
                place_squares.append(square)
            elif direction < 0:
                pick_squares.append(square)

        if len(place_squares) == 0 and len(pick_squares) == 0:
            return self.NO_MOVE

        # castling
        if len(place_squares) == 2 and len(pick_squares) == 2:
            # [[place_squares] [pick_squares]]
            wkc_squares = [[[6, 7], [5, 7]], [[4, 7], [7, 7]]]
            wqc_squares = [[[2, 7], [3, 7]], [[4, 7], [0, 7]]]
            bkc_squares = [[[6, 0], [5, 0]], [[4, 0], [7, 0]]]
            bqc_squares = [[[2, 0], [3, 0]], [[4, 0], [0, 0]]]

            for square_list in [wkc_squares, wqc_squares, bkc_squares, bqc_squares]:
                place = square_list[0]
                pick = square_list[1]
                match = True
                for square in place_squares:
                    if square not in place:
                        match = False
                        break
                for square in pick_squares:
                    if square not in pick:
                        match = False
                        break

                if match:
                    return [pick[0], place[0]]

            return self.ILLEGAL_MOVE

        # en passant
        if len(pick_squares) == 2 and len(place_squares) == 1:
            y_pick_1 = pick_squares[0][1]
            y_pick_2 = pick_squares[1][1]
            x_pick_1 = pick_squares[0][0]
            x_pick_2 = pick_squares[1][0]
            x_place = place_squares[0][0]
            y_place = place_squares[0][1]

            if y_pick_1 == y_pick_2 and (y_pick_1 == 3 or y_pick_1 == 4) and abs(x_pick_1-x_pick_2) == 1:
                if (y_place == 2 and y_pick_1 == 3) or (y_place == 5 and y_pick_1 == 4):
                    if x_place == x_pick_1:
                        return [pick_squares[1], place_squares[0]]
                    elif x_place == x_pick_2:
                        return [pick_squares[0], place_squares[0]]

            return self.ILLEGAL_MOVE

        # can't be legal if there are this many place and pick squares without it being castle or en passant
        if len(place_squares) > 1 or len(pick_squares) > 1:
            return self.ILLEGAL_MOVE

        # normal move
        if len(place_squares) == 1 and len(pick_squares) == 1:
            return [pick_squares[0], place_squares[0]]

        # captures
        if len(pick_squares) == 1 and len(capture_squares) > 0:
            return [pick_squares[0], capture_squares[-1]]

        # if no legal move type found then must be illegal
        return self.ILLEGAL_MOVE


if __name__ == '__main__':
    p = PieceDetection()
    # for k in range(10):
    #     p.detect()
    #     for line in p.frames[-1]:
    #         print(line)
    #     print("------------------------------------")
    #     time.sleep(1)



