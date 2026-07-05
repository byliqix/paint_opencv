import cv2
import numpy as np
import time
import os
import math
import random
from mediapipe.tasks.python.vision.gesture_recognizer import (
    GestureRecognizer,
    GestureRecognizerOptions,
)
from mediapipe.tasks.python.core.base_options import BaseOptions
from mediapipe.tasks.python.vision.core.image import Image, ImageFormat

WIDTH, HEIGHT = 1280, 720
MODEL_PATH = os.path.expanduser("~/.mediapipe/models/gesture_recognizer.task")


class MagicSparkle:
    def __init__(self, x, y, color):
        self.x = x + random.uniform(-20, 20)
        self.y = y + random.uniform(-20, 20)
        self.tx = x + random.uniform(-100, 100)
        self.ty = y + random.uniform(-200, -50)
        self.life = 1.0
        self.decay = random.uniform(0.008, 0.025)
        self.size = random.uniform(2, 7)
        self.color = color
        self.phase = random.uniform(0, 2 * math.pi)
        self.glint = random.random() < 0.2
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-4, -1)

    def update(self, hx, hy):
        self.vy += 0.05
        self.vx += math.sin(self.phase + time.time() * 2) * 0.3
        self.x += self.vx
        self.y += self.vy
        self.life -= self.decay
        self.size *= 0.995
        if hx > 0:
            dx = self.x - hx
            dy = self.y - hy
            d = math.sqrt(dx * dx + dy * dy) + 1
            self.vx -= dx / d * 0.2
            self.vy -= dy / d * 0.2

    def draw(self, frame):
        if self.life <= 0:
            return False
        a = self.life
        glow = max(1, int(self.size * a * 2))
        bright = tuple(min(255, int(ch * a * 2.5)) for ch in self.color)
        c = tuple(min(255, int(ch * a)) for ch in self.color)
        r = max(1, int(self.size * a))
        ix, iy = int(self.x), int(self.y)

        cv2.circle(frame, (ix, iy), glow, bright, -1)
        cv2.circle(frame, (ix, iy), r, c, -1)

        if self.glint:
            for i in range(4):
                angle = i * math.pi / 2 + self.phase + time.time()
                dx = int(math.cos(angle) * r * 1.5)
                dy = int(math.sin(angle) * r * 1.5)
                cv2.circle(frame, (ix + dx, iy + dy), max(1, r // 3), bright, -1)
        return True


class MagicRune:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.points = []
        for _ in range(random.randint(5, 8)):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(15, 40)
            self.points.append((x + math.cos(angle) * dist,
                                y + math.sin(angle) * dist))
        self.life = 1.0
        self.color = color
        self.phase = random.uniform(0, 2 * math.pi)

    def update(self):
        self.life -= 0.008
        return self.life > 0

    def draw(self, frame):
        a = self.life
        c = tuple(min(255, int(ch * a * 0.8)) for ch in self.color)
        glow = tuple(min(255, int(ch * a * 0.4)) for ch in self.color)
        for i in range(len(self.points)):
            x1, y1 = int(self.points[i][0]), int(self.points[i][1])
            x2, y2 = int(self.points[(i + 1) % len(self.points)][0]), int(self.points[(i + 1) % len(self.points)][1])
            cv2.line(frame, (x1, y1), (x2, y2), glow, max(1, int(4 * a)))
            cv2.line(frame, (x1, y1), (x2, y2), c, max(1, int(2 * a)))
            cv2.circle(frame, (x1, y1), max(1, int(3 * a)), c, -1)


class MagicTrail:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.history = [(x, y)]
        self.max_len = 15
        self.color = color
        self.life = 1.0

    def add(self, x, y):
        self.history.append((x, y))
        if len(self.history) > self.max_len:
            self.history.pop(0)

    def update(self):
        self.life -= 0.003

    def draw(self, frame):
        if self.life <= 0:
            return False
        a = self.life
        n = len(self.history)
        for i in range(n - 1):
            t = (i + 1) / max(n, 2)
            x1, y1 = int(self.history[i][0]), int(self.history[i][1])
            x2, y2 = int(self.history[i + 1][0]), int(self.history[i + 1][1])
            c = tuple(min(255, int(ch * t * a * 0.6)) for ch in self.color)
            glow = tuple(min(255, int(ch * t * a * 0.3)) for ch in self.color)
            thk1 = max(1, int(6 * t * a))
            thk2 = max(1, int(3 * t * a))
            cv2.line(frame, (x1, y1), (x2, y2), glow, thk1)
            cv2.line(frame, (x1, y1), (x2, y2), c, thk2)
        cv2.circle(frame, (int(self.history[-1][0]), int(self.history[-1][1])),
                   int(3 * a), self.color, -1)
        return True


class Firefly:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)
        self.phase = random.uniform(0, 2 * math.pi)
        self.size = random.uniform(1, 3)
        self.brightness = random.uniform(0.3, 1.0)

    def update(self):
        self.vx += math.sin(self.phase + time.time() * 0.5) * 0.1
        self.vy += math.cos(self.phase * 1.3 + time.time() * 0.3) * 0.1
        self.vx *= 0.98
        self.vy *= 0.98
        self.x += self.vx
        self.y += self.vy
        self.brightness = 0.3 + 0.7 * math.sin(self.phase + time.time() * 2) ** 2
        if self.x < 0 or self.x > WIDTH:
            self.vx *= -1
        if self.y < 0 or self.y > HEIGHT:
            self.vy *= -1

    def draw(self, frame):
        b = self.brightness
        r = max(1, int(self.size * b))
        c = tuple(min(255, int(ch * b * 0.8)) for ch in (200, 255, 220))
        glow = tuple(min(255, int(ch * b * 0.3)) for ch in (200, 255, 220))
        cv2.circle(frame, (int(self.x), int(self.y)), r * 2, glow, -1)
        cv2.circle(frame, (int(self.x), int(self.y)), r, c, -1)
        cv2.circle(frame, (int(self.x), int(self.y)), max(1, r // 2), (255, 255, 255), -1)


def get_magic_color(t, hi=0):
    hue = (t * 50 + hi * 120) % 360
    h = hue / 60
    c_val = 255
    x_val = int(255 * (1 - abs(h % 2 - 1)))
    if h < 1:
        return (x_val, 255, c_val)
    elif h < 2:
        return (c_val, x_val, 255)
    elif h < 3:
        return (c_val, 255, x_val)
    elif h < 4:
        return (x_val, c_val, 255)
    elif h < 5:
        return (255, x_val, c_val)
    else:
        return (255, c_val, x_val)


def draw_hand_landmarks(img, landmarks, w, h, color):
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),
        (0, 5), (5, 6), (6, 7), (7, 8),
        (0, 9), (9, 10), (10, 11), (11, 12),
        (0, 13), (13, 14), (14, 15), (15, 16),
        (0, 17), (17, 18), (18, 19), (19, 20),
        (5, 9), (9, 13), (13, 17),
    ]
    glow_c = tuple(min(255, c // 2) for c in color)
    for c in connections:
        x1, y1 = int(landmarks[c[0]].x * w), int(landmarks[c[0]].y * h)
        x2, y2 = int(landmarks[c[1]].x * w), int(landmarks[c[1]].y * h)
        cv2.line(img, (x1, y1), (x2, y2), glow_c, 3)
        cv2.line(img, (x1, y1), (x2, y2), color, 1)
    for lm in landmarks:
        x, y = int(lm.x * w), int(lm.y * h)
        cv2.circle(img, (x, y), 5, glow_c, -1)
        cv2.circle(img, (x, y), 2, (255, 255, 255), -1)


def main():
    if not os.path.exists(MODEL_PATH):
        print("ERROR: Gesture model tidak ditemukan.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Tidak bisa membuka kamera")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        num_hands=2,
    )
    gesture_recognizer = GestureRecognizer.create_from_options(options)

    sparkles = []
    runes = []
    trails = []
    fireflies = [Firefly() for _ in range(30)]
    t = 0.0
    prev_time = time.time()
    prev_gestures = {}
    magic_alpha = 0.0
    burst_charge = 0
    canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        now = time.time()
        dt = min(now - prev_time, 0.05)
        prev_time = now
        t += dt

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (WIDTH, HEIGHT))
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = Image(image_format=ImageFormat.SRGB, data=rgb)
        result = gesture_recognizer.recognize(mp_image)

        hands_detected = False

        if result.gestures:
            for hi in range(min(len(result.gestures), 2)):
                gestures = result.gestures[hi]
                if not gestures:
                    continue
                gesture = gestures[0].category_name
                prev_g = prev_gestures.get(hi)

                landmarks = result.hand_landmarks[hi] if hi < len(result.hand_landmarks) else None
                if not landmarks:
                    continue
                hands_detected = True

                color = get_magic_color(t, hi)
                draw_hand_landmarks(frame, landmarks, WIDTH, HEIGHT, color)

                tip = landmarks[8]
                xt, yt = int(tip.x * WIDTH), int(tip.y * HEIGHT)

                if gesture != prev_g:
                    for _ in range(30):
                        sparkles.append(MagicSparkle(xt, yt, color))
                    runes.append(MagicRune(xt, yt, color))
                    burst_charge = 10

                if gesture in ('Pointing_Up', 'Open_Palm', 'None', 'ILoveYou'):
                    is_big = gesture == 'Open_Palm' or gesture == 'ILoveYou'
                    n = 5 if is_big else 2
                    for _ in range(n):
                        s = MagicSparkle(xt + random.uniform(-10, 10),
                                         yt + random.uniform(-10, 10), color)
                        s.vx = random.uniform(-3, 3)
                        s.vy = random.uniform(-5, -1)
                        s.size = random.uniform(2, 6)
                        sparkles.append(s)

                    bw = 5 if is_big else 2
                    c_glow = tuple(min(255, int(ch * 1.5)) for ch in color)
                    cv2.line(canvas, (xt, yt), (xt, yt), c_glow, bw + 2)
                    cv2.line(canvas, (xt, yt), (xt, yt), color, bw)

                    if random.random() < 0.3:
                        runes.append(MagicRune(xt, yt, color))

                    if not trails or trails[-1].color != color:
                        trails.append(MagicTrail(xt, yt, color))
                    trails[-1].add(xt, yt)
                    trails[-1].color = color

                    cv2.circle(frame, (xt, yt), 8,
                               tuple(min(255, c // 2) for c in color), -1)
                    cv2.circle(frame, (xt, yt), 4, (255, 255, 255), -1)

                if gesture == 'Closed_Fist':
                    for _ in range(40):
                        s = MagicSparkle(xt, yt, color)
                        s.vx = random.uniform(-8, 8)
                        s.vy = random.uniform(-8, 8)
                        s.size = random.uniform(3, 8)
                        sparkles.append(s)
                    canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
                    runes.clear()
                    trails.clear()

                prev_gestures[hi] = gesture

        cv2.multiply(canvas, np.array([0.985]), canvas)
        magic_alpha = min(1.0, magic_alpha + dt * 2) if hands_detected else max(0.0, magic_alpha - dt)

        for ff in fireflies:
            ff.update()
            ff.draw(frame)

        for s in sparkles[:]:
            s.update(xt if hands_detected else -1, yt if hands_detected else -1)
            if not s.draw(frame):
                sparkles.remove(s)

        for r in runes[:]:
            if not r.update():
                runes.remove(r)
            else:
                r.draw(frame)

        for tr in trails[:]:
            tr.update()
            if not tr.draw(frame):
                trails.remove(tr)

        if burst_charge > 0:
            burst_charge -= 1
            cx, cy = WIDTH // 2, HEIGHT // 2
            pulse = burst_charge / 10
            cv2.circle(frame, (cx, cy), int(20 * pulse),
                       (255, 255, 200), max(1, int(3 * pulse)))

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (WIDTH, HEIGHT), (5, 5, 15), -1)
        cv2.addWeighted(overlay, 0.08, frame, 0.92, 0, frame)

        neon = cv2.GaussianBlur(canvas, (0, 0), 5)
        frame = cv2.addWeighted(frame, 1, neon, 0.5, 0)
        frame = cv2.addWeighted(frame, 1, canvas, 0.85, 0)

        kx = cv2.getGaussianKernel(WIDTH, WIDTH * 0.35)
        ky = cv2.getGaussianKernel(HEIGHT, HEIGHT * 0.35)
        vignette = 1 - (ky / ky.max()) * (kx / kx.max()).T
        for c in range(3):
            frame[:, :, c] = (frame[:, :, c] * (1 - vignette * 0.4)).astype(np.uint8)

        cv2.putText(frame, "~ MAGIC PAINT ~", (WIDTH // 2 - 110, 35),
                    cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 100), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Sparkles:{len(sparkles)} Runes:{len(runes)}",
                    (30, 70), cv2.FONT_HERSHEY_DUPLEX, 0.4, (180, 180, 200), 1, cv2.LINE_AA)
        cv2.putText(frame, "C=Clear  ESC=Exit",
                    (30, HEIGHT - 25), cv2.FONT_HERSHEY_DUPLEX, 0.4, (120, 120, 140), 1, cv2.LINE_AA)

        cv2.imshow("Magic Paint", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break
        elif key == ord('c') or key == ord('C'):
            canvas = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
            runes.clear()
            trails.clear()
            sparkles.clear()

    gesture_recognizer.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
