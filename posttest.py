import requests
import json

with open('wheels/beginnerWheel.json') as f:
    beginnerWheelJS = json.load(f)
    beginnerWheel = []
    for i in range(1, len(beginnerWheelJS) + 1):
        beginnerWheel.append(beginnerWheelJS[str(i)])
beginnerV2 = False

with open('wheels/wheelWheel.json') as f:
    wheelWheelJS = json.load(f)
    wheelWheel = []
    for i in range(1, len(wheelWheelJS) + 1):
        wheelWheel.append(wheelWheelJS[str(i)])
wheelWheelSpins = 0
wheelWheelV2 = False

with open('wheels/funWheel.json') as f:
    funWheelJS = json.load(f)
    funWheel = []
    for i in range(1, len(funWheelJS) + 1):
        funWheel.append(funWheelJS[str(i)])
        
response = requests.post("https://hack-box.vercel.app/wheelPOSTOFFICE", json=beginnerWheel, headers={'Content-Type': 'application/json'})
print(response)