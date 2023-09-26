import speech_recognition as sr
from gtts import gTTS
from playsound import playsound
import time

def operaciones(usu_TxtResMenu):
    print('Reconocido: {}'.format(usu_TxtResMenu))
    switch = {
        'suma':'suma()',
        'resta':'resta()',
        'multiplicación':'multiplicacion()',
        'división':'division()',
    }
    if usu_TxtResMenu in switch:
        operacion = switch[usu_TxtResMenu]
        eval(operacion)
        return 1
    else:
        operacionInvalida()
        return 0
    #return switch.get(usu_TxtResMenu, "inv") este metodo se utilizaba con un diccionario comun que llamaba a 'suma'
    #El problema: si se llamaban como 'suma' el dicionario se construia, pero no reproducia nada. Si se llamaba como "suma()" se llamaba con audio pero se reproducian todas. 

#Metodo rustico que iba a usar de ultima opcion xd
def operacionesIf(usu_TxtResMenu):
    print('Reconocido: {}'.format(usu_TxtResMenu))
    if (usu_TxtResMenu == 'suma'):
        suma()
    elif (usu_TxtResMenu == 'resta'):
        resta()
    elif (usu_TxtResMenu == 'multiplicacion'):
        multiplicacion()
    elif (usu_TxtResMenu == 'division'):
        division()
    else:
        operacionInvalida()


def suma():
    sys_AudSuma = gTTS('Suma ha sido seleccionada', lang='es')
    sys_AudSuma.save('sumaSel.mp3')
    playsound('sumaSel.mp3')
    time.sleep(1)
    a,b = pedirNums()
    c = float(a)+float(b)
    #print(c)
    res = str(c)
    sys_AudResSuma = gTTS('El resultado de la suma es:'+res, lang='es')
    sys_AudResSuma.save('resSuma.mp3')
    playsound('resSuma.mp3')
    time.sleep(1)

def resta():
    sys_AudResta = gTTS('Resta ha sido seleccionada', lang='es')
    sys_AudResta.save('restaSel.mp3')
    playsound('restaSel.mp3')
    time.sleep(1)
    a,b = pedirNums()
    c = float(a)-float(b)
    res = str(c)
    sys_AudResResta = gTTS('El resultado de la resta es:'+res, lang='es')
    sys_AudResResta.save('resResta.mp3')
    playsound('resResta.mp3')
    time.sleep(1)


def multiplicacion():
    sys_AudMulti = gTTS('Multiplicación ha sido seleccionada', lang='es')
    sys_AudMulti.save('multiSel.mp3')
    playsound('multiSel.mp3')
    time.sleep(1)
    a,b = pedirNums()
    c = float(a)*float(b)
    res = str(c)
    sys_AudResMul = gTTS('El resultado de la multiplicación es:'+res, lang='es')
    sys_AudResMul.save('resMul.mp3')
    playsound('resMul.mp3')
    time.sleep(1)


def division():
    sys_AudDiv = gTTS('División ha sido seleccionada', lang='es')
    sys_AudDiv.save('divSel.mp3')
    playsound('divSel.mp3')
    time.sleep(1)
    a,b = pedirNums()
    c = float(a)/float(b)
    res = str(c)
    sys_AudResDiv = gTTS('El resultado de la división es:'+res, lang='es')
    sys_AudResDiv.save('resDiv.mp3')
    playsound('resDiv.mp3')
    time.sleep(1)


def operacionInvalida():
    sys_AudInv = gTTS('Lo siento, no he entendido tu respuesta. Selecciona suma, resta, mutliplicacion o division', lang='es')
    sys_AudInv.save('invSel.mp3')
    playsound('invSel.mp3')
    time.sleep(1)


def pedirNums():
    sys_AudSolNum1 = gTTS('Dame el primer numero', lang='es')
    sys_AudSolNum1.save('solNum1.mp3')
    playsound('solNum1.mp3')

    usu_MicNum1 = r.record(source, duration=3)
    usu_TxtNum1 = r.recognize_google(usu_MicNum1, language='es-ES')

    sys_AudSolNum2 = gTTS('Ahora dame el segundo', lang='es')
    sys_AudSolNum2.save('solNum2.mp3')
    playsound('solNum2.mp3')

    usu_MicNum2 = r.record(source, duration=3)
    usu_TxtNum2 = r.recognize_google(usu_MicNum2, language='es-ES') 

    print(usu_TxtNum1)
    print(usu_TxtNum2)

    return usu_TxtNum1, usu_TxtNum2


#Declaramos el reconocedor
r = sr.Recognizer()

#Activar el microfono como recurso que estará permanentemente en escucha (listen). Si quiero control es record()
with sr.Microphone() as source:
    print('Inicia, por favor...')
    #Guardamos lo que ha escuchado el microfono en una variable
    #r.adjust_for_ambient_noise(source) Esta linea es para la supresion de ruido
    usu_MicInicio = r.record(source, duration=4)

    try:
        #Hay que convertir lo que dijimos a texto para que pueda ser procesado
        usu_TxtInicio = r.recognize_google(usu_MicInicio,language='es-ES')
        if usu_TxtInicio == 'calculadora':
            print('Accediendo a la calculadora')
            print('Preguntando: ¿Cual es la operacion que quieres realizar? SUMA, RESTA, MULTIPLICACION O DIVISIÓN?')

            #Convertir la respuesta de texto a audio y lo guardamos
            sys_AudMenu = gTTS('Te escucho, dime, ¿cual es la operacion que desea realizar, suma, resta, multiplicación o división?', lang='es')
            #Reproducimos el archivo mp3
            sys_AudMenu.save('menuCalc.mp3')
            playsound('menuCalc.mp3')

            usu_MicResMenu = r.listen(source)
            usu_TxtResMenu = r.recognize_google(usu_MicResMenu, language='es-ES')
            operaciones(usu_TxtResMenu)

            
        else:
            print('Acceso denegado, tu dijiste: {}'.format(usu_TxtInicio))
    except Exception as e:
        print('Lo siento, no te entendi ni un carajo. '+str(e))