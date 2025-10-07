document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); 

        const username = form.querySelector('input[type="text"]').value.trim();
        const password = form.querySelector('input[type="password"]').value.trim();

        
        if (!username || !password) {
            alert("Por favor, completa todos los campos.");
            return;
        }

        if (username === "admin" && password === "1234") {
            alert("Inicio de sesión exitoso");
            window.location.href = "crud/index.html";
        } else {
            alert("Usuario o contraseña incorrectos ❌");
        }
    });
});
