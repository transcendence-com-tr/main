var Router = {
    root: '#/',
    routes: [],
    urls: [],
    titles: [],
    funcs: [],
    params: {},
    currentCleanup: null,
    isLoading: false,

    add: function(path, url, title, func) {
        this.routes.push(path);
        this.urls.push(url);
        this.titles.push(title);
        this.funcs.push(func);
    },

    parseParams: function(path) {
        const routeParts = path.split('/');
        const hashParts = location.hash.split('/');
        this.params = {};

        routeParts.forEach((part, index) => {
            if (part.startsWith('<') && part.endsWith('>')) {
                const paramName = part.slice(1, -1);
                this.params[paramName] = hashParts[index].replace('#', '');
            }
        });
    },

    navigate: function() {
        this.params = {};
        var routes = this.routes,
            urls = this.urls,
            funcs = this.funcs,
            root = this.root;

        async function loading() {
            if (Router.isLoading) return;
            Router.isLoading = true;
            var preloader = document.createElement("div");
            try {
                while (document.getElementById("css"))
                    document.head.removeChild(document.getElementById("css"));
                while (document.getElementById("js"))
                    document.body.removeChild(document.getElementById("js"));
                while (document.getElementById("mainJS"))
                    document.getElementById("mainJS").remove();
                clearAllProcesses();

                let routeIndex = -1;
                routes.forEach((route, index) => {
                    const regexRoute = new RegExp("^" + route.replace(/<\w+>/g, "[^/]+") + "$");
                    if (regexRoute.test(location.hash)) {
                        routeIndex = index;
                        Router.parseParams(route);
                    }
                });

                var template = urls[routeIndex];
                var func = funcs[routeIndex];

                if (Router.currentCleanup) {
                    Router.currentCleanup();
                    Router.currentCleanup = null;
                }

                preloader.classList.add("preloader");
                preloader.innerHTML = `<div class="pong-ball"></div>`;
                document.body.prepend(preloader);

                document.getElementById('main').style.display = 'none';

                if (routeIndex === -1) {
                    location.hash = root;
                    template = urls[0];
                }
                template = "pages/" + template;

                let css = document.createElement("link");
                css.rel = "stylesheet";
                css.href = "assets/css/" + template.split(".")[0] + ".css?v=490";
                css.id = "css";
                css.onerror = function() {
                    console.warn('CSS file not found for template:', template);
                };
                document.head.appendChild(css);
                clearAllProcesses();

                let apiURL = template.split(".")[0].replaceAll("pages/", "");
                console.log(apiURL);
                if (apiURL === "chat")
                    apiURL += "/" + Router.params["username"];
                const response = await fetch("api/frontend/" + apiURL, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + localStorage.getItem('token')
                    }
                });

                if (!response.ok) {
                    let responseData = await response.json();
                    if (responseData.redirect)
                        window.location.href = responseData.redirect;
                    throw new Error('Network response was not ok ' + response.statusText);
                }

                var html = await response.text();

                if (func) {
                    const data = await func();
                    Object.entries(data).forEach(([key, value]) => {
                        Object.entries(value).forEach(([key2, value2]) => {
                            html = html.replaceAll("{" + key + "." + key2 + "}", value2);
                        });
                    });
                }

                document.getElementById("main").innerHTML = html;

                const script = document.createElement("script");
                script.id = "js";
                script.src = "assets/js/" + template.split(".")[0] + ".js?v=490";
                script.defer = true;

                script.onload = function() {
                    console.log('JS file loaded successfully:', script.src);
                    if (window.cleanup) {
                        Router.currentCleanup = window.cleanup;
                    }
                };

                script.onerror = function() {
                    console.warn('JS file not found for template:', template);
                };
                document.body.appendChild(script);
            } catch (error) {
                console.error(error);
            } finally {
                if (preloader && preloader.parentNode)
                    document.body.removeChild(preloader);
                clearAllProcesses();
                document.getElementById('main').style.display = 'block';

                const mainScript = document.createElement("script");
                mainScript.id = "mainJS";
                mainScript.src = "assets/js/main.js?v=490";
                mainScript.defer = true;
                mainScript.onload = function() {
                    console.log('JS main file loaded successfully:', mainScript.src);
                };

                mainScript.onerror = function() {
                    console.warn('JS main file not found');
                };
                document.body.appendChild(mainScript);

                Router.isLoading = false;
            }
            Router.isLoading = false;
        }

        window.onload = loading;
        window.onhashchange = loading;
    },

    get: function() {
        return location.hash.slice(2);
    },

    getParameter: function(name) {
        return this.params[name];
    }
};
