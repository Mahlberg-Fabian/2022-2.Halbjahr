from cmath import cos, sin
import pygame
from pygame.constants import (
    QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_TAB, K_KP_PLUS, K_KP_MINUS, K_F10, K_LEFT, K_RIGHT, K_UP, K_DOWN, K_SPACE)
import os
import random
import time


class Settings:                                                 # Klasse Settings um Einstellungen zu treffen, sowie z.B. Bilder speicherorte abzurufen
    window_width = 800                                         # Fensterbreite
    window_height = 500                                         # Fensterhöhe
    fps = 60                                                    # fps einstellen (Bilder pro Sekunde), 60x die Sekunde
    file_path = os.path.dirname(os.path.abspath(__file__))      # Pfad für Dateien 
    image_path = os.path.join(file_path, "images")              # Pfad und Ordner für Bilder

    @staticmethod
    def get_dim():
        return (Settings.window_width, Settings.window_height)


class Globals:
    points = 0                                                  # Punktevariable auf 0 gesetzt



class Background(pygame.sprite.Sprite):
    def __init__(self, filename):
        super().__init__()
        self.image = pygame.image.load(os.path.join(Settings.image_path, filename)).convert()   # Image wird geladen / convert() = Bitmap wird in ein Format geladen, damit es schneller / effizienter arbeiten kann
        self.image = pygame.transform.scale(self.image, Settings.get_dim())                     # Skalierung -> Damit das Bitmap auf die größe des Bildschirms passt
        self.rect  = self.image.get_rect()                                                      # dadurch bekommt man ein Rechteck           

    def draw(self, screen):
        screen.blit(self.image, self.rect)                                                      # Hintergrund wird auf Bildschirm gezeichnet

    def update(self):
        pass


class Kaefer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = []
        self.images.append(pygame.image.load(os.path.join(Settings.image_path, "spritesheet.jpg")).convert_alpha())                # Image laden | convert.alpha() -> Alphakanal soll erhalten bleiben / hintergrund soll unsichtbar gemacht werden
        self.images.append(pygame.image.load(os.path.join(Settings.image_path, "spritesheet.jpg")).convert_alpha())            # Image laden
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = Settings.window_height  //2                                                                   # Der Marienkäfer spawnt -> -10 verschiebt den Käfer etwas nach oben (damit es nicht so aussieht, als würde der Käfer direkt auf der Bildkante aufliegen)
        self.rect.centerx = Settings.window_width  //2                                                                     # Käfer spawnt in der Mitte
        self.speed = 4                                                                                                       # Geschwindigkeit 4, wenn er sich bewegt
        self.speed_h = 0                                                                                                     # Horizontale Bewegung Initialisieren als Variable
        self.speed_v = 0                                                                                                     # Vertikale Bewegung Initialisieren als Variable
        self.time_between_jump = 2000                            
        self.time_next_possible_jump = pygame.time.get_ticks()                                                               # get ticks = kontrolliert die Zeit seit Spielstart. Wenn Anzahl größer als time_next_possible_jump, dann kann sie aufgerufen werden
        self.triesalive = 4




    def draw(self, screen):
        if self.can_jump():
            self.image = self.images[0]

        else:
            self.image = self.images[1]

        screen.blit(self.image, self.rect)

    
    def update(self):
        newpos = self.rect.move(self.speed_h, self.speed_v)                     # Anzahl der Pixel, die der obere Rand des Sprites und der linke Rand des Sprites verändert ; Speicherung als ein neues rect
        if newpos.left >= 0 and newpos.right <= Settings.window_width:          # Linker Rand und rechter Rand des Bitmaps festlegen bzw. der Käfer darf den linken Rand nicht übergehen
            if newpos.top >= 0 and newpos.bottom <= Settings.window_height:     # Oberer Rand und unterer Rand des Bitmaps wird nicht mehr überschritten
                self.rect = newpos


    def can_jump(self):
        return pygame.time.get_ticks() >= self.time_next_possible_jump          # Wenn die Anzahl der Millisekuden größer oder gleich 2000, dann liefert das return einen True-Wert zurück, wenn nciht False


    def jump(self):
        if self.can_jump():
            self.rect.left = random.randint(0, Settings.window_width - self.rect.width)          # Zufällige Position mit random randint. X-Achse
            self.rect.top = random.randint(0, Settings.window_height - self.rect.height)         # "" für Y-Achse
            self.time_next_possible_jump = pygame.time.get_ticks() + self.time_between_jump      # Pause-Wert einbinden
            


    
    def move_stop(self):
        self.speed_h = self.peed_v = 0            # setzt die Speedvariablen auf 0
        self.speed_v = self.speed_h = 0
    
    def move_left(self):
        pygame.transform.rotate()            # horizontale Variable wird auf -4 gesetzt (y-Koordinate verringert sich, somit wandert sie nach oben)

    def move_right(self):
        self.speed_h =  1 * self.speed            # horizontale Variable wird auf +4 gesetzt ( y-koordinate erhöt sich, somit wandert sie nach unten)

    def move_up(self):
        angle = 0
        self.speed_v = self.speed_v - sin(angle)
        self.speed_h = self.speed_h - cos(angle)

    def move_down(self):
        self.speed_v =  1 * self.speed            # vertikale Variable wird auf +4 gesetzt



    def gametries(self):
        self.rect.bottom = Settings.window_height - 10      # Bitmap auf Y-Achse verschieben (unten, etwas nach oben)
        self.rect.centerx = Settings.window_width // 2      # Bitmap auf X-Achse verschieben (mittig)
       





class Apfel(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        r = random.randint(0, 4)                                                                             # Zufallszahl erzeugen von 0 - 4
        self.image = pygame.image.load(os.path.join(Settings.image_path, f"spritesheet.jpg")).convert_alpha()   # Zufallszahl wird in "{r}" eingesetzt
        self.rect = self.image.get_rect()
        self.rect.top = 0                                                                                    # Y Startposition = 0 == Äpfel spawnen oben
        self.rect.left = random.randint(0, Settings.window_width - self.rect.width)                          # Zufallszahl generieren zwischen 0 und der Breite
        self.speed = random.randint(1, 4)                                                                    # Zufällige geschwindigkeit zwiwschen 1 und 4
        self.randompos()                                                                                     # randompos wird aufgerufen

    def randompos(self):
        self.rect.left = random.randint(0, Settings.window_width - self.rect.width)                          # zufällige Position wird erstellt
        


    def update(self):
        self.rect.move_ip(0, self.speed)                                                                     # X-Wert = 0 -> Y-Koordinate verändert sich mit der Geschwindigkeit (speed) ; move_ip = move in place = Variable führt ein Update der rect Variable durch
        if self.rect.top > Settings.window_height:                                                           # Wenn der Apfel am unteren Fensterrand angekommen ist, dann 
            self.kill()                                                                                      # wird er gelöscht (löst sich auf)
            Globals.points += 1


    def draw(self, screen):
        screen.blit(self.image, self.rect)                                                                    # Äpfel auf den Bildschirm zeichnen



class Game(object):

    def __init__(self):
        pygame.init()                                                                  # Start von Python Modulen
        self.screen = pygame.display.set_mode(Settings.get_dim())                      # screen wird erzeugt
        pygame.display.set_caption("Das Apfelspiel")                                   # Überschrift des Games setzen
        self.clock = pygame.time.Clock()                                               # Clock = Syncronisation der FPS
        self.background = Background("hintergrund.png")                                 # Hintergrund einfügen
        self.kaefer = Kaefer()
        self.all_aepfel = pygame.sprite.Group()                                        # Alle Äpfel werden in einer Pygame Group gespeichert
        self.time_between_apfelbirth = 500                                             # alle 500 Millisekunden spawnt ein neuer Apfel
        self.time_next_possible_apfelbirth = pygame.time.get_ticks()    
        self.time_between_time_decrement = 5000                                        # 5000ms bis mehr Äpfel spawnen                                                            
        self.time_next_possible_time_decrement = pygame.time.get_ticks() 
        self.font_normalsize = pygame.font.Font(pygame.font.get_default_font(), 12)    # Größe des textes bestimmen für "normale Größe"
        self.font_bigsize = pygame.font.Font(pygame.font.get_default_font(), 40)       #          ""                für "große Größe"
        



    def watch_for_events(self):
        for event in pygame.event.get():                               
            if event.type == QUIT:                                  
                self.running = False                                 # Fenster wird zum schließen aufgefordert
            elif event.type == KEYDOWN:                              #                         gedrükt
                if event.key == K_ESCAPE:                            # Wenn die Escape Taste            wurde
                    self.running = False                             # setzt self.running auf False. Damit wird es weiter unten zum schließen aufgefordert
                elif event.key == K_LEFT:                            # Bei Tastendruck von Pfeiltaste links
                    self.kaefer.move_left()                          # Käfer läuft nach links
                elif event.key == K_RIGHT:                           # Bei Tastendruck von Pfeiltaste rechts
                    self.kaefer.move_right()                         # Käfer läuft nach rechts  
                elif event.key == K_UP:                              # Bei Tastendruck von Pfeiltaste oben
                    self.kaefer.move_up()                            # Käfer läuft nach oben
                elif event.key == K_DOWN:                            # Bei Tastendruck von Pfeiltaste unten
                    self.kaefer.move_down()                          # Käfer läuft nach unten
                elif event.key == K_SPACE:                           # Bei Tastendruck der SPACE Taste
                    self.jump()                                      # Käfer springt zu einem zufälligen Ort -> Zugriff auf def jump
            elif event.type == KEYUP:                                # Beim loslassen der Pfeiltasten
                if event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP or event.key == K_DOWN: 
                    self.kaefer.move_stop()                          # Bewegung der´s Käfers wird gestoppt
                    



    def draw(self):
        self.background.draw(self.screen)                            # Hintergrund wird gezeichnet
        self.kaefer.draw(self.screen)                                # Käfer wird gezeichnet
        self.all_aepfel.draw(self.screen)                            # Die Äpfel werden auf den Bildschirm gezeichnet
        text = self.font_normalsize.render(f"Points: {Globals.points}", True, (0, 0, 255))
        self.screen.blit(text, (0, 10))                              # Text wird auf den Bildschirm gezeichnet
        pygame.display.flip()
  

    def update(self):
        self.dec_time_between_apfelbirth()
        if pygame.time.get_ticks() > self.time_next_possible_apfelbirth:
            r = Apfel()                                                       # Äfel wird gebaut
            tries = 100                                                       # 100 Versuche ; Anzahl der Versuche werden gemerkt
            while tries > 0:                                                  # Wenn die Versuche größer als 0 sind, dann soll...
                if pygame.sprite.spritecollide(r, self.all_aepfel, False):    # Prüft ob Äpfel miteinander kollidieren
                    r.randompos()                                             # Wenn sie kollidieren, wird eine neue zufällige Startposition gesucht
                    tries -= 1                                                # Versuche um 1 minimieren               
                else:                                                         # Wenn keine Kollision erkann wird...
                    self.all_aepfel.add(r)                       
                    break                                                     # ... dann soll die Schleife verlassen werden        
            self.time_next_possible_apfelbirth = pygame.time.get_ticks() + self.time_between_apfelbirth
        self.kaefer.update()                                                  # Käfer updaten
        self.all_aepfel.update()                                              # Äpfel updaten
        
        if self.kaefer.triesalive > 0:                                                         # Variable auf 3 gesetzte. (Spieler hat 3 Leben)
            if pygame.sprite.spritecollide(self.kaefer, self.all_aepfel, False):               # Wenn eine Kollision zwischen einem Apfel und dem Käfer vorkommt dann...                                                # Wenn Variable von triesgame größer als 0 ist...
                self.kaefer.gametries()                                                        # ...dann wrd gametries() in der Klasse Käfer aufgerufen
                self.kaefer.triesalive -= 1                                                    # wenn aufgerufen -> Variable wird um 1 verringern
        else:                                                                                  # wenn mehr als triesgame == 0
            self.running = False                                                               # Hauptprogrammschleife = False -> Spiel wird beendet
                
            
                                                                


    def jump(self):
        tries = 3                                                                 # 3 Versuche
        while tries > 0:                                                          # Wenn tries über 0 liegt...     
            self.kaefer.jump()                                                    #...wird die Methode Käfer jump aufgerufen
            if pygame.sprite.spritecollide(self.kaefer, self.all_aepfel, True):   # überprüfung ob eine Kollision stattfindet
                self.kaefer.jump()                                                # Wenn ja, wird der Sprung wiederholt
                tries -= 1                                                        # Versuche wird um 1 minimiert
            else:                                                                 # wenn nicht
                break                                                             # springen nicht mehr dulden



    def run(self):                                                   
        self.running = True                                          # Steuert, ob die Hauptprogrammschleife läuft                         
        while self.running:                                          # setzt in Kraft, wenn Pygame zum schließen aufgefordert wurde
            self.clock.tick(Settings.fps)                            # Syncronisation auf 60 FPS                    
            self.watch_for_events()                                  # prüfen auf Tastatur / Mauseingaben (events) 
            self.update()                                            # updaten
            self.draw()                                              # Alle Spielelemente werden 
        self.game_over()                                             # wenn self.running auf False gesetzt wird, wird game over aufgerufen

        pygame.quit()                                                # Falls die Hauptprogammschleife beendet wird, wird pygame hier geschlossen


    def dec_time_between_apfelbirth(self):
        if pygame.time.get_ticks() >= self.time_next_possible_time_decrement:                                           # Wenn die Wartezeit zuende ist...
            if self.time_between_apfelbirth >= 20:                                                                      # ...Wenn Apfelbirth größer gleich 20 ist...
                self.time_between_apfelbirth -= 10                                                                      #  ... wird Apfelbirth um 10 verringert
            self.time_next_possible_time_decrement = pygame.time.get_ticks() + self.time_next_possible_time_decrement


    def game_over(self):                                                   # Game Over Overlay einbinden
        text = self.font_bigsize.render("GAME OVER", True, (255, 0, 136))  # "GAME OVER" Anzeige einstellen. Text, aktiv/nicht aktiv, Farbe)
        rect = text.get_rect()
        rect.centerx = Settings.window_width //2                           # Position der X-Koordinate
        rect.centery = Settings.window_height //2 - 50                     # Position der Y-Koordinate
        self.screen.blit(text, rect)
        text = self.font_bigsize.render(f"Score: {Globals.points}", True, (0, 136, 255))   # Punkteanzeige einstellen. Text, Punkte aus String lesen, aktiv/inaktiv, Farbe
        rect = text.get_rect()
        rect.centerx = Settings.window_width //2                          # Position der X-Koorinate 
        rect.centery = Settings.window_height //2 + 50                    # Position der Y-Koordinate
        self.screen.blit(text, rect)
        pygame.display.flip()
        time.sleep(3)                                                     # Timer auf 3 Sekunden gesetzt
        
        


if __name__ == '__main__':
        os.environ['SDL_VIDEO_WINDOW_POS'] = "450, 40"                   # Fensterposition auf Bildschirm

        game = Game()                                                                   
        game.run()                                                       # Game starten
        





# Quellen:
# Apfel Bitmap:        https://www.pngwing.com/de/free-png-bnets 
# Marienkäfer Bitmap:  https://www.pngwing.com/de/free-png-mavei
# Hintergrund:         https://freestockgallery.de/natur/apfelbaum-mit-pfeln-792/
