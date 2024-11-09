(async function ()
{
    let code = new URLSearchParams(window.location.search).get("code")
    if (code && code.length > 5)
    {
        document.getElementById("main").innerHTML = `<div class="preloader"><div class="pong-ball"></div></div>`;
        await get("auth/42/callback/?code=" + code);
    }
})();