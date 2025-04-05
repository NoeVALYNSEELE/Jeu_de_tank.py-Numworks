import ion
import kandinsky
from time import *

# Définition de la taille de l'écran
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
TANK_SIZE = 20
SPEED = 5

# Position initiale des tanks
tank1_x, tank1_y = 50, 100
tank2_x, tank2_y = 200, 100
orientationt1 = 1
orientationt2 = 1
vie_tank1 = 5
vie_tank2 = 5

# Couleurs des tanks
COLOR_TANK1 = (255, 0, 0)  # Rouge
COLOR_TANK2 = (0, 0, 255)  # Bleu
COLOR_WALL = (0, 0, 0)  # Noir pour les murs

#Variable de shoot
last_shot1 = 0  # Temps du dernier tir pour le tank 
last_shot2 = 0
COOLDOWN = 0.3  # Délai en secondes (ici 300 ms) entre deux tirs
current_time = monotonic()


# Définir les murs comme une liste de rectangles
walls = [
    (50, 50, 100, 10),  # mur 1: x, y, largeur, hauteur
    (200, 150, 100, 10),  # mur 2
    (150, 100, 10, 50),  # mur 3
]

#Liste pour stocker la position de tous les boulets en cours
bullets1 = []
bullets2 = []

# Définir la fréquence du rafraîchissement
FPS = 20  # Fréquence en images par seconde
frame_time = 1 / FPS  # Durée par frame en secondes

def draw():
    # Effacer l'écran avant de redessiner les tanks et les murs
    kandinsky.fill_rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, (255, 255, 255))  # Fond blanc

    # Dessiner les murs
    for (x, y, width, height) in walls:
        kandinsky.fill_rect(x, y, width, height, COLOR_WALL)
    
    #Dessiner les boulets
    for bullet1 in bullets1:
      kandinsky.fill_rect(bullet1["x"], bullet1["y"], 5, 5, (0, 0, 0))
    for bullet2 in bullets2:
      kandinsky.fill_rect(bullet2["x"], bullet2["y"], 5, 5, (0, 0, 0))
    
    # Dessiner les tanks
    kandinsky.fill_rect(tank1_x, tank1_y, TANK_SIZE, TANK_SIZE, COLOR_TANK1)  # Tank 1
    if orientationt1 == 1:
      kandinsky.fill_rect(tank1_x, tank1_y + 6, 27, 7, COLOR_TANK1)
    elif orientationt1 == 2:
      kandinsky.fill_rect(tank1_x + 7, tank1_y, 7, 27, COLOR_TANK1)
    elif orientationt1 == 3:
      kandinsky.fill_rect(tank1_x - 7, tank1_y + 7, 27, 7, COLOR_TANK1)
    elif orientationt1 == 0:
      kandinsky.fill_rect(tank1_x + 7, tank1_y - 7, 7, 27, COLOR_TANK1)
    
    kandinsky.fill_rect(tank2_x, tank2_y, TANK_SIZE, TANK_SIZE, COLOR_TANK2)  # Tank 2
    if orientationt2 == 1:
      kandinsky.fill_rect(tank2_x, tank2_y + 6, 27, 7, COLOR_TANK2)
    elif orientationt2 == 2:
      kandinsky.fill_rect(tank2_x + 7, tank2_y, 7, 27, COLOR_TANK2)
    elif orientationt2 == 3:
      kandinsky.fill_rect(tank2_x - 7, tank2_y + 7, 27, 7, COLOR_TANK2)
    elif orientationt2 == 0:
      kandinsky.fill_rect(tank2_x + 7, tank2_y - 7, 7, 27, COLOR_TANK2)

def move_tank1():
    global tank1_x, tank1_y, orientationt1, last_shot1  # Déclare les variables comme globales
    new_x, new_y = tank1_x, tank1_y 

    if ion.keydown(ion.KEY_UP):
        new_y -= SPEED
        orientationt1 = 0
    elif ion.keydown(ion.KEY_DOWN):
        new_y += SPEED
        orientationt1 = 2
    elif ion.keydown(ion.KEY_LEFT): #Mettre if pour diagonales MAIS BUGS
        new_x -= SPEED
        orientationt1 = 3
    elif ion.keydown(ion.KEY_RIGHT):
        new_x += SPEED
        orientationt1 = 1

    # Vérifier la collision avec les murs
    if not check_collision(new_x, new_y):
        tank1_x, tank1_y = new_x, new_y
    
    #Shoot
    current_time = monotonic()
    if ion.keydown(ion.KEY_OK) and (current_time - last_shot1) >= COOLDOWN:
      bullet1 = {"x":int(tank1_x + TANK_SIZE/2),
                "y":int(tank1_y + TANK_SIZE/2),
                "dx":0,
                "dy":-10}
      if orientationt1 == 1:
        bullet1["dx"]=10
        bullet1["dy"]=0
      elif orientationt1 == 2:
        bullet1["dx"]=0
        bullet1["dy"]=10
      elif orientationt1 == 3:
        bullet1["dx"]=-10
        bullet1["dy"]=0
      elif orientationt2 == 0:
        bullet1["dx"]=0
        bullet1["dy"]=-10
      bullets1.append(bullet1)
      last_shot1 = current_time  # On met à jour le temps du dernier tir
      
def move_tank2():
    global tank2_x, tank2_y, orientationt2, last_shot2  # Déclare les variables comme globales
    new_x, new_y = tank2_x, tank2_y

    if ion.keydown(ion.KEY_PLUS):
        new_y -= SPEED
        orientationt2 = 0
    elif ion.keydown(ion.KEY_ANS):
        new_y += SPEED
        orientationt2 = 2
    elif ion.keydown(ion.KEY_EE): #Seulement if, pour les diagonales MAIS BUGS
        new_x -= SPEED
        orientationt2 = 3
    elif ion.keydown(ion.KEY_EXE):
        new_x += SPEED
        orientationt2 = 1

    # Vérifier la collision avec les murs
    if not check_collision(new_x, new_y):
        tank2_x, tank2_y = new_x, new_y

    #Shoot
    current_time = monotonic()
    if ion.keydown(ion.KEY_ZERO) and (current_time - last_shot2) >= COOLDOWN:
      bullet2 = {"x":int(tank2_x + TANK_SIZE/2),
                "y":int(tank2_y + TANK_SIZE/2),
                "dx":0,
                "dy":-10}
      if orientationt2 == 1:
        bullet2["dx"]=10
        bullet2["dy"]=0
      elif orientationt2 == 2:
        bullet2["dx"]=0
        bullet2["dy"]=10
      elif orientationt2 == 3:
        bullet2["dx"]=-10
        bullet2["dy"]=0
      elif orientationt2 == 0:
        bullet2["dx"]=0
        bullet2["dy"]=-10
      bullets2.append(bullet2)
      last_shot2 = current_time  # On met à jour le temps du dernier tir
    
    
def check_collision(new_x, new_y):
    for (wx, wy, ww, wh) in walls:
        if (new_x < wx + ww and new_x + TANK_SIZE > wx and new_y < wy + wh and new_y + TANK_SIZE > wy):
            return True  # Collision avec un mur
    if new_x < 0 or new_x > 300 or new_y < 0 or new_y > 207:
      return True
    return False  # Pas de collision

def move_bullets(): #Déplace et vérifie les collisions des boulets
  global tank1_x, tank1_y, tank2_x, tank2_y, vie_tank1, vie_tank2
  for bullet1 in bullets1:
    bullet1["x"] += bullet1["dx"]
    bullet1["y"] += bullet1["dy"]
    #Vérifie les collisions avec les murs
    for (wx, wy, ww, wh) in walls: 
      if (bullet1["x"] >= wx and bullet1["x"] <= wx + ww and bullet1["y"] >= wy and bullet1["y"] <= wy + wh):
        bullets1.remove(bullet1)
    #Vérifie les collisions avec les tanks
    if(bullet1["x"] >= tank2_x and bullet1["x"] <= tank2_x + TANK_SIZE and bullet1["y"] >= tank2_y and bullet1["y"] <= tank2_y + TANK_SIZE):
      vie_tank2 -= 1
      tank1_x, tank1_y = 50, 100
      tank2_x, tank2_y = 200, 100
      bullets1.remove(bullet1)
  
  for bullet2 in bullets2:
    bullet2["x"] += bullet2["dx"]
    bullet2["y"] += bullet2["dy"]
    for (wx, wy, ww, wh) in walls:
      if (bullet2["x"] >= wx and bullet2["x"] <= wx + ww and bullet2["y"] >= wy and bullet2["y"] <= wy + wh):
        bullets2.remove(bullet2)
    #Vérifie les collisions avec les tanks
    if(bullet2["x"] >= tank1_x and bullet2["x"] <= tank1_x + TANK_SIZE and bullet2["y"] >= tank1_y and bullet2["y"] <= tank1_y + TANK_SIZE):
      vie_tank1 -= 1
      tank1_x, tank1_y = 50, 100
      tank2_x, tank2_y = 200, 100
      bullets2.remove(bullet2)

def HUD():
  kandinsky.draw_string(str("Vie : "),0,0,(255, 0, 0),(255, 255, 255))
  kandinsky.draw_string(str(vie_tank1),57,0,(255, 0, 0),(255, 255, 255))
  kandinsky.draw_string(str("Vie : "),250,0,(0, 0, 255),(255, 255, 255))
  kandinsky.draw_string(str(vie_tank2),307,0,(0, 0, 255),(255, 255, 255))

def test_mort():
  global running
  if vie_tank1 <= 0:
    running = False
    kandinsky.fill_rect(0, 0, 500, 500, COLOR_TANK2)
    kandinsky.draw_string("Le tank bleu a gagné !!!",40,100,(0, 0, 0),COLOR_TANK2)
    kandinsky.draw_string("Relancez le programme",40,120,(0, 0, 0),COLOR_TANK2)
  if vie_tank2 <= 0:
    running = False
    kandinsky.fill_rect(0, 0, 500, 500, COLOR_TANK1)
    kandinsky.draw_string("Le tank rouge a gagné !!!",40,100,(0, 0, 0),COLOR_TANK1)
    kandinsky.draw_string("Relancez le programme",40,120,(0, 0, 0),COLOR_TANK1)

# Boucle principale
running = True
try:
    while running:
        start_time = monotonic()  # Capture du temps au début de la boucle
        move_tank1()
        move_tank2()
        move_bullets()
        draw()
        HUD()
        test_mort()
        # Limiter le temps de rafraîchissement pour atteindre un taux constant
        elapsed_time = monotonic() - start_time
        sleep_time = frame_time - elapsed_time
        if sleep_time > 0:
            sleep(sleep_time)  # Attente pour maintenir un taux de rafraîchissement constant
except KeyboardInterrupt:
    print("Jeu interrompu!!!")