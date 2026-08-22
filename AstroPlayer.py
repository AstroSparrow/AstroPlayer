import os
import random
import pygame
from PIL import Image
import keyboard
import time
import sys

#L = []
#L2 = []
#L3 = []
playlistpaths = []
currentplaylistindex = 0
attempts = 0

BASE = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))

playlist_root_complex = os.path.join(BASE, "Assets", "Playlists")
controlfont = os.path.join(BASE, "Assets", "Orbitron-Regular.ttf")
controlimages = os.path.join(BASE, "Assets", "Images")
controlicon = os.path.join(BASE, "Assets", "Voyager Icon.png")

pygame.init()
pygame.font.init()
pygame.mixer.init()

for folder in os.listdir(playlist_root_complex):
    path = os.path.join(playlist_root_complex, folder)
    if (os.path.isdir(path)):
        playlistpaths.append(path)

icon = pygame.image.load(controlicon)
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
font = pygame.font.Font(controlfont, 20)
imagefiles = os.listdir(controlimages)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Astro Music Player")

def Loadplaylist(index):
    playlist = []
    for file in os.listdir(playlistpaths[index]):
        path = os.path.join(playlistpaths[index], file)
        if os.path.isfile(path):
            playlist.append(path)
    random.shuffle(playlist)
    return PlaylistCheck(playlist)

def PlaylistCheck(current_playlist):
    newplaylist = []
    for name in current_playlist:
        if (name[-3:].lower() == "mp3" or name[-3:].lower() == "wav" or name[-3:].lower() == "ogg"):
            newplaylist.append(name)
    return newplaylist

while attempts < len(playlistpaths):
    current_playlist = Loadplaylist(currentplaylistindex)
    if current_playlist:
        break
    currentplaylistindex += 1
    currentplaylistindex %= len(playlistpaths)
    attempts += 1

if (attempts == len(playlistpaths)):
    pygame.quit()
    sys.exit(0)

current_track = 0
Volume = 1.0
seekoffset = 0
playlist_view_bool = False
playlist_scroll = 0
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

def NextPlaylist(step):
    global currentplaylistindex
    while True:
        currentplaylistindex = (currentplaylistindex + step) % len(playlistpaths)
        current_playlist = Loadplaylist(currentplaylistindex)
        if current_playlist:
            return current_playlist

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

            if (playlist_view_bool == True):
                if (40 <= mx <= 760):
                    clicked_index = int(
                        (my - 80 + playlist_scroll * 40) / 40
                    )

                    if 0 <= clicked_index < len(current_playlist):

                        current_track = clicked_index
                        play_track(current_track, current_playlist)

                        playlist_view_bool = False
                        Background = LoadImage()
            else:
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
                    current_track = 0
                    current_playlist = NextPlaylist(1)
                    play_track(current_track, current_playlist)
                    Background = LoadImage()
                
                elif (event.key == pygame.K_COMMA):
                    current_track = 0
                    current_playlist = NextPlaylist(-1)
                    play_track(current_track, current_playlist)
                    Background = LoadImage()
                    
                elif (event.key == pygame.K_l):
                    playlist_view_bool = not playlist_view_bool
                    playlist_scroll = 0

                '''   
                elif (event.key == pygame.K_DOWN and playlist_view_bool == True):
                    playlist_scroll = playlist_scroll + 1
                
                elif (event.key == pygame.K_UP and playlist_view_bool == True):
                    playlist_scroll = playlist_scroll - 1
                '''
    if (keyboard.is_pressed('plus')):
        time.sleep(0.1)
        Volume = min(Volume + 0.1, 1.0)
        pygame.mixer.music.set_volume(Volume)

    elif (keyboard.is_pressed('-')):
        time.sleep(0.1)
        Volume = max(Volume - 0.1, 0.0)
        pygame.mixer.music.set_volume(Volume)
        
    elif (keyboard.is_pressed('up') and playlist_view_bool == True):
        playlist_scroll = playlist_scroll - 1
        time.sleep(0.1)
        
    elif (keyboard.is_pressed('down') and playlist_view_bool == True):
        playlist_scroll = playlist_scroll + 1
        time.sleep(0.1)

    screen.blit(Background, (0, 0))
    screen.blit(overlay,(0,0))
    if (playlist_view_bool == True):
        max_scroll = max(0, len(current_playlist) - 10)
        playlist_scroll = max(0, min(playlist_scroll, max_scroll))
    song_name = os.path.splitext(os.path.basename(current_playlist[current_track]))[0]
    song_name = song_name.replace("_", " ") 
    songnametext = font.render(f"Now Playing: {song_name}", True, (255, 255, 255))
    volumetext = font.render(f"Volume: {int(Volume * 100)}%", True, (255, 255, 255))
    currentplaylistname = os.path.basename(playlistpaths[currentplaylistindex])
    playlisttext = font.render(f"Current Playlist: {currentplaylistname}", True, (255, 255, 255))
    playlisttextrect = playlisttext.get_rect()
    playlisttextrect.centerx = screen.get_width() // 2
    playlisttextrect.y = 20
    playlist_view_scroll_limit = -(len(current_playlist) // 10) - 1
    '''
    if (playlist_scroll > 0):
        playlist_scroll = 0
    if (playlist_scroll < playlist_view_scroll_limit):
        playlist_scroll = playlist_view_scroll_limit
    '''
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

    filled = progress * 500

    if (playlist_view_bool == True):
        Playlist_View_Heading = font.render(f"Playlist View for {currentplaylistname}", True, (255, 255, 255))
        Playlist_View_Heading_Rect = Playlist_View_Heading.get_rect()
        Playlist_View_Heading_Rect.centerx = screen.get_width() // 2
        Playlist_View_Heading_Rect.y = 20
        screen.blit(Playlist_View_Heading, Playlist_View_Heading_Rect)
        pygame.draw.line(screen, (255, 255, 255), (0, 70), (800, 70))
        
        song_queue = current_playlist
        song_queue_y = 80
        i = 1
        for index, song in enumerate(song_queue):
            song_name_queue = os.path.splitext(os.path.basename(song))[0]
            song_name_queue = song_name_queue.replace("_", " ")
            if song_name_queue == song_name:
                song_text = font.render(f"{i}. {song_name_queue} - Now Playing", True, (253, 208, 23))
            else:
                song_text = font.render(f"{i}. {song_name_queue}", True, (255, 255, 255))
            y = 80 + (index * 40) - (playlist_scroll * 40)
            if (70 <= y <= 600):
                screen.blit(song_text, (40, y))
            i += 1
            #if (i > 10):
                #break
        
    else:
        screen.blit(songnametext, (40, 300))
        screen.blit(volumetext, (600, 510))
        screen.blit(playlisttext, playlisttextrect)
        screen.blit(time_text, (20, 540))
        pygame.draw.rect(screen, (70,70,70), (20,510,510,24), border_radius=10)
        pygame.draw.rect(screen, (255,255,255), (20,510,filled,24), border_radius=10)

    clock.tick(20)
    pygame.display.flip()

pygame.quit()
sys.exit(0)