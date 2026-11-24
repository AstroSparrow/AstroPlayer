import os
import sys
L = []
BASE = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
AudioEffectsConfig = open(f"{BASE}/AudioEffects_Config.txt")
Config = AudioEffectsConfig.readlines()

print(Config[0])

for i in Config[1]:
    if i.isnumeric():
        L.append(i)
        
print(L)
SlowedValue = f"{L[0]}.{L[1]}"
print(SlowedValue)