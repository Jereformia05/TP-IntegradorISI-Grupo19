import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class Pregunta{
    private String titulo;
    private String texto;
    private String fecha;

    public Pregunta(String titulo, String texto, String fecha){
        this.titulo = titulo;
        this.texto = texto;
        this.fecha = LocalDate.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy"));
    }

    public String getTitulo() {
        return titulo;
    }

    public void setTitulo(String titulo) {
        this.titulo = titulo;
    }

    public String getTexto() {
        return texto;
    }

    public void setTexto(String texto) {
        this.texto = texto;
    }

    public String getFecha() {
        return fecha;
    }

    public void setFecha(String fecha) {
        this.fecha = fecha;
    }

    public void mostrarDetalle(){
        System.out.println("=====================================");
        System.out.println("Titulo: " + this.titulo + ".");
        System.out.println("Fecha de publicaion: " + this.fecha);
        System.out.println("Pregunta: \n " + this.texto);
        System.out.println("=====================================");
    }
}