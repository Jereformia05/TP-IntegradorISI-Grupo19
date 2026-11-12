package modelo;

public class GeminiStrategy implements LLMStrategy {

    @Override
    public String generarRespuestaAutomatica(Pregunta p) {
        // Acá iría la conexión real con la API de Gemini.
        return "Respuesta generada utilizando Gemini.";
    }
}