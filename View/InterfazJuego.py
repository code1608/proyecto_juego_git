#SOLO FALTA QUE LA NAVE tenga un escudo y sonidos
import mysql.connector
from tkinter import messagebox
import pygame
import random
from Controller.ControladorTablaPosicion import registrar_puntaje, obtener_puntajes
from View.TablaPosicion import TablaPosicion

class InterfazJuego:
    def __init__(self, usuario_actual):
        
        self.jefe = None  # Inicialmente no hay jefe

        self.usuario_actual = usuario_actual
        
        
        if not self.usuario_actual:
            raise ValueError("El usuario actual no está autenticado correctamente.")
        
        
        pygame.init()

        # Dimensiones de la pantalla
        self.ANCHO, self.ALTO = 1000, 800  # Asegúrate de que esto esté definido en la clase
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("Juego estilo Galaga")

        # Colores
        self.NEGRO = (0, 0, 0)
        self.BLANCO = (255, 255, 255)
        self.ROJO = (255, 0, 0)
        self.VERDE = (0, 255, 0)  

        # Fuentes
        self.fuente = pygame.font.SysFont("Arial", 30)

        # Fondo
        self.fondo = pygame.image.load(r"img\space.jpg")
        self.fondo = pygame.transform.scale(self.fondo, (self.ANCHO, self.ALTO))

        # Configuración de la nave
        self.nave_imagen = pygame.image.load(r"img\astronave.png")
        self.nave_imagen = pygame.transform.scale(self.nave_imagen, (self.nave_imagen.get_width() // 5, self.nave_imagen.get_height() // 5))
        self.nave_rect = self.nave_imagen.get_rect(center=(self.ANCHO // 2, self.ALTO - 60))
        self.velocidad_nave = 6
        
        #poderes
        self.poderes = [] 
        
        # Corazones
        self.corazon_imagen = pygame.image.load(r"img\love-always-wins.png")
        self.corazon_imagen = pygame.transform.scale(self.corazon_imagen, (50, 50))
        self.vidas = 3  # Inicializa el número de vidas
        self.corazones = [self.corazon_imagen for _ in range(self.vidas)]  # Lista para mostrar corazones visualmente
        self.juego_terminado = False  # El juego comienza en estado activo

        
        # Imágenes de poderes
        self.imagenes_poderes = {
            "proyectiles_x2": pygame.image.load("img/balas x2.png"),
            "proyectiles_x3": pygame.image.load("img/balas x3.png"),
            "escudo": pygame.image.load("img/proteger.png"),
            "acelerar": pygame.image.load("img/registro-de-tiempo.png"),
        }

        #escudo
        self.escudo_activo = False
        self.tiempo_escudo = 0 
        self.duracion_escudo = 5000
        # Carga y redimensiona la imagen del escudo
        self.escudo_img = pygame.image.load("img/proteger.png").convert_alpha()  
        self.escudo_img = pygame.transform.scale(self.escudo_img, (50, 50))  # Cambia el tamaño según necesites
        self.escudo_rect = self.escudo_img.get_rect()  # Obtiene el rectángulo de la imagen
        # Ajusta la posición del escudo al lado del tercer corazón
        self.escudo_rect.topleft = (20 + 3 * 60 + 10, 60)  # Coloca el escudo al lado del tercer corazón

        # Proyectiles
        self.proyectiles = []
        self.velocidad_proyectil = 10
        self.tiempo_ultimo_disparo = 0  # Inicializa el tiempo del último disparo
        self.proyectiles_extra = 0  # Inicializa la cantidad de proyectiles extra
        self.intervalo_disparo = 15  # Intervalo de disparo inicial
        self.poder_activo = None
        self.tiempo_poder_activo = 0  # Para llevar el tiempo del poder activo
        self.duracion_poder = 5000

        # Configuración de enemigos
        self.enemigo_imagen = pygame.image.load(r"img\enemigos.png")
        self.enemigo_imagen = pygame.transform.scale(self.enemigo_imagen, (50, 50))
        self.enemigo_imagen = pygame.transform.rotate(self.enemigo_imagen, 45)
        self.enemigos = []
        self.velocidad_enemigo = 2
        self.intervalo_enemigos = 60
        

        # Jefe
        self.jefe_imagen = pygame.image.load(r"img\boss.png")
        self.jefe_imagen = pygame.transform.scale(self.jefe_imagen, (200, 200))
        self.jefe = pygame.Rect(self.ANCHO // 2 - 100, -200, 200, 200)
        self.jefe = None  
        self.jefe_proyectiles = []
        self.vida_jefe = 30
        self.jefe_direccion = 1

        # Imagen de disparos del jefe
        self.disparo_jefe_imagen = pygame.image.load(r"img\luz.png")
        self.disparo_jefe_imagen = pygame.transform.scale(self.disparo_jefe_imagen, (40, 60))

        # Variables del juego
        self.puntuacion = 0
        self.nivel = 1
        self.enemigos_destruidos = 0
        self.contador_frames = 0

        # Variables del jefe
        self.tiempo_ultimo_disparo_jefe = 0
        self.intervalo_disparo_jefe = 60
        self.jefe_apareciendo = False
        self.tiempo_aparicion_jefe = 0

    def mover_proyectiles_jefe(self):
        """Mover los proyectiles del jefe."""
        for proyectil in self.jefe_proyectiles[:]:  # Usar [:] para evitar modificar la lista mientras iteras
            proyectil.y += 5  

            # Verifica colisión con la nave
            if proyectil.colliderect(self.nave_rect):
                self.vidas -= 1  # Resta una vida
                print(f"Vidas restantes: {self.vidas}")
                self.jefe_proyectiles.remove(proyectil)  # Elimina el proyectil

                # Verifica si se han acabado las vidas
                if self.vidas <= 0:
                    self.juego_terminado = True
                    print("¡Juego terminado!")

            # Verifica colisión con el jefe
            if self.jefe and proyectil.colliderect(self.jefe):
                self.vida_jefe -= 10  # Ajusta el daño como sea necesario
                self.jefe_proyectiles.remove(proyectil)  # Elimina el proyectil que golpeó al jefe

            # Eliminar proyectiles fuera de pantalla
            elif proyectil.top > self.ALTO or proyectil.bottom < 0 or proyectil.left < 0 or proyectil.right > self.ANCHO:
                self.jefe_proyectiles.remove(proyectil)


    def disparar_jefe(self):
        """Disparar proyectiles desde el jefe."""
        if self.jefe and self.contador_frames - self.tiempo_ultimo_disparo_jefe >= self.intervalo_disparo_jefe:
            if self.vida_jefe <= 3:
                self.jefe_proyectiles.append(pygame.Rect(self.jefe.centerx - 5, self.jefe.top, 10, 20))  
                self.jefe_proyectiles.append(pygame.Rect(self.jefe.centerx - 5, self.jefe.bottom - 20, 10, 20)) 
                self.jefe_proyectiles.append(pygame.Rect(self.jefe.left, self.jefe.centery - 5, 20, 10))  
                self.jefe_proyectiles.append(pygame.Rect(self.jefe.right - 10, self.jefe.centery - 5, 20, 10))  
            else:
                self.jefe_proyectiles.append(pygame.Rect(self.jefe.centerx - 5, self.jefe.bottom, 10, 20))
            self.tiempo_ultimo_disparo_jefe = self.contador_frames

    def aparecer_jefe(self):
        if not self.jefe_apareciendo and self.nivel % 5 == 0 and self.jefe is None:
            self.jefe_apareciendo = True
            self.tiempo_aparicion_jefe = self.contador_frames
            self.jefe = pygame.Rect(self.ANCHO // 2 - 100, -400, 200, 200)  
            self.vida_jefe = 30
            self.mostrar_vida_jefe()

        
    def animar_aparicion_jefe(self):
        if self.jefe_apareciendo:
            if self.jefe is not None and self.jefe.top < 80:  
                self.jefe.y += 5 
            else:
                self.jefe_apareciendo = False


    def dibujar_texto_sombra(self, texto, x, y, color_texto, color_sombra):
        """Dibujar texto con sombra."""
        texto_sombra = self.fuente.render(texto, True, color_sombra)
        self.pantalla.blit(texto_sombra, (x + 2, y + 2))
        texto_final = self.fuente.render(texto, True, color_texto)
        self.pantalla.blit(texto_final, (x, y))

    def mostrar_vida_jefe(self):
        """Dibujar la barra de vida del jefe en la pantalla."""
        barra_vida_ancho = 200
        barra_vida_alto = 20
        
        # Asegúrate de que la vida máxima del jefe esté definida (puede ser una variable inicializada en el constructor)
        if not hasattr(self, 'vida_jefe_maxima'):
            self.vida_jefe_maxima = 30  # Valor predeterminado si no está configurado
        
        # Calcula el porcentaje de vida basado en la vida máxima actual
        porcentaje_vida = self.vida_jefe / self.vida_jefe_maxima
        
        # Dibuja el fondo rojo (vida máxima)
        pygame.draw.rect(self.pantalla, (255, 0, 0), (
            self.ANCHO // 2 - barra_vida_ancho // 2,
            30,
            barra_vida_ancho,
            barra_vida_alto
        ))
        
        # Dibuja la vida restante en verde
        pygame.draw.rect(self.pantalla, (0, 255, 0), (
            self.ANCHO // 2 - barra_vida_ancho // 2,
            30,
            barra_vida_ancho * porcentaje_vida,
            barra_vida_alto
        ))


    def aumentar_vida_jefe(self, incremento):
        """Aumenta la vida máxima y actual del jefe."""
        self.vida_jefe_maxima += incremento
        self.vida_jefe += incremento
    
    def dibujar_corazones(self):
        """Dibuja los corazones restantes en la pantalla."""
        for i in range(self.vidas):
            self.pantalla.blit(self.corazon_imagen, (20 + i * 60, 60))
            
    def dibujar_escudo(self):
        """Dibuja el ícono del escudo si está activo."""
        # Carga y redimensiona la imagen del escudo (puedes hacerlo en la inicialización si no cambia)
        if not hasattr(self, 'escudo_img'):
            self.escudo_img = pygame.image.load("img/proteger.png").convert_alpha()
            self.escudo_img = pygame.transform.scale(self.escudo_img, (50, 50))  # Cambia el tamaño según necesites
            self.escudo_rect = self.escudo_img.get_rect()  # Obtiene el rectángulo de la imagen
            # Ajusta la posición del escudo al lado del tercer corazón
            self.escudo_rect.topleft = (20 + 3 * 60 + 10, 60)  # Coloca el escudo al lado del tercer corazón

        if self.escudo_activo:
            self.pantalla.blit(self.escudo_img, self.escudo_rect.topleft)  # Dibuja el escudo

        # Desactiva el escudo después de su duración
        if self.escudo_activo and (pygame.time.get_ticks() - self.tiempo_escudo > self.duracion_escudo):
            self.desactivar_escudo()  # Llama a la función para desactivar el escudo

    def generar_poder(self, x, y):
        tipos_poderes = {
            "proyectiles_x2": 0.4,  # 40% probabilidad
            "proyectiles_x3": 0.3,  # 30% probabilidad
            "escudo": 0.2,          # 20% probabilidad
            "acelerar": 0.1         # 10% probabilidad
        }
        tipo_poder = random.choices(list(tipos_poderes.keys()), weights=list(tipos_poderes.values()))[0]
        rect_poder = pygame.Rect(x - 25, y - 25, 50, 50)  # Centrado sobre la posición (x, y)
        self.poderes.append({"tipo": tipo_poder, "rect": rect_poder})

    def mover_y_recoger_poderes(self):
        for poder in self.poderes[:]:
            poder["rect"].y += 5  # Mueve el poder hacia abajo
            if poder["rect"].top > self.ALTO:  # Si sale de la pantalla, eliminarlo
                self.poderes.remove(poder)
            elif poder["rect"].colliderect(self.nave_rect):  # Si la nave recoge el poder
                self.poderes.remove(poder)  # Elimina el poder de la lista
                self.tiempo_poder_activo = pygame.time.get_ticks()  # Registrar el tiempo del poder
                
                # Activa el poder correspondiente
                if poder["tipo"] == "proyectiles_x2":
                    self.poder_activo = "x2"  # Activar proyectiles x2
                elif poder["tipo"] == "proyectiles_x3":
                    self.poder_activo = "x3"  # Activar proyectiles x3
                elif poder["tipo"] == "escudo":
                    self.nave_activar_escudo()  # Método para activar el escudo
                elif poder["tipo"] == "acelerar":
                    self.nave_activar_acelerar()  # Método para activar acelerar

    def nave_activar_escudo(self):
        self.escudo_activo = True  # Activa el escudo
        self.tiempo_escudo = pygame.time.get_ticks()  # Marca el tiempo de activación
        self.duracion_escudo = 5000  # Duración del escudo en milisegundos (5 segundos)

    def nave_activar_acelerar(self):
        """Activar aceleración para la nave."""
        self.velocidad_nave += 6  # Aumenta la velocidad de la nave
        self.tiempo_acelerar = pygame.time.get_ticks()  # Registra el tiempo de activación
        self.duracion_acelerar = 5000  # Duración de la aceleración en milisegundos (5 segundos)

    def desactivar_escudo(self):
        self.escudo_activo = False  # Desactivar el escudo

    def desactivar_acelerar(self):
        self.velocidad_nave -= 3  # Restaurar velocidad original
        
    def verificar_poderes(self):
        tiempo_actual = pygame.time.get_ticks()

        # Verifica el estado del poder activo
        if self.poder_activo:
            if tiempo_actual - self.tiempo_poder_activo > self.duracion_poder:
                # Reinicia el poder activo
                if self.poder_activo in ["x2", "x3"]:
                    self.poder_activo = None  # Reinicia el poder activo
                    self.velocidad_nave = 6  # Reinicia la velocidad a su valor original
                else:
                    self.poder_activo = None

        # Verifica si el escudo debe desactivarse
        if self.escudo_activo:
            if tiempo_actual - self.tiempo_escudo > self.duracion_escudo:
                self.desactivar_escudo()  # Desactiva el escudo


    def verificar_aceleracion(self):
        """Verifica si la aceleración ha expirado."""
        if hasattr(self, 'tiempo_acelerar') and self.tiempo_acelerar is not None:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_acelerar > self.duracion_acelerar:
                self.velocidad_nave -= 6  # Restablece la velocidad a su valor original
                self.tiempo_acelerar = None  # Reinicia el tiempo de aceleración

    def disparar_nave(self):
        if self.contador_frames - self.tiempo_ultimo_disparo >= self.intervalo_disparo:
            self.tiempo_ultimo_disparo = self.contador_frames
            
            if self.poder_activo == "x2":  # Si hay poder x2 activo
                for i in range(2):  # Dispara 2 proyectiles
                    # Separa los proyectiles
                    proyectil = pygame.Rect(self.nave_rect.centerx - 15 + i * 30, self.nave_rect.top, 10, 20)  # Ajustar la separación
                    self.proyectiles.append(proyectil)
            elif self.poder_activo == "x3":  # Si hay poder x3 activo
                for i in range(3):  # Dispara 3 proyectiles
                    # Separa los proyectiles
                    proyectil = pygame.Rect(self.nave_rect.centerx - 25 + i * 25, self.nave_rect.top, 10, 20)  # Ajustar la separación
                    self.proyectiles.append(proyectil)
            else:  # Disparo normal
                proyectil = pygame.Rect(self.nave_rect.centerx - 5, self.nave_rect.top, 10, 20)
                self.proyectiles.append(proyectil)

    def verificar_colisiones(self):
        for proyectil in self.jefe_proyectiles[:]:
            if self.nave_rect.colliderect(proyectil):
                print("Colisión detectada")
                self.jefe_proyectiles.remove(proyectil)  # Elimina el proyectil
                
                # Verifica si el escudo está activo
                if not self.escudo_activo:  # Solo reducir vidas si el escudo no está activo
                    if self.vidas > 0:  # Verifica si hay vidas restantes
                        self.vidas -= 1  # Resta una vida
                        print(f"Vidas restantes: {self.vidas}")

                        if self.vidas > 0:  # Solo quita un corazón si aún hay vidas
                            if self.corazones:  # Verifica que haya corazones en la lista
                                self.corazones.pop()  # Elimina el último corazón
                                print(f"Corazones restantes: {self.corazones}")

                    if self.vidas <= 0:  # Si no quedan vidas
                        self.juego_terminado = True
                        print("¡Juego terminado!")
                else:
                    print("Escudo activo, no se reduce vida.")  # Mensaje para indicar que el escudo está activo

                break  # Salir del bucle para evitar conflictos

    def game_over(self):
        font = pygame.font.Font(None, 74)
        texto = font.render("Game Over", True, (255, 0, 0))
        self.pantalla.blit(texto, (self.ANCHO // 2 - texto.get_width() // 2, self.ALTO // 2 - texto.get_height() // 2))

    def manejar_colision_enemigo(self, enemigo, proyectil):
        """Maneja la lógica al destruir un enemigo."""
        self.proyectiles.remove(proyectil)
        self.enemigos.remove(enemigo)
        self.puntuacion += 100
        self.enemigos_destruidos += 1
        
        # Generar poder con probabilidad del 20%
        if random.random() < 0.2:
            self.generar_poder(enemigo.centerx, enemigo.centery)
            
    def manejar_colision_con_jefe(self, proyectil):
        """Maneja la colisión entre un proyectil y el jefe."""
        self.proyectiles.remove(proyectil)

        # Ajusta el daño dependiendo del poder activo
        if self.poder_activo == 'proyectiles_x2':
            self.vida_jefe -= 3  # Daño reducido con x2
        elif self.poder_activo == 'proyectiles_x3':
            self.vida_jefe -= 5  # Daño incrementado con x3
        else:
            self.vida_jefe -= 1  # Daño normal

        # Verifica si el jefe ha sido derrotado
        if self.vida_jefe <= 0:
            self.jefe = None  # Eliminar al jefe si muere
        
        # Actualiza la barra de vida del jefe
        self.mostrar_vida_jefe()
        
    def ejecutar(self):
        ejecutando = True
        self.reloj = pygame.time.Clock() 

        while ejecutando:
            # Rellenar la pantalla y dibujar el fondo
            self.pantalla.fill(self.NEGRO)
            self.pantalla.blit(self.fondo, (0, 0))
            self.contador_frames += 1

            # Sección donde el juego ha terminado
            if self.juego_terminado:
                self.game_over()  # Muestra el mensaje de Game Over
                pygame.display.flip()  # Actualiza la pantalla para mostrar el mensaje

                try:
                    # Verifica que el usuario esté autenticado antes de registrar puntajes
                    if self.usuario_actual:
                        # Registrar el puntaje en la base de datos
                        registrar_puntaje(self.usuario_actual, self.puntuacion)

                        # Obtener los puntajes asociados al usuario actual
                        puntajes = obtener_puntajes(self.usuario_actual)

                        # Depuración: Verificar los puntajes obtenidos
                        print("Puntajes obtenidos:", puntajes)

                        # Mostrar la tabla de posiciones si hay puntajes disponibles
                        if puntajes:
                            TablaPosicion(puntajes)  # Mostrar tabla de posiciones
                        else:
                            messagebox.showinfo("Info", "No hay puntajes disponibles para mostrar.")
                    else:
                        # Caso en el que no haya un usuario autenticado
                        messagebox.showinfo("Info", "No hay usuario autenticado. No se puede guardar el puntaje.")
                except Exception as e:
                    # Manejo de errores durante el registro o la obtención de puntajes
                    messagebox.showerror("Error", f"Error al manejar puntajes: {e}")

                # Salir del bucle después de manejar el Game Over
                ejecutando = False

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        ejecutando = False
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:  # Permite salir al presionar ESC
                            ejecutando = False
                continue  # Salta el resto del bucle si el juego ha terminado


            # Animación del jefe y disparos
            self.animar_aparicion_jefe()
            self.disparar_jefe()
            self.mover_proyectiles_jefe() 
            self.verificar_colisiones()

            # Manejo de eventos
            for evento in pygame.event.get():
                if evento.type == pygame.USEREVENT + 1:  # Evento para desactivar el escudo
                    self.desactivar_escudo()
                elif evento.type == pygame.USEREVENT + 2:  # Evento para desactivar acelerar
                    self.desactivar_acelerar()
                if evento.type == pygame.QUIT:
                    ejecutando = False               
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:  # Disparar al presionar la barra espaciadora
                        self.disparar_nave()

            # Controles de la nave
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a] and self.nave_rect.left > 0:
                self.nave_rect.x -= self.velocidad_nave
            if teclas[pygame.K_d] and self.nave_rect.right < self.ANCHO:
                self.nave_rect.x += self.velocidad_nave

            # Mover proyectiles del jugador
            for proyectil in self.proyectiles[:]:  # Usar copia para evitar modificar la lista durante la iteración
                proyectil.y -= self.velocidad_proyectil
                if proyectil.bottom < 0:
                    self.proyectiles.remove(proyectil)
                    
            # Verificar si el poder activo debe desactivarse
            if self.poder_activo:
                tiempo_actual = pygame.time.get_ticks()
                if tiempo_actual - self.tiempo_poder_activo >= self.duracion_poder:
                    self.poder_activo = None  # Desactivar el poder después de 5 segundos
       
            # Crear enemigos
            if not self.jefe and self.contador_frames % self.intervalo_enemigos == 0:
                enemigo_rect = self.enemigo_imagen.get_rect(topleft=(random.randint(0, self.ANCHO - 50), -50))
                self.enemigos.append(enemigo_rect)

            # Mover enemigos
            for enemigo in self.enemigos[:]:
                enemigo.y += self.velocidad_enemigo
                if enemigo.top > self.ALTO:
                    self.enemigos.remove(enemigo)

            # Colisión entre proyectiles del jugador y enemigos
            for proyectil in self.proyectiles[:]:
                for enemigo in self.enemigos[:]:
                    if proyectil.colliderect(enemigo):
                        self.manejar_colision_enemigo(enemigo, proyectil)
                        break  # Salir del bucle interno para evitar conflictos
                    
            # Lógica de colisión entre la nave y el poder del escudo
            for poder in self.poderes[:]:  # Suponiendo que tienes una lista de poderes en el juego
                if poder["rect"].colliderect(self.nave_rect):  # Verifica si la nave recoge el poder
                    if poder["tipo"] == 'escudo':  # Asegúrate de que el poder sea del tipo escudo
                        self.nave_activar_escudo()  # Activa el escudo
                    self.poderes.remove(poder)  # Elimina el poder de la lista después de recogerlo
                    break  # Salir del bucle


            # Colisión entre la nave y enemigos
            for enemigo in self.enemigos[:]:
                if enemigo.colliderect(self.nave_rect):
                    if not self.escudo_activo:  # Solo restar vidas si el escudo no está activo
                        self.vidas -= 1  # Resta una vida
                        if self.vidas > 0:
                            self.corazones.pop()  # Elimina el último corazón de la lista
                        
                        if self.vidas <= 0:
                            self.juego_terminado = True  # Cambia a estado de juego terminado
                            self.game_over()  # Llama a la función de GAME OVER

                    self.enemigos.remove(enemigo)  # Elimina el enemigo independientemente del escudo
                    break  # Salir del bucle para evitar conflictos
        
            # Colisión entre proyectiles del jugador y el jefe
            for proyectil in self.proyectiles[:]:
                if self.jefe and proyectil.colliderect(self.jefe):
                    self.manejar_colision_con_jefe(proyectil)
                    break  # Salir del bucle para evitar conflictos

            # Dibujo de poderes
            for poder in self.poderes:
                if poder["tipo"] == 'proyectiles_x2':
                    imagen_poder = pygame.transform.scale(self.imagenes_poderes['proyectiles_x2'], (50, 50))  # Ajustar tamaño
                    self.pantalla.blit(imagen_poder, poder["rect"])
                elif poder["tipo"] == 'proyectiles_x3':
                    imagen_poder = pygame.transform.scale(self.imagenes_poderes['proyectiles_x3'], (50, 50))  # Ajustar tamaño
                    self.pantalla.blit(imagen_poder, poder["rect"])
                elif poder["tipo"] == 'escudo':
                    imagen_poder = pygame.transform.scale(self.imagenes_poderes['escudo'], (50, 50))  # Ajustar tamaño
                    self.pantalla.blit(imagen_poder, poder["rect"])
                elif poder["tipo"] == 'acelerar':
                    imagen_poder = pygame.transform.scale(self.imagenes_poderes['acelerar'], (50, 50))  # Ajustar tamaño
                    self.pantalla.blit(imagen_poder, poder["rect"])

            # Incremento de nivel y aparición del jefe
            if self.enemigos_destruidos >= 10 and not self.jefe_apareciendo and not self.jefe:
                self.nivel += 1
                self.velocidad_enemigo += 1
                self.intervalo_enemigos = max(20, self.intervalo_enemigos - 5)
                self.enemigos_destruidos = 0
                
                # Aumentar la velocidad de los proyectiles cada 5 niveles
                if self.nivel % 5 == 0:
                    self.velocidad_proyectil += 5  # Aumenta la velocidad de los proyectiles en 1

                # Crear jefe cada 5 niveles
                if self.nivel % 5 == 0:
                    self.aparecer_jefe()
                    self.aumentar_vida_jefe(20)  # Incrementa 50 puntos de vida

            # Mover el jefe
            if self.jefe and not self.jefe_apareciendo:
                self.jefe.x += self.jefe_direccion * 3
                if self.jefe.left < 0 or self.jefe.right > self.ANCHO:
                    self.jefe_direccion *= -1

            # Dibujar elementos en pantalla
            self.pantalla.blit(self.nave_imagen, self.nave_rect)
            for enemigo in self.enemigos:
                self.pantalla.blit(self.enemigo_imagen, enemigo)
            for proyectil in self.proyectiles:
                pygame.draw.rect(self.pantalla, self.BLANCO, proyectil)
            for proyectil in self.jefe_proyectiles:
                self.pantalla.blit(self.disparo_jefe_imagen, proyectil)

            if self.jefe:
                self.pantalla.blit(self.jefe_imagen, self.jefe)
                self.mostrar_vida_jefe() 
            
            self.verificar_poderes()
            self.verificar_aceleracion()    
            self.dibujar_corazones()
            self.dibujar_escudo()
            self.mover_y_recoger_poderes()  # Llama al método para recoger poderes
            self.dibujar_texto_sombra(f"Puntuación: {self.puntuacion}", 20, 20, self.BLANCO, self.NEGRO)
            self.dibujar_texto_sombra(f"Nivel: {self.nivel}", self.ANCHO - 150, 20, self.BLANCO, self.NEGRO)

            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()
        
