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

function imaginar() {
    let esto = document.getElementById("tipo");
    let div = document.getElementById('visuales')
    let valor = esto.value;
    // let texto = esto.options[esto.selectedIndex].text;
    if (valor == 'candidato') {
        div.style.display = 'block'
    } else {
        div.style.display = 'none'
    }
}

function mostrar_imagen() {
    let input = document.getElementById("imagen");
    let fReader = new FileReader();
    fReader.readAsDataURL(input.files[0]);
    fReader.onloadend = function(event) {
        let img = document.getElementById("textual");
        img.value = event.target.result;
        img = document.getElementById('vistas')
        img.src = event.target.result
        console.log(event.target.result);
        return event.target.result
    }
}

function deimaginar() {
    let imagen = document.getElementById('imagen')
    let externa = document.getElementById('vistas')
    let vistas = document.getElementById('textual')
    imagen.value = ''
    externa.src = ''
    vistas.value = ''
}