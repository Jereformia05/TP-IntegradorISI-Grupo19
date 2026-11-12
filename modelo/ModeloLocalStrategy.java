package modelo;

public class ModeloLocalStrategy implements LLMStrategy {

    @Override
    public String generarRespuestaAutomatica(Pregunta p) {
        // Acá iría la conexión con el modelo de IA local.
        return "Respuesta generada utilizando un modelo local.";
    }
}