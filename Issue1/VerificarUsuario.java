package servicio;

import modelo.Usuario;

public class VerificarUsuario {

    /*
     * Valida si las credenciales ingresadas coinciden con el usuario registrado.
     * Corresponde al metodo + verificarUsuario(u : Usuario) : boolean de su UML.
     */
    public boolean verificarUsuario(Usuario u, String correoIngresado, String contraseñaIngresada) {
        if (u == null || correoIngresado == null || contraseñaIngresada == null) {
            return false;
        }

        // Hacemos el hash de la contraseña ingresada para comparar
        String hashIngresado = Integer.toHexString(contraseñaIngresada.hashCode());

        // Comprobamos coincidencia de email y contraseña
        boolean emailCorrecto = u.getCorreoElectronico().equalsIgnoreCase(correoIngresado);
        boolean claveCorrecta = u.getContraseña().equals(hashIngresado);

        return emailCorrecto && claveCorrecta;
    }
}