# TEE PELI TÄHÄN

import pygame
import random
import time
import math


class Alus:
  # Oma avaruusalus-luokka

  def __init__(self, x:int, y:int) -> None:
    self.kuva=pygame.image.load("ship_small.png")
    self.x=x
    self.y=y-self.kuva.get_height() #kuvakkeen alalaita ruudun alalaidassa
 
   
  def piirra(self, naytto):
    naytto.blit(self.kuva, (self.x, self.y ))
  
  def liiku(self, x, max_leveys):
      if self.x+x>0 and self.x+x+self.kuva.get_width()<=max_leveys:
        self.x+=x


class Alien:
  # Alien viholliset-luokka
  def __init__(self, nayton_leveys:int, nayton_korkeus:int, taso:int) -> None:
    self.kuva=pygame.image.load("alien_small.png")
    self.y=random.randint(-nayton_korkeus,0)
    self.x=random.randint(0,nayton_leveys-self.kuva.get_width())
    self.poista=False
    self.poista_laskuri=10
    self.x_suunta=0
    self.y_suunta=1
    self.kulma=0
    if taso==2:
      self.x_suunta=random.randint(-1,1)*3
      self.y_suunta=1
    if taso>=3:
      self.keskipiste_x=random.randint(0,nayton_leveys-self.kuva.get_width())
      self.keskipiste_y=random.randint(-nayton_korkeus,0)
      self.x_suunta=random.randint(-2,2)
      self.y_suunta=1
  
  def piirra(self, naytto):
    naytto.blit(self.kuva, (self.x, self.y))
  
  def siirra(self, taso:int, nayton_leveys:int, nayton_korkeus:int):
    
    if taso==1:
      self.y+=self.y_suunta
    if taso==2:
      self.y+=self.y_suunta
      if self.x_suunta>0:
        if self.x + self.x_suunta <=nayton_leveys:
          self.x+=self.x_suunta
        else:
          self.x_suunta=-self.x_suunta
      if self.x_suunta<0:
        if self.x+self.x_suunta>=0:
          self.x+=self.x_suunta
        else:
          self.x_suunta=-self.x_suunta
    if taso>=3:  
      self.keskipiste_y+=self.y_suunta
      self.x = self.keskipiste_x+math.cos(self.kulma)*100-self.kuva.get_width()/2
      self.y = self.keskipiste_y+math.sin(self.kulma)*100-self.kuva.get_height()/2
      self.kulma+=0.012
      self.keskipiste_x+=self.x_suunta
      if self.x_suunta>0:
        if self.keskipiste_x + self.x_suunta <=nayton_leveys:
          self.keskipiste_x+=self.x_suunta
        else:
          self.x_suunta=-self.x_suunta
      if self.keskipiste_x<0:
        if self.keskipiste_x+self.x_suunta>=0:
          self.keskipiste_x+=self.x_suunta
        else:
          self.x_suunta=-self.x_suunta


class Ammus:
  def __init__(self, x:int, y:int) -> None:
    self.x=x
    self.y=y

  def piirra(self, naytto):
    pygame.draw.line(naytto,(245, 206, 66),(self.x,self.y),(self.x, self.y-20), 5)
  
  def siirra(self):
    self.y-=20


class AloitusAnimaatio:  
  def __init__(self) -> None:
    self.kello=pygame.time.Clock()
    self.vali=0.78
    self.animaatio_kuvakkeet=[]
    self.animaatio_kuvakkeet.append(self.AnimaatioKuvake(0,"ship_small.png")) # lisää animaation yksi oma alus
    for i in range (1,8):
      self.animaatio_kuvakkeet.append(self.AnimaatioKuvake(i*self.vali,"alien_small.png")) # lisää animaation seitsemän Alien alusta

  def pyorita(self, naytto, nayton_leveys, nayton_korkeus):
    for kuvake in self.animaatio_kuvakkeet:
      kuvake.x = round(nayton_leveys/2)+math.cos(kuvake.kulma)*100-kuvake.kuva.get_width()/2
      kuvake.y = round(nayton_korkeus/2-140)+math.sin(kuvake.kulma)*100-kuvake.kuva.get_height()/2
      kuvake.kulma+=0.012
      naytto.blit(kuvake.kuva, (kuvake.x, kuvake.y))
    self.kello.tick(60)

  def nayta_taso_teksti(self, naytto, nayton_leveys, nayton_korkeus, taso, paras_taso):
    self.fontti = pygame.font.SysFont("Arial Bold", 24)
    tasoteksti=self.fontti.render(f"Paras selvitetty", True, (245, 206, 66))
    naytto.blit(tasoteksti,(nayton_leveys/2-tasoteksti.get_width()/2,nayton_korkeus/2-140-tasoteksti.get_height()/2))
    tasoteksti=self.fontti.render(f"taso: {paras_taso}", True, (245, 206, 66))
    naytto.blit(tasoteksti,(nayton_leveys/2-tasoteksti.get_width()/2,nayton_korkeus/2-140-tasoteksti.get_height()/2+20))
  

  class AnimaatioKuvake:
    def __init__(self, kulma:float, kuva:str) -> None:
      self.x=0
      self.y=0
      self.kulma=kulma
      self.kuva=pygame.image.load(kuva)


class AloitusValikko:
  def __init__(self) -> None:
    fontti = pygame.font.SysFont("Arial Bold", 68)
    self.otsikko=fontti.render("Space Invaders", True, (245, 206, 66))
    fontti = pygame.font.SysFont("Arial", 24)
    self.rivi1=fontti.render("F1 = uusi peli", True, (255, 0, 0))
    self.rivi2=fontti.render("F8 = musiikki pois/päälle", True, (255, 0, 0))
    self.rivi3=fontti.render("Esc = poistu", True, (255, 0, 0))
    self.rivi4=fontti.render("Nuoli vasemmalle ja oikealle = liikuta alusta", True, (255, 0, 0))
    self.rivi5=fontti.render("Välilyönti = ammu", True, (255, 0, 0))

  def nayta(self, naytto, nayton_leveys, nayton_korkeus):
    naytto.blit(self.otsikko,(round(nayton_leveys/2-self.otsikko.get_width()/2),round(nayton_korkeus/11)))
    naytto.blit(self.rivi1,(round(nayton_leveys/2-self.otsikko.get_width()/2)-60,round(nayton_korkeus/4)+240))
    naytto.blit(self.rivi2,(round(nayton_leveys/2-self.otsikko.get_width()/2)-60,round(nayton_korkeus/4)+280))
    naytto.blit(self.rivi3,(round(nayton_leveys/2-self.otsikko.get_width()/2)-60,round(nayton_korkeus/4)+320))
    naytto.blit(self.rivi4,(round(nayton_leveys/2-self.otsikko.get_width()/2)-60,round(nayton_korkeus/4)+360))
    naytto.blit(self.rivi5,(round(nayton_leveys/2-self.otsikko.get_width()/2)-60,round(nayton_korkeus/4)+400))
  


class SpaceInvaders:
  def __init__(self) -> None:
    pygame.init()
    pygame.display.set_caption("Space Invaders")
    self.naytto = pygame.display.set_mode((1024,800))
    self.nayton_leveys, self.nayton_korkeus = pygame.display.get_surface().get_size()
    self.kello=pygame.time.Clock()
    
    #Taustamusiikki ja äänitehosteet:
    pygame.mixer.music.load("background_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    self.music_paused=False
    self.laser_aani=pygame.mixer.Sound("laser.wav")
    self.rajahdys_aani=pygame.mixer.Sound("explosion.wav")
    
    self.peli_kaynnissa=False
    self.tappio=False
    self.taso_lapaisty=False
    self.taso=1 #aloitustaso
    self.paras_taso=1 #paras taso tällä pelikerralla

    self.nayta_aloitussivu()


  def nayta_aloitussivu(self):
    animaatio=AloitusAnimaatio()
    valikko=AloitusValikko()
    self.peli_kaynnissa=False
    self.pisteet=0
    self.aluksen_suunta=0
    while True:
      self.naytto.fill((0,0,0))   
      animaatio.pyorita(self.naytto, self.nayton_leveys, self.nayton_korkeus)
      valikko.nayta(self.naytto, self.nayton_leveys, self.nayton_korkeus)
      animaatio.nayta_taso_teksti(self.naytto, self.nayton_leveys, self.nayton_korkeus, self.taso, self.paras_taso)
      pygame.display.flip()
      self.tutki_tapahtumat()

  def uusi_peli(self):
    self.aliens=[]
    self.ammukset=[]
    self.peli_kaynnissa=True
    self.tappio=False
    self.taso_lapaisty=False
    if self.taso==1:
      maara=20
    elif self.taso==2:
        maara=25
    else:
        maara=30
    for i in range (0,maara):
      self.aliens.append(Alien(self.nayton_leveys,self.nayton_korkeus, self.taso))
    self.alus=Alus(round(self.nayton_leveys/2),self.nayton_korkeus)
    self.silmukka()
      
  def silmukka(self):
    while True:
      self.tutki_tapahtumat()
      if self.peli_kaynnissa:
        self.tarkista_loppu()
        self.poista_turhat_ammukset()
        self.tarkista_osuma()
      self.piirra_naytto()

  def nayta_ylarivi(self):
    fontti = pygame.font.SysFont("Arial boldD", 32)
    teksti=fontti.render(f"Taso: {self.taso}  paras selvitetty taso: {self.paras_taso}", True, (255, 0, 0))
    self.naytto.blit(teksti, (10,10)) 
    teksti=fontti.render(f"Pisteet: {self.pisteet}", True, (255, 0, 0))
    self.naytto.blit(teksti, (self.nayton_leveys-teksti.get_width()-10,10))
  
  def poista_turhat_ammukset(self):
    for ammus in self.ammukset:
      if ammus.x<0:
        self.ammukset.remove(ammus)  

  def tutki_tapahtumat(self):
    for tapahtuma in pygame.event.get():
      if tapahtuma.type==pygame.KEYDOWN:
        if self.peli_kaynnissa:
          if tapahtuma.key==pygame.K_LEFT:
            self.aluksen_suunta=-4
          if tapahtuma.key==pygame.K_RIGHT:
            self.aluksen_suunta=4
          if tapahtuma.key==pygame.K_SPACE:
            self.ammukset.append(Ammus(self.alus.x+round(self.alus.kuva.get_width()/2),self.alus.y))
            self.laser_aani.play()
            self.aluksen_suunta=0
        else:
          if tapahtuma.key==pygame.K_F3 and self.taso_lapaisty:
            self.taso+=1
            self.uusi_peli()
        if tapahtuma.key==pygame.K_F1:
          self.uusi_peli()
        if tapahtuma.key==pygame.K_F2:
          self.nayta_aloitussivu()
        if tapahtuma.key==pygame.K_F8:
          if self.music_paused==False:
            pygame.mixer.music.pause()
            self.music_paused=True
          else:
            pygame.mixer.music.unpause()
            self.music_paused=False
        if tapahtuma.key == pygame.K_ESCAPE:
          exit()
      if self.peli_kaynnissa:
        if tapahtuma.type==pygame.KEYUP:
          self.aluksen_suunta=0
      if tapahtuma.type==pygame.QUIT:
        exit()
  
  def piirra_naytto(self):
    if self.peli_kaynnissa:
      self.naytto.fill((0,0,0)) 
      self.nayta_ylarivi()
      self.alus.liiku(self.aluksen_suunta, self.nayton_leveys)
      self.alus.piirra(self.naytto)
      for alien in self.aliens:
        alien.piirra(self.naytto)
        alien.siirra(self.taso, self.nayton_leveys, self.nayton_korkeus)
        if alien.poista==True:
          alien.poista_laskuri-=1
          if alien.poista_laskuri==0:
            self.aliens.remove(alien)
      for ammus in self.ammukset:
        ammus.piirra(self.naytto)
        ammus.siirra()
    else:
      self.naytto.fill((0,0,0))
      self.nayta_ylarivi()
      if len(self.aliens)==0:
        fontti=pygame.font.SysFont("Arial bold", 64)
        teksti1=fontti.render(f"Voitit!", True, (0, 255, 0))
        fontti=pygame.font.SysFont("Arial", 24)
        teksti2=fontti.render("F3 = seuraava taso, F1 = pelaa taso uudestaan, F2 = valikkoon, Esc = poistu", True, (0, 255, 0))
      else:  
        fontti=pygame.font.SysFont("Arial bold", 64)
        teksti1=fontti.render(f"Hävisit...", True, (255, 0, 0))
        fontti=pygame.font.SysFont("Arial", 24)
        teksti2=fontti.render("F1 = pelaa taso uudestaan, F2 = valikkoon, Esc = poistu", True, (255, 0, 0))
      self.naytto.blit(teksti1, (round(self.nayton_leveys/2-teksti1.get_width()/2), round(self.nayton_korkeus/2-teksti1.get_height()/2)))
      self.naytto.blit(teksti2, (round(self.nayton_leveys/2-teksti2.get_width()/2), round(self.nayton_korkeus/2-teksti2.get_height()/2)+60))
    pygame.display.flip()
    self.kello.tick(60)
    
  def tarkista_osuma(self):
    for alien in self.aliens:
      for ammus in self.ammukset:
        if not alien.poista and ammus.x>alien.x and ammus.x<alien.x+alien.kuva.get_width() and ammus.y>0 and ammus.y>alien.y and ammus.y<alien.y+alien.kuva.get_height():
          alien.kuva=pygame.image.load("explode_small.png")
          self.rajahdys_aani.play()
          alien.poista=True
          self.pisteet+=1
          self.ammukset.remove(ammus)
    
  def tarkista_loppu(self):
    if len(self.aliens)==0: #onko listassa yhtään Alienia?
      self.peli_kaynnissa=False
      self.taso_lapaisty=True
      if self.taso>self.paras_taso:
        self.paras_taso=self.taso
      return # voitto
    for alien in self.aliens:
      if alien.y>=self.nayton_korkeus:
        self.peli_kaynnissa=False
        self.tappio=True
        break
    for alien in self.aliens:
      if alien.x>self.alus.x and alien.x<self.alus.x+self.alus.kuva.get_width() and alien.y+alien.kuva.get_height()>self.alus.y and alien.y+alien.kuva.get_height()<self.alus.y+self.alus.kuva.get_height():
        self.peli_kaynnissa=False
        self.tappio=True
        break
    if self.tappio:
        self.alus.kuva=pygame.image.load("explode_small.png")
        self.naytto.blit (self.alus.kuva, (self.alus.x, self.alus.y))
        pygame.display.flip()
        self.rajahdys_aani.play()
        time.sleep(1)


if __name__ == "__main__":
  SpaceInvaders()