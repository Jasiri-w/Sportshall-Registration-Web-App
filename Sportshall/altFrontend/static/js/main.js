window.addEventListener("load", () => {
    document.querySelector("body").classList.add("loaded");
})
window.addEventListener("unload", () => {
    document.querySelector("body").classList.remove("loaded");
    document.querySelector("body").classList.add("unloaded");
})

function goBack() { window.history.back();}