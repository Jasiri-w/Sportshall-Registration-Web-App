window.addEventListener("load", () => {
    document.querySelector("body").classList.add("loaded");
})
window.addEventListener("unload", () => {
    document.querySelector("body").classList.remove("loaded");
    document.querySelector("body").classList.add("unloaded");
})

function goBack() { window.history.back();}

document.querySelector("#back-btn").addEventListener("mouseover", () => {
    document.querySelector("#back-hover-text").style.width = "7rem"; 
})
document.querySelector("#back-btn").addEventListener("mouseout", () => {
    document.querySelector("#back-hover-text").style.width = "0"; 
})