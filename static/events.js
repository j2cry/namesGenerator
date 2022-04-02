let socket = io({path: serviceURL + '/socket.io'});

window.addEventListener('load', () => {
    document.getElementById('generateBtn').onclick = () => {
        const resultBody = document.getElementById('resultBody');
        socket.emit('generate', collectData(), (response) => {
            resultBody.innerHTML = '';
            response.forEach((obj) => {
                console.log(obj)
                let row = document.createElement('tr')
                row.append(createColumnElement(obj['surname']));
                row.append(createColumnElement(obj['name']));
                row.append(createColumnElement(obj['midname']));
                row.append(createColumnElement(obj['birthday']));
                resultBody.append(row);
            });
        });
    }
})

function collectData() {
    const ln = document.getElementById('nameLetters').value;
    const lm = document.getElementById('midnameLetters').value;
    const ag = document.getElementById('ages').value;
    const sn = document.getElementById('surname').getAttribute('checked');
    const gd = document.getElementById('gender').value;
    return {'ln': ln, 'lm': lm, 'ag': ag, 'sn': sn, 'gd': gd}
}

function createColumnElement(value) {
    let col = document.createElement('td')
    col.innerText = value;
    return col
}