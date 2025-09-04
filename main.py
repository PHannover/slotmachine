# source .venv/bin/activate

import pygame
import random
pygame.init()

######################################### classes ############################################

class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def draw(self, surf):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        surf.blit(self.image, (self.rect.x, self.rect.y))
        return action

class Slot():
    def __init__(self, breite, hoehe, bild_liste_start):
        self.scroll = 0
        self.bild_liste_start = bild_liste_start
        self.bilder_inactive, self.bilder_active = init_slot(self.bild_liste_start)
        self.breite = breite
        self.hoehe = hoehe
        self.surf = pygame.Surface((self.breite, self.hoehe))
        self.stop_toggle = False
        self.top_speed = 500 * random.uniform(0.8, 1.2)
        self.speed = 0
        self.lowest_speed = 20
        self.stop_acc = 2
        self.start_acc = 10
        self.color = (255, 255, 255)

        # Slots bewegen
    def update(self, delta_time):
        self.scroll += self.speed * delta_time
        if self.scroll >= (self.hoehe/3):
            self.scroll -= (self.hoehe/3)
            self.bilder_active.pop(0)
            self.bilder_inactive, self.bilder_active = bild_hinzuf(self.bilder_inactive, self.bilder_active)
            occured = [zeile[1] for zeile in self.bilder_inactive]  # nur die zweite Spalte
            if sum(occured) == 0:
                self.bilder_inactive = [zeile[:] for zeile in self.bild_liste_start]

        self.surf.fill(self.color)

        for i, bild in enumerate(self.bilder_active):
            y_pos = (3-i-1) * (self.hoehe/3) + self.scroll
            self.surf.blit(bild[0], (5 // 2, y_pos))
            
        if self.stop_toggle and self.speed > self.lowest_speed:
            self.speed -= self.stop_acc
        elif self.stop_toggle and  self.scroll < self.stop_acc:
            self.scroll = 0
            self.speed = 0

        if not self.stop_toggle and self.speed < self.top_speed:
            self.speed += self.start_acc

    def draw(self, target_surface, x_pos, y_pos):
        target_surface.blit(self.surf, (x_pos, y_pos))

    def stop(self):
        if self.speed >= self.top_speed: 
            self.stop_toggle = True

    def start(self):
        if self.speed == 0: 
            self.stop_toggle = False

    def get_stop_toggle(self):
        return self.stop_toggle
        



######################################### functions ############################################

def load_img(path, width, hight):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (width, hight))

def bild_hinzuf(bild_liste, slot_bilder):
    # Alle Zeilen, deren zweites Element nicht 1 ist
    gefiltert_indices = [i for i, zeile in enumerate(bild_liste) if zeile[1] > 0]
    # Zufälligen Index auswählen
    zufall_index = random.choice(gefiltert_indices)
    # Zeile in der Original-Liste anpassen
    bild_liste[zufall_index][1] -= 1
    slot_bilder.append(bild_liste[zufall_index])
    return bild_liste, slot_bilder

# Slot-Listen vorbereiten
def init_slot(bild_liste_start):
    bilder = []
    bild_liste = [zeile[:] for zeile in bild_liste_start]
    for _ in range(4):  # immer 4 Bilder pro Slot aktiv
        bild_liste, bilder = bild_hinzuf(bild_liste, bilder)
    return bild_liste, bilder

######################################### main ############################################

def main():

    rot = (255,20,20)
    schwarz = (0, 0, 0)
    grau = (130,130,130)
    weiß = (255,255,255)

    # Maße
    bild_breite = 50
    bild_hoehe = 50
    bild_abstand = 10
    slot_breite = bild_hoehe + bild_abstand
    slot_hoehe = 3 * (bild_hoehe + bild_abstand)

    screen = pygame.display.set_mode((600, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Slot Machine")

    kirsche_img = load_img('bilder/Kirsche.png', bild_breite, bild_hoehe)
    sieben_img = load_img('bilder/7.png', bild_breite, bild_hoehe)
    apfel_img = load_img('bilder/apfel.png', bild_breite, bild_hoehe)
    armor_img = load_img('bilder/armor.png', bild_breite, bild_hoehe)
    book_img = load_img('bilder/book.png', bild_breite, bild_hoehe)
    erdblock_img = load_img('bilder/erdblock.png', bild_breite, bild_hoehe)
    glocke_img = load_img('bilder/glocke.png', bild_breite, bild_hoehe)
    
    stop_button_img = load_img('bilder/Stop.PNG', 80, 40)
    start_button_img = load_img('bilder/start.png', 80, 40)

    stop_button = Button(200 ,450, stop_button_img)
    start_button = Button(300 ,450, start_button_img)

    
    bild_liste_start = [
        [kirsche_img, 1],
        [sieben_img, 1],
        [apfel_img, 1],
        [armor_img, 1],
        [book_img, 1],
        [erdblock_img, 1],
        [glocke_img, 1]
    ]

    
    slot1 = Slot(slot_breite, slot_hoehe, bild_liste_start)
    slot2 = Slot(slot_breite, slot_hoehe, bild_liste_start)
    slot3 = Slot(slot_breite, slot_hoehe, bild_liste_start)

    running = True
    clock = pygame.time.Clock()
    # delta_time = 0.1  
    automat_surf = pygame.Surface((300,450))

    while running:
        delta_time = clock.tick(60) / 1000.0

        #Automat erstellen
        automat_surf.fill(grau)
        pygame.draw.rect(automat_surf, schwarz, (0, 0, 300, 450), 3)
        pygame.draw.line(automat_surf, schwarz, (0, 87), (300, 87), 3)
        pygame.draw.line(automat_surf, schwarz, (0, 271), (300, 271), 3)

        # Slots bewegen
        slot1.update(delta_time)
        slot2.update(delta_time)
        slot3.update(delta_time)


        # Slots auf Automaten zeichnen
        slot1.draw(automat_surf, 30, 90)
        slot2.draw(automat_surf, 120, 90)
        slot3.draw(automat_surf, 210, 90)

        # Automaten zeichnen
        screen.blit(automat_surf, (150, 50))
    
        #stop slots
        if stop_button.draw(screen):
            if not slot1.get_stop_toggle(): 
                slot1.stop()
                print("stop slot 1")
            elif not slot2.get_stop_toggle(): slot2.stop()
            else: slot3.stop()

           # start slots        
        if start_button.draw(screen):
            slot1.start()
            slot2.start()
            slot3.start()

        if start_slots == 1 and speed1 < top_speed and stop_slot == 0:
            speed1 += start_acc
            speed2 += start_acc
            speed3 += start_acc     
        
        # Spiel schließen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Screen update
        pygame.display.flip()
        #   delta_time = max(0.001, min(0.1, delta_time))

    pygame.quit()

main()