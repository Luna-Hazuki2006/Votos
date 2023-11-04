const http = require('http')
const fs = require('fs')
const path = require('path')

const puerto = 5000

const server = http.createServer(async (req, res) => {
    if (req.url === '/') {
        const body = path.join(__dirname, '/templates/index.html')
        res.setHeader('Content-Type', 'text/html')
        fs.readFile(body, 'utf-8', (err, contenido) => {
            if (err) {
                res.writeHead(500)
                res.end('No hay un archivo HTML')
            } else {
                res.end(contenido)
            }
        })
    } else if (req.url === '/style.css') {
        const css = path.join(__dirname, '/static/style.css')
        console.log(css);
        fs.readFile(css, 'utf-8', (err, contenido) => {
            if (err) {
                res.writeHead(500)
                res.end('No hay archivo CSS')
            } else {
                res.writeHead(200, {
                    'Content-Type': 'text/css'
                })
                res.end(contenido)
            }
        })
    } else if (req.url === '/index.js') {
        const js = path.join(__dirname, '/static/index.js')
        console.log(js);
        fs.readFile(js, 'utf-8', (err, contenido) => {
            if (err) {
                res.writeHead(500)
                res.end('No hay archivo js')
            } else {
                res.writeHead(200, {
                    'Content-Type': 'text/javascript'
                })
                res.end(contenido)
            }
        })
    }
})

server.listen(puerto, () => {
    console.log(`El servidor se encuentra en el puerto ${puerto}`);
})