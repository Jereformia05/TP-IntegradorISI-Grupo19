
package modelo;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.Objects;

public class AgenteSistema extends Autor {

    private LLMStrategy estrategia;

    public AgenteSistema(LLMStrategy estrategia) {
        this.estrategia = Objects.requireNonNull(estrategia);
    }

    // Genera una respuesta utilizando la estrategia configurada.
    @Override
    public Respuesta generarRespuesta(Pregunta p) {

        String contenido = estrategia.generarRespuestaAutomatica(p);

        String fecha = LocalDate.now().format(
            DateTimeFormatter.ofPattern("dd/MM/yyyy")
        );

        return new Respuesta(contenido, fecha);
    }

    // Comprueba si la pregunta tiene el tag #ia-help.
    private boolean tieneTagIAHelp(Pregunta p) {

        for (Tag tag : p.getTags()) {

            String nombreTag = tag.getNombreTag()
                                  .trim()
                                  .toLowerCase();

            if (nombreTag.equals("#ia-help") ||
                nombreTag.equals("ia-help")) {

                return true;
            }
        }

        return false;
    }

    // Procesa la pregunta y genera una respuesta solamente
    // cuando encuentra el tag #ia-help.
    public Respuesta procesarPregunta(Pregunta p) {

        if (tieneTagIAHelp(p)) {
            return generarRespuesta(p);
        }

        return null;
    }

    public void setEstrategia(LLMStrategy estrategia) {
        this.estrategia = Objects.requireNonNull(estrategia);
    }

    public LLMStrategy getEstrategia() {
        return estrategia;
    }
}
