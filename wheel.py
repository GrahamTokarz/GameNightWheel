import pygame
import math
import random
import json
import time
import requests
from datetime import datetime

start_time = time.time()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1000, 1000))
clock = pygame.time.Clock()
running = True
dt = 0

#region File Handler

# --- THE PATHS OF THESE SHOULD BE UPDATED WEEKLY, OR I CAN NOT BE A DUMBASS AND JUST USE THE MAIN WHEELS FOLDER. WE'LL SEE ---
allSlices = {}
with open("wheelsV0.4/allSlices.json") as f:
    allSlices = json.load(f)
    # print(allSlices)
    
allPastSlices = {}
with open("wheelsV0.4/allPastSlices.json") as f:
    allPastSlices = json.load(f)
    # print(allSlices)
        
def match_keys_to_ids(data):
    for key, value in list(data.items()):
        if key != value["id"]:
            print(f"ERROR AT {key}")

match_keys_to_ids(allSlices)
match_keys_to_ids(allPastSlices)

jbLabels = ["JBP1G1", "JBP1G2", "JBP1G3", "JBP1G4", "JBP1G5",
            "JBP2G1", "JBP2G2", "JBP2G3", "JBP2G4", "JBP2G5",
            "JBP3G1", "JBP3G2", "JBP3G3", "JBP3G4", "JBP3G5",
            "JBP4G1", "JBP4G2", "JBP4G3", "JBP4G4", "JBP4G5",
            "JBP5G1", "JBP5G2", "JBP5G3", "JBP5G4", "JBP5G5",
            "JBP6G1", "JBP6G2", "JBP6G3", "JBP6G4", "JBP6G5",
            "JBP7G1", "JBP7G2", "JBP7G3", "JBP7G4", "JBP7G5",
            "JBP8G1", "JBP8G2", "JBP8G3", "JBP8G4", "JBP8G5",
            "JBP9G1", "JBP9G2", "JBP9G3", "JBP9G4", "JBP9G5",
            "JBP10G1", "JBP10G2", "JBP10G3", "JBP10G4", "JBP10G5",
            "JBPSG1", "JBPSG2", "JBP4G1.5", "JBP9G1.5", "JBP9G5.5"]
    
WHEEL_LOADER = {
    "Low Rated Jackbox Wheel": 'jackboxWheels/lowRated',
    "Mid Rated Jackbox Wheel": "jackboxWheels/midRated",
    "High Rated Jackbox Wheel": "jackboxWheels/highRated",
    "Jackbox Trivia Games Wheel": "jackboxWheels/triviaGames",
    "Jackbox Drawing Games Wheel": "jackboxWheels/drawingGames",
    "Jackbox Prompt Games Wheel": "jackboxWheels/promptGames",
    "Jackbox Arcade Games Wheel": "jackboxWheels/arcadeGames",
    "Jackbox Coinflip Wheel": "jackABWheel",
    "Jackbox Types Wheel": "JackAWheel",
    "Jackbox Ratings Wheel": "jackBWheel",
    "Eight Ball Wheel": "eightBallWheel",
    "Secret Wheel": "secretWheel",
    "Beginner Wheel": "beginnerWheel",
    "Who's Paying Wheel": "whoPayingWheel",
    "How Much Wheel": "howMuchWheel",
    "Physical Activity Wheel": "physicalActivityWheel",
    "End Wheel Night Wheel": "endWheelNightWheel",
    "Wheel Wheel": "wheelWheel",
    # "America Wheel": "americaWheel",
    "Points Wheel": "pointsWheel",
    
    "Spider Man Wheel": "spiderManWheel",
    "Salivation Wheel": "salivationWheel",
    "Smacky Scissors Wheel": "smackyScissorsWheel",
    "Goop Wheel": "goopWheel",
    "This Wheel is Circular": "thisWheelIsCircular",
    
    "David Dance Wheel": "davidDanceWheel",
    "Decision Paralysis Wheel": "decisionParalysisWheel",
    "200 Ball Wheel": "twohundredBallWheel",
    "IO Wheel": "ioWheel"
    
    
    
    # "All Queued Wheels": "allQueuedWheels",
}

wheelLabels = {}
for key in WHEEL_LOADER:
    with open(f"wheelsV0.4/{WHEEL_LOADER[key]}.json") as f:
        wheelProperties = json.load(f)
        merged_dict = []

        for k in wheelProperties:
            if (k[0:7] == "JBAdder"):
                merged = {"winMult": 1, "sizeMult": 1, "removeFromWheel": 1}
                merged.update(allSlices.get(random.choice(jbLabels), {}))
                merged_dict.append(merged)
            else:
                merged = wheelProperties.get(k, {}).copy()
                merged.update(allSlices.get(k, {}))
                merged_dict.append(merged)

        wheelLabels[key] = merged_dict
        
merged_dict = []
for k in allPastSlices:
    # print(k)
    merged = {"winMult": 1, "sizeMult": 1, "removeFromWheel": 1}
    merged.update(allPastSlices.get(k, {}))
    merged_dict.append(merged)
wheelLabels["Past Slice Wheel"] = merged_dict
        
QUEUED_WHEELS = {
    # "Cigar Wheel": {"name": "cigarWheel", "size": 6},
    # "Everyone's Favorite Wheel": {"name": "everyonesFavoriteWheel", "size": 7},
    # "Ceaseless Watcher Wheel": {"name": "ceaselessWatcherWheel", "size": 6},
    # "Everyone's Actual Favorite Wheel": {"name": "everyonesFavoriteFrWheel", "size": 15},
}

wheelQueues = {}
def nextFromQueue(label):
    return wheelQueues[label].pop(0)

for key in QUEUED_WHEELS:
    with open(f"wheelsV0.4/{QUEUED_WHEELS[key]["name"]}.json") as f:
        wheelProperties = json.load(f)
        merged_dict = []
        wheel_builder = []

        for k in wheelProperties:
            merged = wheelProperties.get(k, {}).copy()
            merged.update(allSlices.get(k, {}))
            merged_dict.append(merged)

        wheelQueues[key] = random.sample(merged_dict, k=len(merged_dict))
        
        wheel_builder = wheelLabels["All Queued Wheels"].copy()
        while (len(wheel_builder) < QUEUED_WHEELS[key]["size"]):
            wheel_builder.append(nextFromQueue(key))
        wheelLabels[key] = wheel_builder
            
print(*(len(wheelLabels[k]) for k in wheelLabels))
#endregion

#region Function Variables
lastWheel = "Beginner Wheel"
currentWheel = "Beginner Wheel"
callbackWheel = "Beginner Wheel"

wheel_options = random.sample(wheelLabels[lastWheel], k=len(wheelLabels[lastWheel]))
wheel_slices = len(wheel_options)
wheel_divisions = len(wheel_options)
slice_size = 360 / wheel_divisions

spinning = False
needAccept = False

wheel_tick = pygame.mixer.Sound("spinSounds/dnk.mp3")
jingle = pygame.mixer.Sound("spinSounds/truck.mp3")
fart = pygame.mixer.Sound("jingles/fart.mp3")
america_tick = pygame.mixer.Sound("spinSounds/rifleShot.mp3")

lastTick = 0
triRot = 0

spin_duration = 8
full_rots = 6
min_spin_time = 5
spin_time = 0
spinDirection = 1
angle = 0
pointer_angle = 0
target_angle = 0
final_angle = 0
start_angle = 0
winning_slice = 0
slice_boundaries = []

total_spins = 0
wheelWheelSpins = 0
beginnerSpins = 0
cigars = 0

lastWheelOptions = []
lastSpinResult = ""
unmodifiedLastSpinResult = False

seenSlices = allPastSlices.copy()

zeepleSlice = False
endingAdded = False
wheelWheelV2 = False
mlpDraw = False
mlpDone = False

confetti = True

loadBar = False
loading_width = 0

rickroll = False
songPlaying = False
TOTAL_FRAMES = 12785
FRAME_DURATION = 1.0 / 60
FRAME_FOLDER = ""
CACHE_LIMIT = 300  # adjust to control memory usage

frame_index = 1
elapsed_time = 0
frame_cache = {}

def load_frame(index):
    if index in frame_cache:
        return frame_cache[index]

    frame_path = f"rickroll/frames/frame_{index:04d}.jpg"
    img = pygame.image.load(frame_path).convert()
    frame_cache[index] = img

    if len(frame_cache) > CACHE_LIMIT:
        oldest = min(frame_cache.keys())
        del frame_cache[oldest]

    return img

rrSong = pygame.mixer.Sound("rickroll/rickroll.mp3")

#endregion

#region Visual Variables
wheel_color_sets = [
    ["#fbc4ab", "#cdb4db", "#a2d2ff"],
    ["#0f4c81", "#00bcd4", "#cfd8dc"],
    ["#8f9779", "#c9b458", "#6b4226"],
    ["#ff6b6b", "#ffa600", "#4d96ff"],
    ["#00ffc3", "#ff00d4", "#3a0ca3"],
    ["#ff7518", "#2e2b2b", "#7f00ff"],
    ["#ff9ecd", "#ffe156", "#6b5b95"],
    ["#00916e", "#ffcf56", "#ef6f6c"],
    ["#90f1ef", "#ffd6e0", "#ffef9f"],
    ["#003566", "#ffc300", "#ff6b35"],
    ["#b8bedd", "#f6ae2d", "#d7263d"],
    ["#e0b1cb", "#9f86c0", "#5e548e"],
    ["#0d1b2a", "#1b263b", "#415a77"],
    ["#b4e7ce", "#ffcb77", "#fe6d73"],
    ["#fae1dd", "#fcd5ce", "#f8edeb"],
    ["#283618", "#606c38", "#dda15e"],
    ["#a7c957", "#6a994e", "#386641"],
    ["#f3722c", "#f9844a", "#f9c74f"],
    ["#3a86ff", "#8338ec", "#ff006e"],
    ["#9e2a2b", "#540b0e", "#e09f3e"],
    ["#f7aef8", "#b388eb", "#8093f1"],
    ["#2ec4b6", "#e71d36", "#ff9f1c"],]
wheel_colors = ["#db7dc1", "#dbd77d", "#7d85db"]
wheel_radius = 425
wheel_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2 - 30)

button_rect = pygame.Rect(0, 0, 100, 60)
button_rect.center = (screen.get_width() / 2, (screen.get_height() / 2) + 450)

counter_rect = pygame.Rect(0, 0, 100, 60)
counter_rect.midleft = (25, 25)

accept_rect = pygame.Rect(0, 0, screen.get_width() - 100, screen.get_height() / 3)
accept_rect.center = (screen.get_width() / 2, screen.get_height() / 2)

cigar_rect = pygame.Rect(0, 0, 100, 60)
cigar_rect.midright = (screen.get_width() - 25, 75)

showDuration = False
timer_rect = pygame.Rect(0, 0, 100, 0)
timer_rect.midleft = (25, 75)
#endregion

def changeWheel(wheel):
    global wheel_slices, wheel_options, wheel_divisions, jingle, lastWheel, seenSlices
    
    wheelLabels[lastWheel] = wheel_options
    lastWheel = currentWheel
        
    wheel_options = random.sample(wheelLabels[wheel], k=len(wheelLabels[wheel]))
    wheel_slices = len(wheel_options)
    wheel_divisions = 0
    
    pygame.display.set_caption(currentWheel)
    icon_image = pygame.image.load(f"imgs/{currentWheel}.png")
    pygame.display.set_icon(icon_image)
    jingle = pygame.mixer.Sound(f"jingles/{currentWheel}.mp3")
    
    for i in range(wheel_slices):
        wheel_divisions += wheel_options[i]["sizeMult"]
                
changeWheel(currentWheel)

#region Drawing
class Confetti:
    def __init__(self):
        self.x = wheel_pos.x
        self.y = wheel_pos.y
        self.size = random.randint(5, 9)
        self.color = random.randint(0, 2)
        
        self.angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.vel_x = speed * math.cos(self.angle)
        self.vel_y = speed * math.sin(self.angle)

        self.rotation_speed = random.uniform(-5, 5)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.angle += self.rotation_speed
        
        if self.x < 0 or self.x > 1000 or self.y < 0 or self.y > 1000:
            self.__init__()

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(surface, wheel_colors[self.color], rect)

confetti_particles = [Confetti() for _ in range(200)]

precomputed_wheel = []

def prepare_wheel_graphics(wheel_options):
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
            response = requests.post(
                "https://hack-box.vercel.app/wheelPOSTOFFICE",
                json={"wn": currentWheel, "wo": wheel_options, "last": lastSpinResult, "seenSlices": seenSlices},
                headers={'Content-Type': 'application/json'}
            )
            
            print("Status Code:", response.status_code)
            print("Headers:", response.headers)
            print("Response Text:", response.text)

            try:
                print("JSON Response:", response.json())
            except ValueError:
                print("No JSON content in response.")
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
    if (len(toDisp) > 40):
        font = pygame.font.Font(None, 35)
        
    pygame.draw.rect(surface, "#9EC2C8", accept_rect, border_radius=12)
    text_surf = font.render(toDisp, True, "#000000")
    text_rect = text_surf.get_rect(center=accept_rect.center)
    surface.blit(text_surf, text_rect)
    font = pygame.font.Font(None, 42)
    
def draw_mlp(surface):    
    font = pygame.font.Font(None, 200)
    toDisp = "MLP TIME!"
        
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
    
def draw_cigar_count(surface):
    font = pygame.font.Font(None, 42)
    pygame.draw.rect(surface, "#b2bfb5", cigar_rect, border_radius=12)
    text_surf = font.render(f"{cigars} cigars", True, "#000000")
    text_rect = text_surf.get_rect(midright=cigar_rect.midright)
    surface.blit(text_surf, text_rect)
#endregion
        
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

def check_neg_tick(prev_angle, new_angle):
    for boundary in slice_boundaries:
        if prev_angle < boundary <= new_angle:
            return True
        if new_angle < prev_angle and (boundary >= prev_angle or boundary < new_angle):
            return True
    return False
        
def get_slice_index(pointer_angle):
    for i, boundary in enumerate(slice_boundaries):
        if pointer_angle < boundary:
            return i
    return len(slice_boundaries) - 1

def addSlice(slice, sizeMult=1, winMult=1, removeFromWheel=1):
    global wheel_options, wheel_divisions, wheel_slices
    slice["sizeMult"] = sizeMult
    slice["winMult"] = winMult
    slice["removeFromWheel"] = removeFromWheel
    wheel_options.insert(random.randint(0, len(wheel_options) - 1), slice)
    wheel_divisions += sizeMult
    wheel_slices += 1
    
def addPremadeSlice(slice):
    global wheel_options, wheel_divisions, wheel_slices
    wheel_options.insert(random.randint(0, len(wheel_options) - 1), slice)
    wheel_divisions += slice["sizeMult"]
    wheel_slices += 1
        
while running:
    # region Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if needAccept and accept_rect.collidepoint(event.pos):
                winning_op = wheel_options[winning_slice]
                if (winning_op["removeFromWheel"] == 1):
                    wheel_slices -= 1
                    wheel_divisions -= winning_op["sizeMult"]
                    wheel_options.pop(winning_slice)
                    
                else:
                    if (winning_op["removeFromWheel"] > 1):
                        wheel_options[winning_slice]["removeFromWheel"] -= 1
                        if (winning_op["sizeMult"] > 1): wheel_options[winning_slice]["sizeMult"] -= 1
                        if (winning_op["winMult"] > 1): wheel_options[winning_slice]["winMult"] -= 1

                    unmodifiedLastSpinResult = True
                
                if (currentWheel in wheelQueues.keys()):
                    print("ADDING A SLICE")
                    if (len(wheelQueues[currentWheel]) > 0):
                        addPremadeSlice(nextFromQueue(currentWheel))
                    
                    if (zeepleSlice and random.randint(1, 10) == 2):
                        addPremadeSlice({
                            "label": "Zeeple Dome!",
                            "full": "WE'RE PLAYING ZEEPLE DOME!",
                            "sizeMult": 1,
                            "winMult": 1,
                            "removeFromWheel": 1,
                            "goToWheel": None,
                            "specialEffect": None,
                            "specialColor": "#EF3FC9",
                            "id": "THZEEP"                            
                        })
                
                if (beginnerSpins == 4 and currentWheel == "Beginner Wheel"):
                    addSlice({
                        "label": "Wheel Wheel",
                        "full": "GO TO THE WHEEL WHEEL!",
                        "goToWheel": "Wheel Wheel",
                        "specialEffect": "unlockCurrency",
                        "specialColor": "#EE8C4B",
                        "id": "WHWH"
                    }, 4, 2, 0)
                    
                if (total_spins == 20):
                    showDuration = True
                    
                if (winning_op["goToWheel"]):
                    if (winning_op["specialEffect"] == "setCallback"):
                        callbackWheel = currentWheel
                    currentWheel = winning_op["goToWheel"]
                    changeWheel(winning_op["goToWheel"])
                    
                if (winning_op["specialEffect"]):
                    eff = winning_op["specialEffect"]
                    
                    if eff == "changeTick":
                        wheelTickSounds = ["dnk", "doorclose", "gun", "many", "metl", "onDoop", "offDoop", "oof", "oOGo", "Ooo", "ptDrum", "thump", "tick", "truck", "woodDonk"]
                        wheel_tick = pygame.mixer.Sound(f"spinSounds/{random.choice(wheelTickSounds)}.mp3")
                        
                    elif eff == "performCallback":
                        if not callbackWheel: callbackWheel = "Beginner Wheel"
                        currentWheel = callbackWheel
                        callbackWheel = None
                        # print("YOU HAVEN'T NULLED OUT CALLBACK YOU BITCH!!!!")
                        changeWheel(currentWheel)
                        
                    elif eff == "thaliaSpecialSlice":
                        if not callbackWheel: callbackWheel = "Beginner Wheel"
                        currentWheel = callbackWheel
                        callbackWheel = None
                        # print("YOU HAVEN'T NULLED OUT CALLBACK YOU BITCH!!!!")
                        changeWheel(currentWheel)
                        zeepleSlice = True
                    
                    elif eff == "pastSlice":
                        idx = random.randint(0, len(allPastSlices.keys())-1)
                        addSlice(allPastSlices[list(allPastSlices.keys())[idx]])
                        
                    elif eff == "wheelColors":
                        wheel_colors = wheel_color_sets[random.randint(0, len(wheel_color_sets) - 1)]
                        
                    elif eff == "velocity":
                        min_spin_time += 2
                        
                    elif eff == "addJack":
                        addSlice(allSlices[random.choice(jbLabels)])
                        
                    elif eff == "toggleConf":
                        confetti = not confetti
                        
                if (currentWheel == "Past Slice Wheel" or (currentWheel == "Decision Paralysis Wheel" and lastSpinResult[0:1] == "JB")):
                    if not callbackWheel: callbackWheel = "Beginner Wheel"
                    currentWheel = callbackWheel
                    callbackWheel = None
                    # print("YOU HAVEN'T NULLED OUT CALLBACK YOU BITCH!!!!")
                    changeWheel(currentWheel)
                
                if (cigars >= 23 and currentWheel == "Wheel Wheel" and not endingAdded):
                    endingAdded = True
                    addPremadeSlice({
                        "label": "End Wheel Night Wheel",
                        "full": None,
                        "sizeMult": 1,
                        "winMult": 1,
                        "removeFromWheel": 1,
                        "goToWheel": "End Wheel Night Wheel",
                        "specialEffect": None,
                        "specialColor": "#942B08",
                        "id": "WHEWN"                            
                    })
                    
                # else:
                    # MilkTime-esque
                needAccept = False
                current_datetime = datetime.now()
                if (0 == current_datetime.hour and not mlpDone):
                    mlpDraw = True
                    mlpDone = True
            elif mlpDraw and accept_rect.collidepoint(event.pos):
                mlpDraw = False
            elif not needAccept and not spinning and button_rect.collidepoint(event.pos):                
                if (currentWheel == "Wheel Wheel"):
                    wheelWheelSpins += 1
                elif (currentWheel == "Beginner Wheel"):
                    beginnerSpins += 1
                elif (currentWheel == "Cigar Wheel"):
                    cigars += 1

                spinning = True
                total_spins += 1
                
                spin_duration = random.uniform(min_spin_time, min_spin_time + 2)
                spin_time = 0
                slice_boundaries = compute_boundaries()
                
                weights = [opt["winMult"] for opt in wheel_options]
                winning_slice = random.choices(range(len(wheel_options)), weights=weights, k=1)[0]
                lastSpinResult = wheel_options[winning_slice]["label"]
                seenSlices.update({wheel_options[winning_slice]["id"]: allSlices.get(wheel_options[winning_slice]["id"], {})})

                
                if wheel_options[winning_slice]["specialEffect"] == "confetti":
                    confetti = True
                elif wheel_options[winning_slice]["specialEffect"] == "loadload":
                    loadBar = True
                elif wheel_options[winning_slice]["specialEffect"] == "rickroll":
                    rickroll = True
                
                slice_start_angle = sum(opt["sizeMult"] * slice_size for opt in wheel_options[:winning_slice])
                slice_span = wheel_options[winning_slice]["sizeMult"] * slice_size
                target_angle = (slice_start_angle + slice_span * random.uniform(0.1, 0.9)) % 360
                
                delta_to_align = (270 - target_angle) % 360
                final_angle = full_rots * 360 + delta_to_align - angle
                start_angle = angle
        #endregion
    
    if spinning:
        spin_time += dt

        t = min(spin_time / spin_duration, 1.0)  # normalize 0 → 1
        progress = spinDirection*ease_out_cubic(t)

        angle = (start_angle + progress*final_angle) % 360
        
        prev_angle = pointer_angle
        pointer_angle = (-angle - 90) % 360
        
        if spinDirection == 1:
            if check_tick(prev_angle, pointer_angle):
                current_tick = get_slice_index(pointer_angle)
                if (wheel_options[current_tick]["label"] == "Play a Fart Sound"):
                    fart.play()
                elif (currentWheel == "America Wheel"):
                    america_tick.play()  
                else:
                    wheel_tick.play()
                color = wheel_options[current_tick]["specialColor"] if wheel_options[current_tick].get("specialColor") else wheel_colors[current_tick % len(wheel_colors)]
                with open("lightColor.txt", "w") as f:
                    f.write(color)
                triRot = 30
        else: #Doesn't work right now and I'm not going to fix it.
            if check_neg_tick(prev_angle, pointer_angle):
                current_tick = get_slice_index(pointer_angle)
                if (wheel_options[current_tick]["label"] == "Play a Fart Sound"):
                    fart.play()
                elif (currentWheel == "America Wheel"):
                    america_tick.play()  
                else:
                    wheel_tick.play()
                color = wheel_options[current_tick]["specialColor"] if wheel_options[current_tick].get("specialColor") else wheel_colors[current_tick % len(wheel_colors)]
                with open("lightColor.txt", "w") as f:
                    f.write(color)
                triRot = 30
        
        if t >= 1:
            spinning = False
            needAccept = True
            jingle.play()
        
    screen.fill("#b2bfb5")

    draw_wheel(screen, angle)
        
    pointer_surface = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.polygon(pointer_surface, (255,255,255), [(10, 0), (50, 0), (30, 40)])
    pointer_vertices = pygame.transform.rotate(pointer_surface, triRot)
    if (triRot > 0): triRot -= 5
    pointer_rec = pointer_vertices.get_rect(center=(wheel_pos.x, wheel_pos.y - 425))
    screen.blit(pointer_vertices, pointer_rec)
    
    if not spinning and not needAccept:
        draw_spin_button(screen)
    if needAccept and not loadBar and not rickroll:
        if confetti:
            for particle in confetti_particles:
                particle.update()
                particle.draw(screen)
        draw_accept(screen)
    if mlpDraw:
        draw_mlp(screen)
    if loadBar and needAccept:
        font = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, "#000000", (25, 1000 // 2 - 20, 950, 40), 2)
        pygame.draw.rect(screen, "#FFFFFF", (25, 1000 // 2 - 20, loading_width, 40))
        text_surf = font.render(f"Loading... {int((loading_width / 950) * 100)}%", True, "#000000")
        screen.blit(text_surf, (1000 // 2 - 100, 1000 // 2 + 50))
        loading_width += 0.1
        if loading_width > 970:
            loadBar = False
    if total_spins >= 3:
        draw_counter(screen)
    if showDuration:
        draw_timer(screen)
    if cigars >= 2:
        draw_cigar_count(screen)
    if needAccept and rickroll:
        if not songPlaying:
            rrSong.play()
            songPlaying = True
            frame_index = 1
            elapsed_time = 0
        elapsed_time += dt
        while elapsed_time >= FRAME_DURATION and frame_index <= 12785:
            image = load_frame(frame_index)
            if image:
                screen.blit(image, (0, 0))
                pygame.display.flip()

            elapsed_time -= FRAME_DURATION
            frame_index += 1
        if (frame_index >= 12785):
            rickroll = False
    
    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()