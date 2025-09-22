# -*- coding: utf-8 -*-
import pygame
import sys
import json

pygame.init()
pygame.mixer.init()

# --- Config ---
WIDTH, HEIGHT = 600, 800
LANES = 3
LANE_WIDTH = WIDTH // LANES
NOTE_WIDTH, NOTE_HEIGHT = LANE_WIDTH - 20, 30
NOTE_SPEED = 5

HIT_ZONE_Y = HEIGHT - 100
HIT_ZONE_HEIGHT = 20
HIT_CENTER = HIT_ZONE_Y + HIT_ZONE_HEIGHT // 2

# Hit windows
PERFECT_WINDOW = 10
GOOD_WINDOW = 30
MAX_HIT_WINDOW = 60

# Fail condition
MAX_MISSES = 10

# --- Setup ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Drum Hero")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Colors
COLORS = [(255, 80, 80), (255, 230, 80), (80, 160, 255)]

# Keys (R, H, B)
LANE_KEYS = {
    pygame.K_5: 0,
    pygame.K_6: 1,
    pygame.K_7: 2,
}

# --- Game states ---
MENU, PLAYING, GAME_OVER, RECORDING = "menu", "playing", "game_over", "recording"
state = MENU

# --- Game variables ---
notes = []
score = 0
misses = 0
paused = False
judgement_text = ""
judgement_time = 0
JUDGEMENT_DURATION_MS = 700

note_chart = []
note_index = 0
recorded_notes = []


def reset_game():
    """Reset gameplay variables and start song."""
    global notes, score, misses, paused, judgement_text, state, note_index
    notes = []
    score = 0
    misses = 0
    paused = False
    judgement_text = ""
    note_index = 0
    state = PLAYING

    # load + play song
    pygame.mixer.music.load("song1.mp3")
    pygame.mixer.music.play()

    # load chart from file
    try:

        global note_chart
        with open("recorded_chart.json", "r") as f:
            note_chart = json.load(f)

    except FileNotFoundError:
        print("No chart1.json found. Using empty chart.")
        note_chart = []


def start_recording():
    """Start recording mode."""
    global recorded_notes, state
    recorded_notes = []
    state = RECORDING
    pygame.mixer.music.load("song1.mp3")
    pygame.mixer.music.play()
    print("Recording started! Tap R, H, B to add notes. Press SPACE to stop and save.")


def save_recording():
    """Save the recorded chart to JSON."""
    with open("recorded_chart.json", "w") as f:
        json.dump(recorded_notes, f, indent=2)
    print("Recording finished! Saved to recorded_chart.json")


def spawn_note_lane(lane):
    rect = pygame.Rect(lane * LANE_WIDTH + 10, -NOTE_HEIGHT, NOTE_WIDTH, NOTE_HEIGHT)
    notes.append({'rect': rect, 'lane': lane, 'color': COLORS[lane]})


def draw_hit_zone():
    for i in range(LANES):
        x = i * LANE_WIDTH
        pygame.draw.rect(screen, (255, 255, 255),
                         (x, HIT_ZONE_Y, LANE_WIDTH, HIT_ZONE_HEIGHT), 2)
    pygame.draw.line(screen, (200, 200, 200),
                     (0, HIT_CENTER), (WIDTH, HIT_CENTER), 1)


def handle_hit(lane):
    global score, judgement_text, judgement_time
    candidates = [n for n in notes if n['lane'] == lane]
    if not candidates:
        return None

    def distance_to_center(n):
        note_bottom = n['rect'].y + NOTE_HEIGHT
        return abs(note_bottom - HIT_CENTER)

    closest = min(candidates, key=distance_to_center)
    dist = distance_to_center(closest)

    if dist <= PERFECT_WINDOW:
        score += 100
        notes.remove(closest)
        judgement_text = "Perfect!"
    elif dist <= GOOD_WINDOW:
        score += 60
        notes.remove(closest)
        judgement_text = "Good"
    elif dist <= MAX_HIT_WINDOW:
        score += 20
        notes.remove(closest)
        judgement_text = "Ok"
    else:
        return None

    judgement_time = pygame.time.get_ticks()
    return judgement_text


def draw_judgement():
    if judgement_text and pygame.time.get_ticks() - judgement_time < JUDGEMENT_DURATION_MS:
        jt = big_font.render(judgement_text, True, (255, 255, 255))
        jt_rect = jt.get_rect(center=(WIDTH // 2, HEIGHT - 150))
        screen.blit(jt, jt_rect)


def draw_hud():
    score_surf = font.render(f"Score: {score}", True, (230, 230, 230))
    screen.blit(score_surf, (10, 10))
    miss_surf = font.render(f"Misses: {misses}/{MAX_MISSES}", True, (230, 100, 100))
    screen.blit(miss_surf, (WIDTH - 250, 10))


# --- Main loop ---
running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # MENU
        if state == MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()

        # PLAYING
        elif state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_p, pygame.K_SPACE):
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    continue
                if event.key == pygame.K_r and paused:
                    start_recording()
                if event.key in LANE_KEYS and not paused:
                    lane = LANE_KEYS[event.key]
                    handle_hit(lane)

        # RECORDING
        elif state == RECORDING:
            if event.type == pygame.KEYDOWN:
                if event.key in LANE_KEYS:
                    lane = LANE_KEYS[event.key]
                    t = pygame.mixer.music.get_pos()
                    recorded_notes.append({"time": t, "lane": lane})
                    print(f"Note recorded at {t} ms, lane {lane}")
                elif event.key == pygame.K_SPACE:
                    save_recording()
                    state = MENU
                    pygame.mixer.music.stop()

        # GAME OVER
        elif state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

    # --- Update ---
    if state == PLAYING and not paused:
        current_time = pygame.mixer.music.get_pos()
        while note_index < len(note_chart) and current_time >= note_chart[note_index]["time"]:
            spawn_note_lane(note_chart[note_index]["lane"])
            note_index += 1

        for n in notes[:]:
            n['rect'].y += NOTE_SPEED
            if n['rect'].y > HEIGHT:
                notes.remove(n)
                misses += 1
                judgement_text = "Miss"
                judgement_time = pygame.time.get_ticks()
                if misses >= MAX_MISSES:
                    state = GAME_OVER
                    pygame.mixer.music.stop()

    # --- Draw ---
    screen.fill((12, 12, 12))

    if state == MENU:
        title = big_font.render("Mini Drum Hero", True, (255, 255, 255))
        t_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(title, t_rect)
        instr = font.render("Press ENTER to start", True, (200, 200, 200))
        i_rect = instr.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(instr, i_rect)

    elif state == PLAYING:
        for n in notes:
            pygame.draw.rect(screen, n['color'], n['rect'])
        draw_hit_zone()
        draw_hud()
        draw_judgement()

        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            ptext = big_font.render("PAUSED", True, (255, 255, 255))
            pr = ptext.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(ptext, pr)
            rtext = font.render("Press R to Record", True, (200, 200, 200))
            rr = rtext.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            screen.blit(rtext, rr)

    elif state == RECORDING:
        rec_text = big_font.render("RECORDING", True, (255, 80, 80))
        rec_rect = rec_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(rec_text, rec_rect)

    elif state == GAME_OVER:
        over = big_font.render("GAME OVER", True, (255, 80, 80))
        o_rect = over.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(over, o_rect)

        score_txt = font.render(f"Score: {score}", True, (230, 230, 230))
        s_rect = score_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(score_txt, s_rect)

        miss_txt = font.render(f"Misses: {misses}/{MAX_MISSES}", True, (230, 100, 100))
        m_rect = miss_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        screen.blit(miss_txt, m_rect)

        restart_txt = font.render("Press ENTER to Restart, ESC to Quit", True, (200, 200, 200))
        r_rect = restart_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
        screen.blit(restart_txt, r_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
