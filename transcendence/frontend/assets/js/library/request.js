let apiURL =  window.location.origin + "/api";
let token = localStorage.getItem("token") ?? "";

function request(method, action, formData = null) {
    let data = null;
    if (formData) {
        // If formData is an instance of FormData, keep it as-is for file uploads
        if (formData instanceof FormData) {
            data = formData;
        } else {
            // Convert form data to JSON if it's not a FormData object
            data = {};
            for (const [key, value] of formData.entries()) {
                data[key] = value;
            }
            data = JSON.stringify(data);
        }
    }

    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method, apiURL + "/" + action, true);
        xhr.setRequestHeader('Authorization', 'Bearer ' + token);

        // Only set 'Content-Type' if the data is not a FormData object
        if (!(formData instanceof FormData)) {
            xhr.setRequestHeader('Content-Type', 'application/json');
        }

        xhr.onload = function () {
            let response = JSON.parse(xhr.responseText);
            if (response.payload && response.payload.token) {
                token = response.payload.token;
                localStorage.setItem("token", token);
            }
            if (response.message_view) {
                notification(response.state, response.title, response.message);
            }
            if (response.redirect) {
                if (response.redirect.startsWith("#"))
                {
                    let currentPath = window.location.origin + "/" + window.location.hash;
                    if (response.redirect === "#/reload")
                    {
                        window.location.href = currentPath + "/reload";
                        window.location.href = currentPath;
                    }
                    else
                        window.location.href = window.location.origin + "/" + response.redirect;
                }
                else
                    window.location.href = response.redirect;
            }

            var paras = document.getElementsByClassName('errors');
            while (paras[0]) {
                paras[0].parentNode.removeChild(paras[0]);
            }

            for (const field in response.error) {
                if (response.error.hasOwnProperty(field)) {
                    const errorMessages = response.error[field];
                    for (const errorType in errorMessages) {
                        if (errorMessages.hasOwnProperty(errorType)) {
                            document.getElementsByName(field)[0].parentNode.insertAdjacentHTML("beforebegin",
                                `<small class="errors text-color-red d-flex" style="font-size: 12px;">${errorMessages[errorType]}</small>`);
                        }
                    }
                }
            }
            resolve(response);
        };

        xhr.onerror = function () {
            console.error('Request failed');
            reject(new Error('Request failed'));
        };

        if (method !== "GET" && method !== "HEAD") {
            xhr.send(data);
        } else {
            xhr.send();
        }
    });
}

async function post(action, data = null)
{
    return request("POST", action, data);
}

async function get(action, data = null)
{
    return request("GET", action, data);
}

async function put(action, data = null)
{
    return request("PUT", action, data);
}

async function del(action, data = null)
{
    return request("DELETE", action, data);
}

async function frontend(action, callback)
{
    return await fetch(apiURL + "/frontend/" + action, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
    }}).then(response => response.text()).then(callback);
}