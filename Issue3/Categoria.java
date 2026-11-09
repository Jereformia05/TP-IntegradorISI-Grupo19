package modelo;

public class Categoria {
    private String tipoCategoria;

    public Categoria(String tipoCategoria) {
        this.tipoCategoria = tipoCategoria;
    }

    public String getTipoCategoria() {
        return tipoCategoria;
    }

    public void setTipoCategoria(String tipoCategoria) {
        this.tipoCategoria = tipoCategoria;
    }

    @Override
    public String toString() {
        return "Categoria{" +
                "tipoCategoria ='" + tipoCategoria + '\'' +
                '}';
    }
}