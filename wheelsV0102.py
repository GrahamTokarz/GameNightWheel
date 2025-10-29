import pygame
import math
import random
import json
import time
import requests

start_time = time.time()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True
dt = 0

#Job Wheel

wheel_colors = ["#db7dc1", "#dbd77d", "#7d85db"]
wheel_radius = 425
wheel_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 - 30)

beginnerV2 = False
wheelWheelSpins = 0
wheelWheelV2 = False
cigarSpins = 0

wheel_files = [
    'beginnerWheel', 'wheelWheel', 'goodIdeaWheel', 'gameWheel',
    'iMadeThisLastWeekWheel', 'discussionWheel', 'cheeseWheel',
    'chaoticWheelWheel', 'jailWheel', 'toasterWheel', 'burglaryWheel',
    'gravelWheel', 'amazonReviewsWheel', 'thunderSpellWheel', 'secretWheel', 'spaghetWheel',
    'eightBallWheel', 'subwheelsWheel', 'wheelWheelWheel', 'wheelWheel3', 'pointsWheel',
    'doomWheel', 'cigarWheel', 'wordGameWheel', 'forbiddenWordsWheel'
]

wheel_names = [
    'Beginner Wheel', 'Wheel Wheel', 'Good Idea Wheel', 'Game Wheel',
    'I Made This Last Week Wheel', 'Discussion Wheel', 'Cheese Wheel',
    'Chaotic Wheel Wheel', 'Jail Wheel', 'Toaster Wheel', 'Burglary Wheel',
    'Gravel Wheel', 'Amazon Reviews Wheel', 'Thunder Spell Wheel', 'Secret Wheel', 'Spaghet Wheel',
    'Eight Ball Wheel', 'Subwheels Wheel', 'Wheel Wheel Wheel', 'Wheel Wheel 3', 'Points Wheel',
    'Doom Wheel', 'Cigar Wheel', 'Word Game Wheel', 'Forbidden Words Wheel'
]

wheelLabels = {}
for i in range(len(wheel_files)):
    with open(f"wheelsV0.2/{wheel_files[i]}.json") as f:
        data = json.load(f)
        wheelLabels[wheel_names[i]] = [data[str(i)] for i in range(1, len(data)+1)]

wheel_options = random.sample(wheelLabels['Beginner Wheel'], k=len(wheelLabels['Beginner Wheel']))
wheel_slices = len(wheel_options)
wheel_divisions = len(wheel_options)
slice_size = 360 / wheel_divisions

spinning = False
needAccept = False
needSkongAccept = False

wheel_tick = pygame.mixer.Sound("spinSounds/dnk.mp3")
jingle = pygame.mixer.Sound("spinSounds/truck.mp3")
fart = pygame.mixer.Sound("jingles/fart.mp3")

lastTick = 0
triRot = 0

spin_duration = 8
full_rots = 6
min_spin_time = 5
spin_time = 0
angle = 0
pointer_angle = 0
target_angle = 0
final_angle = 0
start_angle = 0
winning_slice = 0
slice_boundaries = []

total_spins = 0
vicotryPoinet = 0
cheesePoints = 2

button_rect = pygame.Rect(0, 0, 100, 60)
button_rect.center = (screen.get_width() / 2, (screen.get_height() / 2) + 450)

counter_rect = pygame.Rect(0, 0, 100, 60)
counter_rect.midleft = (25, 25)

vicotry_rect = pygame.Rect(0, 0, 100, 60)
vicotry_rect.midright = (screen.get_width() - 25, 25)

cigar_rect = pygame.Rect(0, 0, 100, 60)
cigar_rect.midright = (screen.get_width() - 25, 75)

accept_rect = pygame.Rect(0, 0, screen.get_width() - 100, screen.get_height() / 3)
accept_rect.center = (screen.get_width() / 2, screen.get_height() / 2)

jail_rect = pygame.Rect(0, 0, 100, 0)
jail_rect.center = (screen.get_width() / 2, 25)

showDuration = False
timer_rect = pygame.Rect(0, 0, 100, 0)
timer_rect.midleft = (25, 75)

cheese_rect = pygame.Rect(0, 0, 100, 60)
cheese_rect.midleft = (65, 125)

skongCounter = False
skongDuration = 0
hasntSkonged = True

fishgifindex = 0
fishgifon = False

swsfindex = 0
swsfon = False

jailLevel = 1

zeepleMode = False
needZeepleAccept = False

milkTime = False

lastWheelOptions = []
lastSpinResult = ""
unmodifiedLastSpinResult = False

def changeWheel(wheel):
    global wheel_slices
    global wheel_options
    global wheel_divisions
    global jingle
    
    wheelLabels[wheel_options[0]["wheelName"]] = wheel_options
    
    wheel_options = random.sample(wheel, k=len(wheel))
    wheel_slices = len(wheel_options)
    wheel_divisions = 0
    
    pygame.display.set_caption(wheel_options[0]["wheelName"])
    icon_image = pygame.image.load(f"imgs/{wheel_options[0]["wheelName"]}.png")
    pygame.display.set_icon(icon_image)
    jingle = pygame.mixer.Sound(f"jingles/{wheel_options[0]["wheelName"]}.mp3")
    
    for i in range(wheel_slices):
        wheel_divisions += wheel_options[i]["sizeMult"]
        
changeWheel(wheelLabels['I Made This Last Week Wheel'])

# Precomputed graphics cache
precomputed_wheel = []

def prepare_wheel_graphics(wheel_options):
    """Precompute slice polygons and text surfaces."""
    global slice_size
    slice_size = 360 / wheel_divisions
    usedDivisions = 0
    precomputed = []

    for i, opt in enumerate(wheel_options):
        start_angle = slice_size * usedDivisions
        end_angle = start_angle + slice_size * opt["sizeMult"]
        usedDivisions += opt["sizeMult"]

        # Polygon points
        points = [wheel_pos]
        steps = 40
        for j in range(steps + 1):
            a = math.radians(start_angle + (end_angle - start_angle) * j / steps)
            x = wheel_pos.x + (wheel_radius * math.cos(a))
            y = wheel_pos.y + (wheel_radius * math.sin(a))
            points.append(pygame.Vector2(x, y))

        # Determine color
        color = opt["specialColor"] if opt.get("specialColor") else wheel_colors[i % len(wheel_colors)]

        # Pre-render label surface
        font_size = 42
        if len(opt["label"]) >= 15:
            font_size = 30
        if len(opt["label"]) >= 20:
            font_size = 22
        font = pygame.font.Font(None, font_size)
        label_surf = font.render(opt["label"], True, "#000000")
        mid_angle = math.radians(start_angle + (end_angle - start_angle) / 2)
        label_x = wheel_pos.x + (wheel_radius * 0.7 * math.cos(mid_angle))
        label_y = wheel_pos.y + (wheel_radius * 0.7 * math.sin(mid_angle))
        label_rect = label_surf.get_rect(center=(label_x, label_y))

        precomputed.append({
            "points": points,
            "color": color,
            "label_surf": label_surf,
            "label_rect": label_rect,
            "mid_angle": mid_angle
        })
    return precomputed

def draw_wheel(surface, angle):
    global lastWheelOptions, precomputed_wheel, unmodifiedLastSpinResult

    if lastWheelOptions != wheel_options or unmodifiedLastSpinResult:
        try:
            requests.post(
                "https://hack-box.vercel.app/wheelPOSTOFFICE",
                json={"wo": wheel_options, "last": lastSpinResult},
                headers={'Content-Type': 'application/json'}
            )
        except:
            pass

        precomputed_wheel = prepare_wheel_graphics(wheel_options)
        lastWheelOptions = wheel_options.copy()
        unmodifiedLastSpinResult = False

    for i, slice_data in enumerate(precomputed_wheel):
        rotated_points = []
        for p in slice_data["points"]:
            dx, dy = p.x - wheel_pos.x, p.y - wheel_pos.y
            rad = math.radians(angle)
            x = wheel_pos.x + dx * math.cos(rad) - dy * math.sin(rad)
            y = wheel_pos.y + dx * math.sin(rad) + dy * math.cos(rad)
            rotated_points.append((x, y))

        pygame.draw.polygon(surface, slice_data["color"], rotated_points)

        mid_angle = slice_data["mid_angle"] + math.radians(angle)
        label_x = wheel_pos.x + (wheel_radius * 0.7 * math.cos(mid_angle))
        label_y = wheel_pos.y + (wheel_radius * 0.7 * math.sin(mid_angle))
        rotated_label = pygame.transform.rotate(slice_data["label_surf"], -math.degrees(mid_angle))
        rect = rotated_label.get_rect(center=(label_x, label_y))
        surface.blit(rotated_label, rect)
        
def draw_spin_button(surface):
    pygame.draw.rect(surface, "#FFFFFF", button_rect, border_radius=12)
    font = pygame.font.Font(None, 42)
    text_surf = font.render("SPIN", True, "#000000")
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    
def draw_accept(surface):
    if skongCounter and hasntSkonged:
        skongDuration += random.randint(1, 10)
    
    font = pygame.font.Font(None, 200)
    toDisp = wheel_options[winning_slice]["label"]
    if (wheel_options[winning_slice]["full"]):
        toDisp = wheel_options[winning_slice]["full"]
    if (len(toDisp) > 8):
        font = pygame.font.Font(None, 100)
    if (len(toDisp) > 20):
        font = pygame.font.Font(None, 90)
    if (len(toDisp) > 30):
        font = pygame.font.Font(None, 50)
        
    pygame.draw.rect(surface, "#9EC2C8", accept_rect, border_radius=12)
    text_surf = font.render(toDisp, True, "#000000")
    text_rect = text_surf.get_rect(center=accept_rect.center)
    surface.blit(text_surf, text_rect)
    font = pygame.font.Font(None, 42)
    
def draw_skong_accept(surface):    
    toDisp = f"Skong For {skongDuration} Seconds!"
    font = pygame.font.Font(None, 80)
        
    pygame.draw.rect(surface, "#9EC2C8", accept_rect, border_radius=12)
    text_surf = font.render(toDisp, True, "#000000")
    text_rect = text_surf.get_rect(center=accept_rect.center)
    surface.blit(text_surf, text_rect)
    font = pygame.font.Font(None, 42)
    
def draw_zeeple_accept(surface):    
    toDisp = f"ZEEPLE DOME TIME!"
    font = pygame.font.Font(None, 80)
        
    pygame.draw.rect(surface, "#9EC2C8", accept_rect, border_radius=12)
    text_surf = font.render(toDisp, True, "#000000")
    text_rect = text_surf.get_rect(center=accept_rect.center)
    surface.blit(text_surf, text_rect)
    font = pygame.font.Font(None, 42)
    
def draw_milk_accept(surface):    
    toDisp = f"2 MINUTE MILK BREAK!!"
    font = pygame.font.Font(None, 80)
        
    pygame.draw.rect(surface, "#9EC2C8", accept_rect, border_radius=12)
    text_surf = font.render(toDisp, True, "#000000")
    text_rect = text_surf.get_rect(center=accept_rect.center)
    surface.blit(text_surf, text_rect)
    font = pygame.font.Font(None, 42)
    
def draw_counter(surface):
    font = pygame.font.Font(None, 42)
    pygame.draw.rect(surface, "#b2bfb5", counter_rect, border_radius=12)
    text_surf = font.render(f"Spin Count: {total_spins}", True, "#000000")
    text_rect = text_surf.get_rect(midleft=counter_rect.midleft)
    surface.blit(text_surf, text_rect)
    
def draw_cigar_count(surface):
    font = pygame.font.Font(None, 42)
    pygame.draw.rect(surface, "#b2bfb5", cigar_rect, border_radius=12)
    text_surf = font.render(f"{cigarSpins} cigars", True, "#000000")
    text_rect = text_surf.get_rect(midright=cigar_rect.midright)
    surface.blit(text_surf, text_rect)

def draw_vicotry(surface):
    font = pygame.font.Font(None, 42)
    pygame.draw.rect(surface, "#b2bfb5", vicotry_rect, border_radius=12)
    text_surf = font.render(f"Vicotry Poinets: {vicotryPoinet}", True, "#000000")
    text_rect = text_surf.get_rect(midright=vicotry_rect.midright)
    surface.blit(text_surf, text_rect)

def draw_jail(surface):
    font = pygame.font.Font(None, 42)
    pygame.draw.rect(surface, "#b2bfb5", jail_rect, border_radius=12)
    text_surf = font.render(f"Jail Level: {jailLevel}", True, "#9F0000")
    text_rect = text_surf.get_rect(center=jail_rect.center)
    surface.blit(text_surf, text_rect)
    
def draw_timer(surface):
    timer_duration = int(time.time() - start_time)
    timer_hours = timer_duration // 3600
    timer_minutes = (timer_duration % 3600) // 60
    timer_seconds = timer_duration % 60
    timer_text = f"{timer_hours:02}:{timer_minutes:02}:{timer_seconds:02}"
    
    font = pygame.font.Font(None, 42)
    pygame.draw.rect(surface, "#b2bfb5", timer_rect, border_radius=12)
    text_surf = font.render(timer_text, True, "#000000")
    text_rect = text_surf.get_rect(center=timer_rect.center)
    surface.blit(text_surf, text_rect)
    
def draw_cheese(surface):
    font = pygame.font.Font(None, 42)
    pygame.draw.rect(surface, "#b2bfb5", cheese_rect, border_radius=12)
    text_surf = font.render(f"Cheese Points: {cheesePoints}", True, "#927F05")
    text_rect = text_surf.get_rect(center=cheese_rect.center)
    surface.blit(text_surf, text_rect)
    
def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)

def compute_boundaries():
    boundaries = []
    total = 0
    for opt in wheel_options:
        start_angle = total
        end_angle = start_angle + opt["sizeMult"] * slice_size
        boundaries.append(end_angle % 360.0)
        total = end_angle
    return boundaries
    
def check_tick(prev_angle, new_angle):
    for boundary in slice_boundaries:
        if prev_angle > boundary >= new_angle:
            return True
        if new_angle > prev_angle and (boundary <= prev_angle or boundary > new_angle):
            return True
    return False
        
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if needSkongAccept and accept_rect.collidepoint(event.pos):
                needSkongAccept = False
                skongDuration = 0
            elif needZeepleAccept and accept_rect.collidepoint(event.pos):
                needZeepleAccept = False
            elif milkTime and accept_rect.collidepoint(event.pos):
                milkTime = False
            elif needAccept and accept_rect.collidepoint(event.pos):
                winning_op = wheel_options[winning_slice]
                if (winning_op["removeFromWheel"] == 1):
                    wheel_slices -= 1
                    wheel_divisions -= winning_op["sizeMult"]
                    wheel_options.pop(winning_slice)
                else:
                    unmodifiedLastSpinResult = True
                
                if (total_spins == 5):
                    wheel_options.insert(1, {
                        "label": "Wheel Wheel",
                        "full": "GO TO THE WHEEL WHEEL!",
                        "sizeMult": 4,
                        "winMult": 2,
                        "removeFromWheel": 0,
                        "goToWheel": "Wheel Wheel",
                        "specialEffect": "newBeginnerWheel",
                        "specialColor": "#EE8C4B",
                        "wheelName": "Beginner Wheel"
                    })
                    wheel_divisions += 4
                    wheel_slices += 1
                    
                if (total_spins == 20):
                    showDuration = True
                    
                if (wheelWheelSpins == 3 and not wheelWheelV2):
                    wheelWheelV2 = True
                    wheel_options.insert(1, {
                        "label": "Good Idea Wheel",
                        "full": "I HAVE AN IDEA!!",
                        "sizeMult": 1,
                        "winMult": 2,
                        "removeFromWheel": 0,
                        "goToWheel": "Good Idea Wheel",
                        "specialEffect": None,
                        "specialColor": "#F0F0F0",
                        "wheelName": "Wheel Wheel"
                    })
                    wheel_options.insert(1, {
                        "label": "Wheel Wheel... 2?",
                        "full": "Where things are slightly more chaotic.",
                        "sizeMult": 1,
                        "winMult": 3,
                        "removeFromWheel": 0,
                        "goToWheel": "Chaotic Wheel Wheel",
                        "specialEffect": None,
                        "specialColor": "#BB6A29",
                        "wheelName": "Wheel Wheel"
                    })
                    
                if (winning_op["goToWheel"]):
                    changeWheel(wheelLabels[winning_op["goToWheel"]])
                    
                if (winning_op["specialEffect"]):
                    eff = winning_op["specialEffect"]
                    
                    if eff == "changeTick":
                        wheelTickSounds = ["dnk", "doorclose", "many", "oof", "oOGo", "Ooo", "ptDrum", "thump", "tick", "truck"]
                        wheel_tick = pygame.mixer.Sound(f"spinSounds/{random.choice(wheelTickSounds)}.mp3")
                    
                    elif eff == "toggleSkong":
                        skongCounter = not skongCounter
                        
                    elif eff == "ShowSKONGCounter":
                        needSkongAccept = True
                        
                    elif eff == "vicotryPoinet":
                        vicotryPoinet += 1
                        
                    elif eff == "velocity":
                        min_spin_time += 2
                        full_rots += 4
                        
                    elif eff == "newBeginnerWheel" and not beginnerV2:
                        beginnerV2 = True
                        wheelLabels["Beginner Wheel"].insert(1, {
                            "label": "Kahoot!",
                            "full": "Play a random Kahoot!",
                            "sizeMult": 1,
                            "winMult": 1,
                            "removeFromWheel": 1,
                            "goToWheel": None,
                            "specialEffect": None,
                            "specialColor": None,
                            "wheelName": "Beginner Wheel"
                        })
                        wheelLabels["Beginner Wheel"].insert(1, {
                            "label": "Random Discussion Topic!",
                            "full": "Discuss the following for 1 minute:",
                            "sizeMult": 1,
                            "winMult": 1,
                            "removeFromWheel": 0,
                            "goToWheel": "Discussion Wheel",
                            "specialEffect": None,
                            "specialColor": None,
                            "wheelName": "Beginner Wheel"
                        })
                        wheelLabels["Beginner Wheel"].insert(1, {
                            "label": "Venmo Simon",
                            "full": "Venmo Simon $1 (@simondaug)",
                            "sizeMult": 1,
                            "winMult": 1,
                            "removeFromWheel": 1,
                            "goToWheel": None,
                            "specialEffect": None,
                            "specialColor": None,
                            "wheelName": "Beginner Wheel"
                        })
                        wheelLabels["Beginner Wheel"].insert(1, {
                            "label": "Do Do Re Mi", 
                            "full": None,
                            "sizeMult": 1,
                            "winMult": 1,
                            "removeFromWheel": 1,
                            "goToWheel": None,
                            "specialEffect": None,
                            "specialColor": None,
                            "wheelName": "Beginner Wheel"
                        })
                
                    elif eff == "jailMinus":
                        if (jailLevel == 1):
                            changeWheel(wheelLabels["Chaotic Wheel Wheel"])
                        else:
                            jailLevel -= 1
                            
                    elif eff == "jailPlus":
                        jailLevel += 1
                        
                    elif eff == "zeepleSlice":
                        zeepleMode = True
                        
                    elif eff == "cheesePoint":
                        cheesePoints += 1
                        if cheesePoints % 3 == 0:
                            changeWheel(wheelLabels["Cheese Wheel"])
                    
                    elif eff == "addJonDM":
                        wheelLabels["Game Wheel"].insert(1, {
                        "label": "Jon DM",
                        "full": "Jon DMs a Pokemon Mystery Dungeon Thing",
                        "sizeMult": 1,
                        "winMult": 1,
                        "removeFromWheel": 0,
                        "goToWheel": None,
                        "specialEffect": None,
                        "specialColor": None,
                        "wheelName": "Game Wheel"
                    })
                        
                    elif eff == "hiddenAchievement":
                        vicotryPoinet += 5
                else:
                    if total_spins > 15 and random.randint(1, 20) == 5:
                        milkTime = True
                needAccept = False
            elif not needAccept and not needSkongAccept and not spinning and button_rect.collidepoint(event.pos):
                hasntSkonged = True
                
                if (wheel_options[0]["wheelName"] == "Wheel Wheel"):
                    wheelWheelSpins += 1
                if (wheel_options[0]["wheelName"] == "Cigar Wheel"):
                    cigarSpins += 1

                spinning = True
                total_spins += 1
                
                spin_duration = random.uniform(min_spin_time, min_spin_time + 2)
                spin_time = 0
                slice_boundaries = compute_boundaries()
                
                weights = [opt["winMult"] for opt in wheel_options]
                winning_slice = random.choices(range(len(wheel_options)), weights=weights, k=1)[0]
                lastSpinResult = wheel_options[winning_slice]["label"]
                
                slice_start_angle = sum(opt["sizeMult"] * slice_size for opt in wheel_options[:winning_slice])
                slice_span = wheel_options[winning_slice]["sizeMult"] * slice_size
                target_angle = (slice_start_angle + slice_span * random.uniform(0.1, 0.9)) % 360
                
                delta_to_align = (270 - target_angle) % 360
                final_angle = full_rots * 360 + delta_to_align - angle
                start_angle = angle
                
    if spinning:
        spin_time += dt

        t = min(spin_time / spin_duration, 1.0)  # normalize 0 → 1
        progress = ease_out_cubic(t)

        angle = (start_angle + progress*final_angle) % 360
        
        prev_angle = pointer_angle
        pointer_angle = (-angle - 90) % 360        
        current_tick = int(pointer_angle // slice_size) % wheel_slices
        
        if check_tick(prev_angle, pointer_angle):
            if (wheel_options[current_tick]["label"] == "Play a Fart Sound"):
                fart.play()
            else:
                wheel_tick.play()
            triRot = 30
        
        if t >= 1:
            spinning = False
            needAccept = True
            if (zeepleMode):
                if random.randint(1, 100) == 100:
                    needZeepleAccept = True
                    needAccept = False
            jingle.play()
        
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("#b2bfb5")

    # RENDER YOUR GAME HERE
    draw_wheel(screen, angle)
        
    pointer_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.polygon(pointer_surface, (255,255,255), [(10, 0), (50, 0), (30, 40)])
    pointer_vertices = pygame.transform.rotate(pointer_surface, triRot)
    if (triRot > 0): triRot -= 5
    pointer_rec = pointer_vertices.get_rect(center=(wheel_pos.x, wheel_pos.y - 425))
    screen.blit(pointer_vertices, pointer_rec)
    
    if not spinning and not needAccept and not needSkongAccept and not needZeepleAccept and not milkTime:
        draw_spin_button(screen)
    if needAccept:
        draw_accept(screen)
    if needSkongAccept:
        draw_skong_accept(screen)
    if needZeepleAccept:
        draw_zeeple_accept(screen)
    if milkTime:
        draw_milk_accept(screen)
    if total_spins >= 3:
        draw_counter(screen)
    if cigarSpins >= 1:
        draw_cigar_count(screen)
    if vicotryPoinet >= 1:
        draw_vicotry(screen)
    if vicotryPoinet >= 0:
        draw_cheese(screen)
    if showDuration:
        draw_timer(screen)
    
    if (wheel_options[0]["wheelName"] == "Jail Wheel"):
        draw_jail(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    dt = clock.tick(60) / 1000 # limits FPS to 60

pygame.quit()