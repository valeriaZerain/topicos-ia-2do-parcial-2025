# 2do Parcial - Topicos IA: Despliegue de Agentes IA

En este parcial exploraremos una aplicación de depliegue de un agente IA para el análisis y consulta de una 
base de datos relacional.

### Descripción de la aplicación
El repositorio contiene el código fuente necesario para implementar un agente IA que es capaz de
explorar y ejecutar consultas SQL en una base de datos relacional implementada con sqlite. 

El objetivo del agente es el de ofrecer una interfaz en lenguaje natural para realizar consultas sobre
una base de datos relacional. 

El usuario realizará una consulta al agente y el mismo deberá convertir la pregunta en lenguaje natural
a una consulta en el lenguaje SQL. Esta consulta se mandará a la DB a través de una herramienta que ejecuta
consultas en la DB. El agente interpreta los resultados y responde al usuario. 

El agente también es capaz de analizar errores y corregir llamadas para obtener la mejor respuesta posible al 
usuario. Esto es posible gracias al patrón ReAct del Agente IA.

La interfaz del Agente es una API REST implementada con el framework FastAPI. Esta API cuenta con dos
formas de interactuar con el agente, una síncrona y una asíncrona:

 - Endpoint Síncrono: Este endpoint invoca el agente y espera el resultado antes de devolver una respuesta al usuario. Por tanto, una llamada a este endpoint puede resultar en una espera de varios segundos. El cliente debe esperar el resultado y mantener una conexión abierta con el servidor.
 - Endpoints Asíncronos: Se componen por un par de endpoints, uno para enviar la consulta y ejecutarla en 2do plano y otra para obtener el estado de la consulta, y si la consulta ha terminado obtener los resultados. De esta manera, el cliente podrá enviar una tarea y consultar su estado de forma asíncrona, sin necesidad de esperar o bloquear la ejecución por una solicitud no terminada.


## 1. Instrucciones
Para completar la evaluación parcial, usted deberá implementar lo siguiente:
### 1.1. Completar la implementación del agente
La lógica del agente está definida en el archivo `agent.py`. En él, usted
encontrará la definición del signature, la definición del agente usando un `dspy.Module`, 
y la función de inicialización del agente. Las descripciones o prompts para el agente y las herramientas deberán ser implementadas.
#### 1.1.1. Prompt del Signature del agente
En primer lugar, el prompt del agente deberá ser completado en el docstring
del signature en la clase `SQLAgentSignature`. Usted deberá agregar una descripción detallada
de las tareas del agente, las herramientas con las que cuenta y las reglas o limitaciones de su funcionamiento.

#### 1.1.2. Descripciones de las herramientas
Por su parte, también deberá implementar los prompts o descripciones de las herramientas. Estas descripciones
se encuentran incompletas como el parámetro `desc` al momento de instanciar 
un objeto `dspy.Tool`. Esto lo podrá encontrar en la función `create_agent`.

Complete las descripciones correspondientes con las herramientas, también detalle las entradas y salidas de las mismas.

### 1.2. Implementar Herramienta de guardar reportes
Para la segunda parte, usted deberá implementar la herramienta `save_csv_tool`. La lógica para esta herramienta
reside en el archivo `tools.py`, en la función `save_data_to_csv`. La función deberá recibir los resultados de las 
consultas que el usuario hace y guardarlas en un archivo con formato csv. 

La herramienta tiene las siguientes características:
 - los datos de entrada deben ser una lista de listas o lista de tuplas de python. Estos datos se almacenarán de forma tabular en un archivo .csv
 - Se espeficica el archivo de salida con el argumento `filename`
 - La función deberá tomar en cuenta los posibles errores que el agente pueda cometer al invocarla, es decir, la función no deberá fallar. Las posibles excepciones deben ser atendidas dentro de la función para no detener ni terminar todo el programa.
 - La función deberá retornar una cadena de texto con la descripción de la operación realizada. 
 - Si la operación fue exitosa deberá indicar el directorio del archivo guardado.
 - Si la operación tuvo un error o excepción también deberá indicar el error en la cadena de retorno.
