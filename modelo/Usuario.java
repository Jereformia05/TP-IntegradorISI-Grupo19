package modelo;

public class Usuario extends Autor {
    private String correoElectronico;
    private String contraseña;
    private TUsuario usuario; // Rol del usuario

    // Constructor para registrar un nuevo usuario
    public Usuario(String correoElectronico, String contraseña, TUsuario usuario) {
        this.correoElectronico = correoElectronico; // Guardamos la contraseña encriptada (hashing) por seguridad
        this.contraseña = encriptarContraseña(contraseña);
        this.usuario = usuario;
    }

    // Metodo privado para no guardar la contraseña en texto plano
    private String encriptarContraseña(String pass) {
        // En un proyecto real se usa BCrypt o SHA-256
        return Integer.toHexString(pass.hashCode());
    }

    public String getCorreoElectronico(){
        return correoElectronico;
    }

    public String getContraseña(){
        return contraseña;
    }

    public TUsuario getUsuario(){
        return usuario;
    }

    
    public Pregunta generarPregunta(String titulo, String texto, Categoria categoria ){
        //Creo la pregunta con sus parametros agrgandole la fecha automaticamente
        Pregunta nuevaPregunta = new Pregunta(titulo, texto, categoria);
        return nuevaPregunta;
    }

    @Override 
    public Respuesta generarRespuesta(Pregunta p) {
    
        String fechaActual = java.time.LocalDate.now().toString();
        
        String cuerpoRespuesta = "Respuesta generada por el usuario para la pregunta: " + p.getTitulo();
        
        Respuesta nuevaRespuesta = new Respuesta(cuerpoRespuesta, fechaActual);
        return nuevaRespuesta;
    }

    public void setEstadoRespuestaAceptada(Respuesta r) {
        r.setRespuestaAceptada(true);
    }
}