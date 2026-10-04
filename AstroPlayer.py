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

MessierNames = {'M1': 'Crab Nebula', 'M2': 'NGC 7089', 'M3': 'NGC 5272', 'M4': 'NGC 6121', 'M5': 'NGC 5904', 'M6': 'Butterfly Cluster', 'M7': "Ptolemy's Cluster", 'M8': 'Lagoon Nebula', 'M9': 'NGC 6333', 'M10': 'NGC 6254', 'M11': 'Wild Duck Cluster', 'M12': 'NGC 6218', 'M13': 'Hercules Globular Cluster', 'M14': 'NGC 6402', 'M15': 'NGC 7078', 'M16': 'Eagle Nebula Cluster', 'M17': 'Omega Nebula', 'M18': 'NGC 6613', 'M19': 'NGC 6273', 'M20': 'Trifid Nebula', 'M21': 'NGC 6531', 'M22': 'NGC 6656', 'M23': 'NGC 6494', 'M24': 'Milky Way Patch', 'M25': 'IC 4725', 'M26': 'NGC 6694', 'M27': 'Dumbbell Nebula', 'M28': 'NGC 6626', 'M29': 'NGC 6913', 'M30': 'NGC 7099', 'M31': 'Andromeda Galaxy', 'M32': 'Satellite of M31', 'M33': 'Triangulum Galaxy', 'M34': 'NGC 1039', 'M35': 'NGC 2168', 'M36': 'NGC 1960', 'M37': 'NGC 2099', 'M38': 'NGC 1912', 'M39': 'NGC 7092', 'M40': 'Winecke 4', 'M41': 'NGC 2287', 'M42': 'Orion Nebula', 'M43': "de Mairan's Nebula", 'M44': 'Beehive Cluster', 'M45': 'Pleiades', 'M46': 'NGC 2437', 'M47': 'NGC 2422', 'M48': 'NGC 2548', 'M49': 'NGC 4472', 'M50': 'NGC 2323', 'M51': 'Whirlpool Galaxy', 'M52': 'NGC 7654', 'M53': 'NGC 5024', 'M54': 'NGC 6715', 'M55': 'NGC 6809', 'M56': 'NGC 6779', 'M57': 'Ring Nebula', 'M58': 'NGC 4579', 'M59': 'NGC 4621', 'M60': 'NGC 4649', 'M61': 'NGC 4303', 'M62': 'NGC 6266', 'M63': 'Sunflower Galaxy', 'M64': 'Blackeye Galaxy', 'M65': 'NGC 3623', 'M66': 'NGC 3627', 'M67': 'NGC 2682', 'M68': 'NGC 4590', 'M69': 'NGC 6637', 'M70': 'NGC 6681', 'M71': 'NGC 6838', 'M72': 'NGC 6981', 'M73': 'Group of 4 stars', 'M74': 'NGC 628', 'M75': 'NGC 6864', 'M76': 'Little Dumbbell Nebula', 'M77': 'Cetus A', 'M78': 'NGC 2068', 'M79': 'NGC 1904', 'M80': 'NGC 6093', 'M81': "Bode's Galaxy", 'M82': 'Cigar Galaxy', 'M83': 'Southern Pinwheel Galaxy', 'M84': 'NGC 4374', 'M85': 'NGC 4382', 'M86': 'NGC 4406', 'M87': 'Virgo A', 'M88': 'NGC 4501', 'M89': 'NGC 4552', 'M90': 'NGC 4569', 'M91': 'NGC 4548', 'M92': 'NGC 6341', 'M93': 'NGC 2447', 'M94': 'NGC 4736', 'M95': 'NGC 3351', 'M96': 'NGC 3368', 'M97': 'Owl Nebula', 'M98': 'NGC 4192', 'M99': 'NGC 4254', 'M100': 'NGC 4321', 'M101': 'Pinwheel Galaxy', 'M102': 'Spindle Galaxy', 'M103': 'NGC 581', 'M104': 'Sombrero Galaxy', 'M105': 'NGC 3379', 'M106': 'NGC 4258', 'M107': 'NGC 6171', 'M108': 'NGC 3556', 'M109': 'NGC 3992', 'M110': 'Satellite of M31'}

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

controlicon = pygame.image.load(controlicon)
pygame.display.set_icon(controlicon)
controlclock = pygame.time.Clock()
controlfontactual = pygame.font.Font(controlfont, 20)
imagefiles = os.listdir(controlimages)
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("AstroPlayer")

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
    global z
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
    controlsongnametext = controlfontactual.render("Now Playing: ", True, (218, 177, 218))
    songnameactual = controlfontactual.render(song_name, True, (255, 255, 255))
    volumetext = controlfontactual.render(f"Volume: {int(Volume * 100)}%", True, (100, 190, 255))
    ImageName = z
    ImageName = ImageName.replace("_", " ")
    ImageName = ImageName.replace(".jpg", "")
    ImageName = ImageName.replace(".png", "")
    if ("Messier" in ImageName):
        MessierNameLength = len(ImageName)
        MessierNumber = ImageName[8:MessierNameLength + 1]
        if (f"M{MessierNumber}" in MessierNames):
            MessierNameActual = MessierNames[f"M{MessierNumber}"]
            ImageNameText = controlfontactual.render(f"{ImageName}: {MessierNameActual}",  True, (255, 255, 255))
        else:
            ImageNameText = controlfontactual.render(ImageName,  True, (255, 255, 255))
    else:
        ImageNameText = controlfontactual.render(ImageName,  True, (255, 255, 255))
    ImageNameText.set_alpha(200)
    currentplaylistname = os.path.basename(playlistpaths[currentplaylistindex])
    controlplaylisttext = controlfontactual.render("Current Playlist: ", True, (136, 231, 136))
    playlisttextactual = controlfontactual.render(currentplaylistname, True, (255, 255, 255))
    playlisttextunittotalwidth = controlplaylisttext.get_width() + playlisttextactual.get_width()
    starting_x_forplaylisttextunit = (screen.get_width() - playlisttextunittotalwidth) // 2
    ImageNameTextTotalWidth = ImageNameText.get_width()
    Starting_X_ForImageNameText = (screen.get_width() - ImageNameTextTotalWidth) // 2
    '''playlisttextrect = controlplaylisttext.get_rect()
    playlisttextrect.centerx = screen.get_width() // 2
    playlisttextrect.y = 20'''
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

    time_text = controlfontactual.render(
f"{elapsed_min}:{elapsed_sec:02} / {length_min}:{length_sec:02}",
True,
(255, 255, 255)
)

    filled = progress * 500

    if (playlist_view_bool == True):
        Playlist_View_Heading = controlfontactual.render(f"Playlist View for {currentplaylistname}", True, (136, 231, 136))
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
                song_text = controlfontactual.render(f"{i}. {song_name_queue} - Now Playing", True, (253, 208, 23))
            else:
                song_text = controlfontactual.render(f"{i}. {song_name_queue}", True, (255, 255, 255))
            y = 80 + (index * 40) - (playlist_scroll * 40)
            if (70 <= y <= 600):
                screen.blit(song_text, (40, y))
            i += 1
            #if (i > 10):
                #break
        
    else:
        screen.blit(controlsongnametext, (40, 300))
        screen.blit(ImageNameText, (Starting_X_ForImageNameText, 560))
        screen.blit(songnameactual, (184, 300))
        screen.blit(volumetext, (600, 510))
        #screen.blit(controlplaylisttext, playlisttextrect)
        screen.blit(controlplaylisttext, (starting_x_forplaylisttextunit, 20))
        screen.blit(playlisttextactual, (starting_x_forplaylisttextunit + controlplaylisttext.get_width(), 20))
        #screen.blit(playlisttextactual, (414, 20))
        screen.blit(time_text, (20, 540))
        pygame.draw.rect(screen, (70,70,70), (20,510,510,24), border_radius=10)
        pygame.draw.rect(screen, (255,255,255), (20,510,filled,24), border_radius=10)

    controlclock.tick(20)
    pygame.display.flip()

pygame.quit()
sys.exit(0)