import os
import sys
L = []
BASE = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
AudioEffectsConfig = open("T:/GitHub Repositories/AstroPlayer/AudioEffects_Config.txt")
Config = AudioEffectsConfig.read()
Config_Actual = Config.split()

print(Config_Actual)

for i in Config_Actual:
    try:
        float(i)
        L.append(float(i))
    except:
        pass
        
print(L)
'''
for i in Config[1]:
    if i.isnumeric():
        L.append(i)
        
print(L)
SlowedValue = f"{L[0]}.{L[1]}"
print(SlowedValue)
'''