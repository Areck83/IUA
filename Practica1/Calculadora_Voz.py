#Areck83- Issac Glez
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
        sys_Play('Lo siento, no he entendido tu respuesta. Selecciona suma, resta, mutliplicación o división','invSel.mp3')
        return 0
    #return switch.get(usu_TxtResMenu, "inv") este metodo se utilizaba con un diccionario comun que llamaba a 'suma'
    #El problema: si se llamaban como 'suma' el dicionario se construia, pero no reproducia nada. Si se llamaba como "suma()" se llamaba con audio pero se reproducian todas. 

def suma():
    sys_Play('Suma ha sido seleccionada','sumaSel.mp3')
    a,b = pedirNums()
    c = float(a)+float(b)
    res = str(c)
    print(res)
    sys_Play('El resultado de la suma es:'+res, 'resSuma.mp3')

def resta():
    sys_Play('Resta ha sido seleccionada', 'restaSel.mp3')
    a,b = pedirNums()
    c = float(a)-float(b)
    res = str(c)
    print(res)
    sys_Play('El resultado de la resta es:'+res,'resResta.mp3')

def multiplicacion():
    sys_Play('Multiplicación ha sido seleccionada','multiSel.mp3')
    a,b = pedirNums()
    c = float(a)*float(b)
    res = str(c)
    print(res)
    sys_Play('El resultado de la multiplicación es:'+res,'resMul.mp3')

def division():
    sys_Play('División ha sido seleccionada','divSel.mp3' )
    a,b = pedirNums()
    c = float(a)/float(b)
    res = str(c)
    print(res)
    sys_Play('El resultado de la división es:'+res,'resDiv.mp3')

def pedirNums():

    sys_Play('Dame el primer numero','solNum1.mp3')
    
    usu_MicNum1 = r.record(source, duration=3)
    usu_TxtNum1 = r.recognize_google(usu_MicNum1, language='es-ES')
    print(usu_TxtNum1)

    #while (not validadorNum(usu_TxtNum1)):
    #    usu_MicNum1 = r.record(source, duration=3)
    #    usu_TxtNum1 = r.recognize_google(usu_MicNum1, language='es-ES')
    #Ciclo no usable porque se guardaria el mismo sonido en cada error, validacion simple en su lugar

    validadorNum(usu_TxtNum1)

    sys_Play('Ahora dame el segundo','solNum2.mp3')
    usu_MicNum2 = r.record(source, duration=3)
    usu_TxtNum2 = r.recognize_google(usu_MicNum2, language='es-ES') 
    print(usu_TxtNum2)

    validadorNum(usu_TxtNum2)

    return usu_TxtNum1, usu_TxtNum2

def sys_Play(sys_Aud,nombre_Archivo):
    sys_AudUniversal = gTTS(sys_Aud, lang='es')
    sys_AudUniversal.save(nombre_Archivo)
    playsound(nombre_Archivo)
    time.sleep(1)

def validadorNum(usu_Num):
    try:
        check = int(usu_Num)
        return True
    except:
        print('no fue un numero')
        sys_Play('Según yo eso no es un número, no podré procesarlo despué','errorNums.mp3')
        return False

#Declaramos el reconocedor
r = sr.Recognizer()

#Activar el microfono como recurso que estará permanentemente en escucha (listen). Si quiero control es record()
with sr.Microphone() as source:
    print('Inicia, por favor...')

    #r.adjust_for_ambient_noise(source) Esta linea es para la supresion de ruido
    usu_MicInicio = r.record(source, duration=4)

    try:
        #Hay que convertir lo que dijimos a texto para que pueda ser procesado
        usu_TxtInicio = r.recognize_google(usu_MicInicio,language='es-ES')
        if usu_TxtInicio == 'calculadora':
            print('Accediendo a la calculadora')
            print('Preguntando: ¿Cual es la operacion que quieres realizar? SUMA, RESTA, MULTIPLICACION O DIVISIÓN?')

            #Convertir la respuesta de texto a audio y lo guardamos
            sys_Play('Te escucho, dime, ¿cual es la operacion que desea realizar, suma, resta, multiplicación o división?', 'menuCalc.mp3')

            usu_MicResMenu = r.listen(source)
            usu_TxtResMenu = r.recognize_google(usu_MicResMenu, language='es-ES')
            operaciones(usu_TxtResMenu)

            
        else:
            print('Acceso denegado, tu dijiste: {}'.format(usu_TxtInicio))
    except Exception as e:
        print('Lo siento, no te entendi ni un carajo. '+str(e))