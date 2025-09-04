# source .venv/bin/activate

import pygame
import random
pygame.init()

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



def bild_hinzuf(bild_liste, slot_bilder):
    # Alle Zeilen, deren zweites Element nicht 1 ist
    gefiltert_indices = [i for i, zeile in enumerate(bild_liste) if zeile[1] > 0]
    # Zufälligen Index auswählen
    zufall_index = random.choice(gefiltert_indices)
    # Zeile in der Original-Liste anpassen
    bild_liste[zufall_index][1] -= 1
    slot_bilder.append(bild_liste[zufall_index])
    return bild_liste, slot_bilder




def main():

    rot = (255,20,20)
    schwarz = (0, 0, 0)
    grau = (130,130,130)
    weiß = (255,255,255)

    # Maße
    bild_breite = 50
    bild_hoehe = 50
    bild_abstand = 10
    slot_breite = 60
    slot_hoehe = 180

    #Slot Stati
    # stop_slot = 0
    start_slots = 0
    stop_slot1 = False
    stop_slot2 = False
    stop_slot3 = False
    positioning_slot1 = False
    positioning_slot2 = False
    positioning_slot3 = False

    # Geschwindigkeit
    start_speed = 500
    stop_inc = 2
    start_inc = 10
    lowest_speed = 20
    y1 = start_speed 
    y2 = start_speed 
    y3 = start_speed 

    # Slot-Surfaces
    slot1_surf = pygame.Surface((slot_breite, slot_hoehe))
    slot2_surf = pygame.Surface((slot_breite, slot_hoehe))
    slot3_surf = pygame.Surface((slot_breite, slot_hoehe))

    # Offsets
    scroll1 = 0
    scroll2 = 0
    scroll3 = 0


    screen = pygame.display.set_mode((600, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Slot Machine")

    # Bilder laden
    def load_img(path, width, hight):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (width, hight))

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

    # Slot-Listen vorbereiten
    def init_slot():
        bilder = []
        bild_liste = [zeile[:] for zeile in bild_liste_start]
        for _ in range(4):  # immer 4 Bilder pro Slot aktiv
            bild_liste, bilder = bild_hinzuf(bild_liste, bilder)
        return bild_liste, bilder

    bild_liste1, slot1_bilder = init_slot()
    bild_liste2, slot2_bilder = init_slot()
    bild_liste3, slot3_bilder = init_slot()




    running = True
    clock = pygame.time.Clock()
    # delta_time = 0.1

    
    automat_surf = pygame.Surface((300,450))

    while running:
        delta_time = clock.tick(60) / 1000.0


        screen.fill(weiß)
        #Automat füllen, Slots und Buttons zeichnen
        automat_surf.fill(grau)
        pygame.draw.rect(automat_surf, schwarz, (0, 0, 300, 450), 3)
        pygame.draw.line(automat_surf, schwarz, (0, 87), (300, 87), 3)
        pygame.draw.line(automat_surf, schwarz, (0, 271), (300, 271), 3)

        # Slots bewegen
        def update_slot(scroll, slot_bilder, bild_liste, slot_surf, y, stop_slot, positioning_slot):
            scroll += y * delta_time
            if scroll >= (bild_hoehe + bild_abstand):
                scroll -= (bild_hoehe + bild_abstand)
                slot_bilder.pop(0)
                bild_liste, slot_bilder = bild_hinzuf(bild_liste, slot_bilder)
                occured = [zeile[1] for zeile in bild_liste]  # nur die zweite Spalte
                if sum(occured) == 0:
                    bild_liste = [zeile[:] for zeile in bild_liste_start]
            slot_surf.fill(weiß)
            for i, bild in enumerate(slot_bilder):
                pos_y = (3-i-1) * (bild_hoehe + bild_abstand) + scroll
                slot_surf.blit(bild[0], (bild_abstand // 2, pos_y))
                
            if stop_slot and y > lowest_speed:
                y -= stop_inc
            elif stop_slot and  scroll < stop_inc:
                scroll = 0
                y = 0

            
            return scroll, slot_bilder, bild_liste, y, positioning_slot

        scroll1, slot1_bilder, bild_liste1, y1, positioning_slot1 = update_slot(scroll1, slot1_bilder, bild_liste1, slot1_surf, y1, stop_slot1, positioning_slot1)
        scroll2, slot2_bilder, bild_liste2, y2, positioning_slot2 = update_slot(scroll2, slot2_bilder, bild_liste2, slot2_surf, y2, stop_slot2, positioning_slot2)
        scroll3, slot3_bilder, bild_liste3, y3, positioning_slot3 = update_slot(scroll3, slot3_bilder, bild_liste3, slot3_surf, y3, stop_slot3, positioning_slot3)

        # Slots ins Automaten-Surface zeichnen
        automat_surf.blit(slot1_surf, (30, 90))
        automat_surf.blit(slot2_surf, (120, 90))
        automat_surf.blit(slot3_surf, (210, 90))

        # Automaten-Surface ins Hauptfenster
        screen.blit(automat_surf, (150, 50))
    

        #stop slots
        if stop_button.draw(screen):
            if stop_slot1 == 0: stop_slot1 = 1
            elif stop_slot2 == 0: stop_slot2 = 1
            else: stop_slot3 = 1
                

        # if stop_slot > 0 and y1 > lowest_speed:
        #     y1 -= stop_inc
        # elif y1 <= lowest_speed and positioning_slot < 1:
        #     positioning_slot = 1

        # if stop_slot > 1 and y2 > lowest_speed:
        #     y2 -= stop_inc
        # elif y2 <= lowest_speed and positioning_slot < 2:
        #     positioning_slot = 2

        # if stop_slot > 2 and y3 > lowest_speed:
        #     y3 -= stop_inc
        # elif y3 <= lowest_speed and positioning_slot < 3:
        #     positioning_slot = 3

           # start slots        
        if start_button.draw(screen):
            start_slots = 1

        if start_slots == 1 and y1 < start_speed and stop_slot == 0:
            y1 += start_inc
            y2 += start_inc
            y3 += start_inc     
        
        # Spiel schließen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Screen update
        pygame.display.flip()
        #   delta_time = max(0.001, min(0.1, delta_time))

    pygame.quit()

main()