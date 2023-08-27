// function revisar() {
//     const forma = document.querySelector('form')
//     const titulo = document.getElementById('titulo')
//     if (localStorage.getItem('usuario')) {
//         titulo.innerText = ''
//     }
// }
const actual = document.getElementById('usuario')

function iniciar_sesion() {
    const forma = document.querySelector('form')

    const data = new FormData(forma)
    const cedula = data.get('cedula')
    const clave = data.get('contraseña')
    const real = JSON.parse(localStorage.getItem(cedula))
    if (real.clave == clave) {
        localStorage.setItem('actual', JSON.stringify(real))
    }
    actual.innerText = 'Usuario: ' + cedula
}

function registrar_usuario() {
    const forma = document.querySelector('form')

    let data = new FormData(forma)
    const cedula = data.get('cedula')
    const nombre = data.get('nombre')
    const clave = data.get('contraseña')
    const repetida = data.get('repetida')
    const correo = data.get('correo')
    console.log(data);
    if (clave != repetida) {
        alert('Las contraseñas no son iguales')
        return
    }
    const usuario = {
        'cedula': cedula, 
        'nombre': nombre, 
        'clave': clave, 
        'correo': correo
    }
    localStorage.setItem(cedula, JSON.stringify(usuario))
    // data = { id: 1345, day: "Tuesday", title: "Economics210" };
    // const jsonData = JSON.stringify(data);
    // const blob = new Blob([jsonData], { type: "application/json" });
    // const url = URL.createObjectURL(blob);
    // const link = document.createElement("a");
    // link.href = url;
    // link.download = "data.json";
    // document.body.appendChild(link);
    // link.click();
    // document.body.removeChild(link);
}