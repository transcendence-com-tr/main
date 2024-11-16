(async function () {
    event(document, 'submit', function(event) {
        if (event.target.tagName === 'FORM') {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            let action = new URL(form.action).pathname;

            action = action[0] === '/' ? action.substring(1) : action;

            request(form.getAttribute("method"), action, formData);
        }
    });
})();