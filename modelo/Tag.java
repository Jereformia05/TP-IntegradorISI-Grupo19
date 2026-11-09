package modelo;

public class Tag {
    private int idTag;
    private String nombreTag;

    public Tag(int idTag, String nombreTag) {
        this.idTag = idTag;
        this.nombreTag = nombreTag;
    }

    public int getIdTag() {
        return idTag;
    }

    public void setIdTag(int idTag) {
        this.idTag = idTag;
    }

    public String getNombreTag() {
        return nombreTag;
    }

    public void setNombreTag(String nombreTag) {
        this.nombreTag = nombreTag;
    }

    @Override
    public String toString() {
        return "Tag{" +
                "idTag =" + idTag +
                ", nombreTag ='" + nombreTag + '\'' +
                '}';
    }
}