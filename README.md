# TP-IntegradorISI-Grupo19

INTEGRANTES

1)
-Nombres : Jeremias Nahuel
-Apellido : Formia

2)
-Nombre : Agustin Osvaldo
-Apellido : Bruno Rodriguez

3)
-Nombre : Juan Ignacio
-Apellido : Furlan Rodriguez

4)
-Nombre : Santino
-Apellido : Calvo

5)
-Nombre : Santino
-Apellido : Roccia Belgoff

Justificación de los Patrones de Diseño

1. Patrón Strategy (Modelos de IA)
 El proposito de incluir el Patron Strategy es permitir que el AgenteSistema delegue la generación de respuestas a distintos modelos de IA sin quedar atado a un proveedor específico.

Lo usamos para encapsular cada integrador o proveedor (OpenAI, Gemini, ModelosLocales) detrás de la interfaz LLMStrategy. Esto facilita cambiar de modelo en tiempo de ejecución o sumar nuevos en el futuro sin tocar la lógica interna del agente.

2. Modelado de Usuarios y Agentes (Herencia Directa)
   Optamos por una estructura de herencia simple donde Usuario y AgenteSistema extienden directamente de Autor. Ya que el proyecto no requiere manejar abstracciones complejas o fábricas dinámicas para la creación de actores, esta solución directa resuelve la autoría de las publicaciones de forma limpia, reduciendo la complejidad innecesaria en el código.
