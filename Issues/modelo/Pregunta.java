package modelo;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class Pregunta {
    private String titulo;
    private String texto;
    private String fecha;
    private Categoria categoria;   // Vinculación 1 a 1 obligatoria
    private List<Tag> tags;        // Vinculación 1 a N

    // Constructor que exige la categoría obligatoria
    public Pregunta(String titulo, String texto, Categoria categoria) {
        if (categoria == null) {
            throw new IllegalArgumentException("La pregunta debe tener obligatoriamente una categoría.");
        }
        this.titulo = titulo;
        this.texto = texto;
        this.categoria = categoria;
        this.fecha = LocalDate.now().format(DateTimeFormatter.ofPattern("dd/MM/yyyy"));
        this.tags = new ArrayList<>();
    }

    // Método para agregar tags evitando repetidos
    public void agregarTag(Tag tag) {
        if (tag != null && !this.tags.contains(tag)) {
            this.tags.add(tag);
        }
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

    public Categoria getCategoria() {
        return categoria;
    }

    public void setCategoria(Categoria categoria) {
        if (categoria == null) {
            throw new IllegalArgumentException("La categoría no puede ser nula.");
        }
        this.categoria = categoria;
    }

    public List<Tag> getTags() {
        return tags;
    }

    public void mostrarDetalle() {
        System.out.println("=====================================");
        System.out.println("Titulo: " + this.titulo);
        System.out.println("Fecha de publicacion: " + this.fecha);
        System.out.println("Categoria: " + this.categoria.getTipoCategoria());
        
        System.out.print("Tags: ");
        if (this.tags.isEmpty()) {
            System.out.println("Sin tags.");
        } else {
            List<String> nombresTags = new ArrayList<>();
            for (Tag t : this.tags) {
                nombresTags.add(t.getNombreTag());
            }
            System.out.println(String.join(", ", nombresTags));
        }

        System.out.println("Pregunta:\n" + this.texto);
        System.out.println("=====================================");
    }
}