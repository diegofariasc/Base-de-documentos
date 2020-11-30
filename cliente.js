const URLservidor = "http://127.0.0.1:8080"

/* 
El metodo permite extraer las palabras claves especificadas
por el usuario desde la interfaz
Input:  undefined
Output: string   
*/
const obtenerPalabrasClave = () => {

    // Ver que visualizacion esta activa y devolver el texto
    if ( document.getElementById("principal").hidden )
        return document.getElementById("campoBusquedaSecundario").value
    else
        return document.getElementById("campoBusquedaPrincipal").value

} // End obtenerPalabrasClave


/*
El metodo permite cambiar a la vista secundaria
Input:  undefined
Output: undefined  
*/
const cambiarVistaSecundaria = () => {

    document.getElementById("principal").hidden = true
    document.getElementById("secundario").hidden = false
    document.getElementById("campoBusquedaSecundario").value = document.getElementById("campoBusquedaPrincipal").value

} // End obtenerPalabrasClave


/* 
El metodo permite enviar un objeto con alguna peticion
al servidor
Input:  objeto (JS)
Output: objeto JSON    
*/
const enviarSolicitud = async ( object ) => {

    const response = await fetch( URLservidor, {
        method: "POST",
        body: JSON.stringify( object ),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    }) // End fetch
    const json = await response.json();
    return json;

} // End enviarSolicitud


/* 
El metodo permite efectuar una consulta
Input:  resultados (list) con los resultados a ofrecer
Output: undefined  
*/
const construirVistaSecundaria = ( resultados, tiempo ) => {

    // Acceder al div contenedor y limpiarlo
    let contenedor = document.getElementById("contenedor")
    while (contenedor.firstChild) {
        contenedor.removeChild(contenedor.lastChild);
    } // End while

    contenedor.innerHTML += 
    `<label class="nombre" style="color: #3f3f3f; font-size: 15px; font-weight: normal; margin-left: 20px;">${resultados.length} resultados en ${tiempo.toFixed(3)} segundos</label>`

    // Reflejar visualmente cada resultado obtenido
    for (let i = 0; i < resultados.length; i++){

        let resultado = document.createElement('div');
        let marginTop = ( i === 0 ? 10 : 20 )
        resultado.innerHTML = 
        `<div style=" margin-left: 20px; margin-top: ${marginTop}px;">` +
        `<a href="${resultados[i][8]}"><label id="nombre" class="nombre" style="color: #2f5597; font-size: 20px; font-weight: normal; vertical-align: middle; cursor: pointer;"><u>${resultados[i][0]}</u></label><br></a>` +
        `<label id="nombre" class="nombre" style="color: #3f3f3f; font-size: 15px; font-weight: normal; vertical-align: middle;">${resultados[i][1]}</label><br>` +
        `<label id="nombre" class="nombre" style="color: #7c7c7c; font-size: 15px; margin-top: 5px; vertical-align: middle; text-align: left; width: 90%;">${resultados[i][2]}</label><br>` +
        `<label id="nombre" class="nombre" style="color: #0e5f20; font-size: 13px; margin-top: 5px; vertical-align: middle;">Editorial: ${resultados[i][4]}</label>` +
        `<label id="nombre" class="nombre" style="color: #0e5f20; font-size: 13px; margin-top: 5px; margin-left: 10px; vertical-align: middle;">Fecha: ${resultados[i][3]}</label>` +
        `<label id="nombre" class="nombre" style="color: #0e5f20; font-size: 13px; margin-top: 5px; margin-left: 10px; vertical-align: middle;">Lugar: ${resultados[i][5]}</label>` +
        `<label id="nombre" class="nombre" style="color: #0e5f20; font-size: 13px; margin-top: 5px; margin-left: 10px; vertical-align: middle;">Revista: ${resultados[i][6]}</label>` +
        `<label id="nombre" class="nombre" style="color: #0e5f20; font-size: 13px; margin-top: 5px; margin-left: 10px; vertical-align: middle;">ISSN / ISBN: ${resultados[i][7]}</label>` +
        `</div>`

        contenedor.appendChild( resultado )

    } // End for

} // End construirVistaSecundaria


/* 
El metodo permite efectuar una consulta
Input:  undefined
Output: undefined  
*/
const buscar = async () => {

    let consulta =
    {
        palabras    : obtenerPalabrasClave(),
        separacion  : document.getElementById("campoSeparaciones").value,
        resultados  : parseInt(document.getElementById("resultados").value),
        usarFreqT   : document.getElementById("matrizFrecuencias").checked,
        proximidad  : document.getElementById("proximidad").value,
    } // End consulta

    // Obtener resultado
    let respuesta = await enviarSolicitud( consulta )
    let resultados = respuesta["resultados"]
    let tiempo = respuesta["tiempo"]

    // Construir y cambiar a la vista secundaria
    construirVistaSecundaria( resultados, tiempo )
    if ( document.getElementById("secundario").hidden )
        cambiarVistaSecundaria()


} // End buscar


/* 
El metodo permite abrir el menu de herramientas avanzadas 
Input:  undefined
Output: undefined  
*/
const desplegarOpcionesAvanzadas = () => {

    document.getElementById("busquedaAvanzada").hidden = false
    document.getElementById("contenedor").style.marginTop = "140px"

} // End desplegarOpcionesAvanzadas

/* 
El metodo permite ocultar el menu de herramientas avanzadas 
Input:  undefined
Output: undefined  
*/
const ocultarOpcionesAvanzadas = () => {

    document.getElementById("busquedaAvanzada").hidden = true
    document.getElementById("contenedor").style.marginTop = "90px"

} // End desplegarOpcionesAvanzadas

