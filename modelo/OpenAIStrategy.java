package modelo;

public class OpenAIStrategy implements LLMStrategy {

    @Override
    public String generarRespuestaAutomatica(Pregunta p) {
        // Acá iría la conexión real con la API de OpenAI.
        return "Respuesta generada utilizando OpenAI.";
    }
}