import os
import random
import pygame
from PIL import Image
import keyboard
import time
import sys

L = []
L2 = []
L3 = []

BASE = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))

controlmusic = os.path.join(BASE, "Assets", "Music")
controlmelodysheep = os.path.join(BASE, "Assets", "Melodysheep")
controlimages = os.path.join(BASE, "Assets", "Images")
controlfont = os.path.join(BASE, "Assets", "Nasalization Rg.otf")
controlicon = os.path.join(BASE, "Assets", "Voyager Icon.png")

os.chdir(controlmelodysheep)
files = os.listdir(controlmelodysheep)

pygame.init()
pygame.font.init()
pygame.mixer.init()

icon = pygame.image.load(controlicon)
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font(controlfont, 20)
imagefiles = os.listdir(controlimages)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Astro Music Player")

L2 = files.copy()
random.shuffle(L2)
current_playlist = L2

def PlaylistCheck(current_playlist):
    newplaylist = []
    for name in current_playlist:
        if name[-3:].lower() in ("mp3", "wav", "ogg"):
            newplaylist.append(name)
    return newplaylist

current_playlist = PlaylistCheck(current_playlist)

current_track = 0
Volume = 1.0
seekoffset = 0
MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)
pause = 0
def play_track(index, current_playlist):
    global length
    global seekoffset
    pygame.mixer.music.load(current_playlist[index])
    length = pygame.mixer.Sound(current_playlist[index]).get_length()
    pygame.mixer.music.set_volume(Volume)
    pygame.mixer.music.play(fade_ms=1500)
    seekoffset = 0

def LoadImage():
    z = random.choice(imagefiles)
    Messier = Image.open(os.path.join(BASE, "Assets", "Images", z))
    Messier = Messier.resize((800, 600), Image.LANCZOS)
    Mode2 = Messier.mode
    Size2 = Messier.size
    Data2 = Messier.tobytes()
    Background = pygame.image.fromstring(Data2, Size2, Mode2)
    return Background

Background = LoadImage()
overlay = pygame.Surface((800,600), pygame.SRCALPHA)
overlay.fill((0,0,0,120))
running = True
play_track(current_track, current_playlist)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == MUSIC_END:
            current_track += 1
            if current_track >= len(current_playlist):
                random.shuffle(current_playlist)
                current_track = 0
                current_playlist = PlaylistCheck(current_playlist)
            play_track(current_track, current_playlist)
            Background = LoadImage()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if (20 <= mx <= 20 + 480 and 500 <= my <= 500 + 24):
                fraction = (mx - 20) / 480
                new_time = fraction * length
                seekoffset = new_time
                pygame.mixer.music.play(start=new_time)
                pygame.mixer.music.set_volume(Volume)

        elif (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_RIGHT:
                    current_track = current_track + 1
                    if current_track >= len(current_playlist):
                            random.shuffle(current_playlist)
                            current_track = 0
                            current_playlist = PlaylistCheck(current_playlist)
                    play_track(current_track, current_playlist)
                    Background = LoadImage()

                elif event.key == pygame.K_LEFT:
                    current_track = current_track - 1
                    if current_track < 0:
                            random.shuffle(current_playlist)
                            current_track = 0
                            current_playlist = PlaylistCheck(current_playlist)
                    play_track(current_track, current_playlist)
                    Background = LoadImage()

                elif event.key == pygame.K_ESCAPE:
                     running = False

                elif (event.key == pygame.K_SPACE and pause == 0):
                    pygame.mixer.music.pause()
                    pause = 1

                elif ((event.key == pygame.K_SPACE and pause == 1)):
                    pygame.mixer.music.unpause()
                    pause = 0

                elif (event.key == pygame.K_PERIOD):
                    os.chdir(controlmusic)
                    files2 = os.listdir(controlmusic)
                    L3 = files2.copy()
                    random.shuffle(L3)
                    current_track = 0
                    current_playlist = L3
                    current_playlist = PlaylistCheck(current_playlist)
                    play_track(current_track, current_playlist)
                    Background = LoadImage()
                
                elif (event.key == pygame.K_COMMA):
                    os.chdir(controlmelodysheep)
                    files = os.listdir(controlmelodysheep)
                    L2 = files.copy()
                    random.shuffle(L2)
                    current_track = 0
                    current_playlist = L2
                    current_playlist = PlaylistCheck(current_playlist)
                    play_track(current_track, current_playlist)
                    Background = LoadImage()

    if (keyboard.is_pressed('plus')):
        time.sleep(0.1)
        Volume = min(Volume + 0.1, 1.0)
        pygame.mixer.music.set_volume(Volume)

    elif (keyboard.is_pressed('-')):
        time.sleep(0.1)
        Volume = max(Volume - 0.1, 0.0)
        pygame.mixer.music.set_volume(Volume)
                                          
    screen.blit(Background, (0, 0))
    screen.blit(overlay,(0,0))
    name = os.path.splitext(current_playlist[current_track])[0]
    name = name.replace("_", " ")
    songnametext = font.render(f"Now Playing: {name}", True, (255, 255, 255))
    volumetext = font.render(f"Volume: {int(Volume * 100)}%", True, (255, 255, 255))
    screen.blit(songnametext, (40, 300))
    screen.blit(volumetext, (600, 500))
    song_completion = seekoffset + pygame.mixer.music.get_pos()/1000
    progress = song_completion/length
    progress = min(song_completion / length, 1)
    elapsed_min = int(song_completion // 60)
    elapsed_sec = int(song_completion % 60)

    length_min = int(length // 60)
    length_sec = int(length % 60)

    time_text = font.render(
f"{elapsed_min}:{elapsed_sec:02} / {length_min}:{length_sec:02}",
True,
(255, 255, 255)
)

    screen.blit(time_text, (20, 530))
    filled = progress * 500
    pygame.draw.rect(screen, (70,70,70), (20,500,500,24), border_radius=10)
    pygame.draw.rect(screen, (255,255,255), (20,500,filled,24), border_radius=10)

    clock.tick(20)
    pygame.display.flip()

pygame.quit()
sys.exit(0)