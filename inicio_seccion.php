<?php
session_start();

// Conexión a la base de datos
$conn = new mysqli('localhost', 'usuario', 'contraseña', 'base_de_datos');

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Consulta para verificar las credenciales
    $sql = "SELECT * FROM usuarios WHERE username = '$username' AND password = '$password'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $_SESSION['username'] = $username;
        header("Location: index.html"); // Redirige a la página principal después del login
    } else {
        echo "Usuario o contraseña incorrectos.";
    }
}

$conn->close();
?>
