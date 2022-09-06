#Importação do Sys, OpenCV, Numpy e Pyautogui
import sys
import cv2 as cv
import numpy as np
import pyautogui as pyag

#Função que passa a mascara de uma cor e o número para colorir o contorno, de acordo com a cor passada
# faz uma ação
def contornoCor(mask, cor):
    #Faz o contorno da mask tendo como modo de recuperação apenas sinalizadores externo e o 
    # método de aproximação sendo simples
    contornos, _ = cv.findContours(
        mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    
    for contorno in contornos:
        #Pega a area de contorno de cada contorno
        area = cv.contourArea(contorno)

        #O if faz a captura apenas dos objetos que tenha area maior que 1500
        if area > 1500:
            #Usado para pegar um retangulo aproximado ao redor da imagem, pegando suas coordenadas e 
            # altura/largura
            (x, y, w, h) = cv.boundingRect(contorno)

            #Verifica e corrige uma curva quanto a defeitos de convexidade 
            novoContorno = cv.convexHull(contorno)

            #Utilizado para desenhar os contornos, corrigindo os defeitos de convexidade e passando 
            # uma cor para o contorno
            cv.drawContours(frame, [novoContorno], 0, cor, 3)

            #Utilizado para escrever um texto na imagem, aqui excreve o X e Y do objeto
            cv.putText(
                frame,
                str(f"x: {x} y: {y}"),
                (x, y-20),
                cv.FONT_HERSHEY_SIMPLEX,
                1, 1
            )

            #Se a cor for azul faz o seguinte:
            if cor == (255, 0, 0):
                #Diminui a área na camera para capturar a cor e mexer de acordo com ela,
                #isso diminui quanto que tem que mexer na cor para chegar nos cantos.
                widthCaptura = widthCam - 130
                heightCaptura = heightCam - 130

                #Converter coordenadas da camera com a tela
                x = np.interp(x, (70, widthCaptura), (0, resoluçãoTelaW))
                y = np.interp(y, (70, heightCaptura), (0, resoluçãoTelaH))

                #Move o mouse de acordo com as coordenadas x y
                pyag.moveTo(x, y)
            #Se a cor for verde faz o seguinte:
            elif cor == (0, 255, 0):
                #O mouse da um click com o esquerdo na posição
                pyag.click()
            #Se a cor for amarelo faz o seguinte:
            elif cor == (0, 255, 255):
                #O mouse da um click com o direito na posição
                pyag.click(button='right')
            #Se a cor for vermelho faz o seguinte:
            elif cor == (0, 0, 255):
                #Fecha o sistema
                sys.exit()

#Captura a camera do note
camera = cv.VideoCapture(0, cv.CAP_DSHOW)

#Desabilita o fail-safe do pyautogui
pyag.FAILSAFE = False

#Captura o tamanho da tela
resoluçãoTelaW, resoluçãoTelaH = pyag.size()

while 1:
    #Pega o quadro/camera atual
    _, frame = camera.read()

    #Inverte a imagem horizonaltamente
    frame = cv.flip(frame, 1)

    #captura o tamanho da imagem
    heightCam, widthCam, bppCam = np.shape(frame)

    #Transforma a imagem em HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    #HSV do azul com baixo e alto
    lowerBlue = np.array([102, 74, 112])
    upperBlue = np.array([125, 255, 255])
    
    #HSV do verde com baixo e alto
    lowerGreen = np.array([50, 90, 175])
    upperGreen = np.array([65, 255, 255])

    #HSV do amarelo com baixo e alto
    lowerYellow = np.array([10, 70, 180])
    upperYellow = np.array([45, 255, 255])

    #HSV do vermelho com baixo e alto
    lowerRed = np.array([170, 90, 150])
    upperRed = np.array([179, 255, 255])

    #Verifica a posição atual do mouse (x, y)
    posicaoMouseX, posicaoMouseY = pyag.position()

    #Construção das mascara para todas as cores
    maskBlue = cv.inRange(hsv, lowerBlue, upperBlue)
    maskGreen = cv.inRange(hsv, lowerGreen, upperGreen)
    maskYellow = cv.inRange(hsv, lowerYellow, upperYellow)
    maskRed = cv.inRange(hsv, lowerRed, upperRed)

    #Chama a função passando a mascara de uma cor com sua respectiva cor em BGR para o contorno
    contornoCor(maskBlue, (255, 0, 0))
    contornoCor(maskGreen, (0, 255, 0))
    contornoCor(maskYellow, (0, 255, 255))
    contornoCor(maskRed, (0, 0, 255))

    #Exibe a imagem/frame 
    cv.imshow("result", frame)

    #Ao apertar o Esc que é a tecla 27 no teclado fecha o programa
    k = cv.waitKey(60)
    if k == 27:
        break

#Finalizando a conexão com a camera
camera.release()

#Fecha a janela com a imagem aberta
cv.destroyAllWindows()