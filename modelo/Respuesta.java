package modelo;

public class Respuesta {

    private String cuerpo;
    private String fecha;
    private boolean respuestaAceptada;

    public Respuesta(String cuerpo, String fecha) {
        this.cuerpo = cuerpo;
        this.fecha = fecha;
        this.respuestaAceptada = false;
    }
    
    public String getCuerpo() {
        return cuerpo;
    }

    public void setCuerpo(String cuerpo) {
        this.cuerpo = cuerpo;
    }

    public String getFecha() {
        return fecha;
    }

    public void setFecha(String fecha) {
        this.fecha = fecha;
    }

    public boolean isRespuestaAceptada() {
        return respuestaAceptada;
    }

    public void setRespuestaAceptada(boolean respuestaAceptada) {
        this.respuestaAceptada = respuestaAceptada;
    }
    
}
