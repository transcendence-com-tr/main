let intervals = [];
let timeouts = [];
let events = [];
function interval(func, timeout, autoClear = true)
{
    let _interval = setInterval(func, timeout);
    if (autoClear) {
        intervals.push({
            "interval": _interval,
        });
    }
}

function timeout(func, timeout, autoClear = true)
{
    let _timeout = setTimeout(func, timeout);
    if (autoClear)
    {
        timeouts.push({
            "timeout": _timeout,
        });
    }
}

function event(element, _event, func, autoClear = true) {
    element.addEventListener(_event, func);
    if (autoClear) {
        events.push({
            "event": _event,
            "element": element,
            "callback": func
        });
    }
}

function clearIntervals()
{
    intervals.forEach(interval => {
        clearInterval(interval.interval);
    });
    intervals = [];
}

function clearTimeouts()
{
    timeouts.forEach(timeout => {
        clearTimeout(timeout.timeout);
    });
    timeouts = [];
}

function clearEvents() {
    events.forEach(event => {
        event.element.removeEventListener(event.event, event.callback);
    });
    events = [];
}


function clearAllProcesses()
{
    clearIntervals();
    clearTimeouts();
    clearEvents();
}

function notification(state, title, message, closeable = true)
{
    document.getElementById('alertModalLabel').textContent = title;
    document.getElementById('alertModalMessage').innerHTML = message;
    document.getElementById("alertModal").classList.add("show");
    document.getElementById("main").style.opacity = "0.2";
    document.getElementById("alertModal").style.zIndex = "9999";
    document.getElementsByClassName("modal-footer")[0].style.display = closeable ? "block" : "none";
}

function notificationTemplate(title, template, data = null)
{
    template = "pages/modals/" + template + ".html?v=460";
    document.getElementById('alertModalLabel').textContent = title;
    fetch(template).then(response => response.text()).then(item => {
        if (data)
        {
            Object.entries(data).forEach(([key, value]) => {
                item = item.replaceAll("{" + key + "}", value);
            });
        }
        document.getElementById('alertModalMessage').innerHTML = item;
    });
    document.getElementById("alertModal").classList.add("show");
    document.getElementById("main").style.opacity = "0.2";
    document.getElementById("alertModal").style.zIndex = "9999";
    document.getElementsByClassName("modal-footer")[0].style.display = "none";
}

function closeModal()
{
    document.getElementById("alertModal").classList.remove("show");
    document.getElementById("main").style.opacity = "1";
    document.getElementById("alertModal").style.zIndex = "-1";
}