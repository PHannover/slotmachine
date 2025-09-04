import pygame
import random

pygame.init()

# Farben
rot = (255, 20, 20)
schwarz = (0, 0, 0)
grau = (130, 130, 130)
weiß = (255, 255, 255)

# Maße
bild_breite = 50
bild_hoehe = 50
bild_abstand = 10
slot_breite = 60
slot_hoehe = 200

# Geschwindigkeit
y = 200   # Pixel pro Sekunde

def bild_hinzuf(bild_liste, slot_bilder):
    gefiltert_indices = [i for i, zeile in enumerate(bild_liste) if zeile[1] > 0]
    zufall_index = random.choice(gefiltert_indices)
    bild_liste[zufall_index][1] -= 1
    slot_bilder.append(bild_liste[zufall_index])
    return bild_liste, slot_bilder

def main():
    screen = pygame.display.set_mode((600, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Slot Machine")

    # Bilder laden
    def load_img(path):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (bild_breite, bild_hoehe))

    kirsche_img = load_img('bilder/Kirsche.png')
    sieben_img = load_img('bilder/7.png')
    apfel_img = load_img('bilder/apfel.png')
    armor_img = load_img('bilder/armor.png')
    book_img = load_img('bilder/book.png')
    erdblock_img = load_img('bilder/erdblock.png')
    glocke_img = load_img('bilder/glocke.png')

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

    # Slot-Surfaces
    slot1_surf = pygame.Surface((slot_breite, slot_hoehe))
    slot2_surf = pygame.Surface((slot_breite, slot_hoehe))
    slot3_surf = pygame.Surface((slot_breite, slot_hoehe))

    # Offsets
    scroll1 = 0
    scroll2 = 0
    scroll3 = 0

    clock = pygame.time.Clock()
    running = True

    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Hintergrund
        screen.fill(weiß)

        # Automat-Hintergrund
        automat_surf = pygame.Surface((300, 450))
        automat_surf.fill(grau)
        pygame.draw.rect(automat_surf, schwarz, (0, 0, 300, 450), 3)
        pygame.draw.line(automat_surf, schwarz, (0, 67), (300, 67), 3)
        pygame.draw.line(automat_surf, schwarz, (0, 271), (300, 271), 3)

        # Slots bewegen
        def update_slot(scroll, slot_bilder, bild_liste, slot_surf):
            scroll += y * delta_time
            if scroll >= (bild_hoehe + bild_abstand):
                scroll -= (bild_hoehe + bild_abstand)
                slot_bilder.pop(0)
                bild_liste, slot_bilder = bild_hinzuf(bild_liste, slot_bilder)
            slot_surf.fill(weiß)
            for i, bild in enumerate(slot_bilder):
                pos_y = i * (bild_hoehe + bild_abstand) - scroll
                slot_surf.blit(bild[0], (bild_abstand // 2, pos_y))
            return scroll, slot_bilder, bild_liste

        scroll1, slot1_bilder, bild_liste1 = update_slot(scroll1, slot1_bilder, bild_liste1, slot1_surf)
        scroll2, slot2_bilder, bild_liste2 = update_slot(scroll2, slot2_bilder, bild_liste2, slot2_surf)
        scroll3, slot3_bilder, bild_liste3 = update_slot(scroll3, slot3_bilder, bild_liste3, slot3_surf)

        # Slots ins Automaten-Surface zeichnen
        automat_surf.blit(slot1_surf, (30, 70))
        automat_surf.blit(slot2_surf, (120, 70))
        automat_surf.blit(slot3_surf, (210, 70))

        # Automaten-Surface ins Hauptfenster
        screen.blit(automat_surf, (150, 50))

        pygame.display.flip()

    pygame.quit()

main()
