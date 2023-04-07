function openTab(el){
    console.log("Open Tab")
    contentTabs = document.querySelectorAll(".tab-content");
    tabs = document.querySelectorAll(".tab");
    for(var x = 0; x < contentTabs.length; x++){
        contentTabs[x].classList.remove("active");
    }
    for(var x = 0; x < tabs.length; x++){
        tabs[x].classList.remove("active");
    }

    query = ".tab-content[name = '" + el.getAttribute("name") + "']";
    document.querySelector(query).classList.add("active");

    el.classList.add("active");
}

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

function exportTableToExcel(tableID, filename = ''){
    var downloadLink;
    var dataType = 'application/vnd.ms-excel';
    var tableSelect = document.getElementById(tableID);
    var tableHTML = tableSelect.outerHTML.replace(/ /g, '%20');
    
    // Specify file name
    filename = filename?filename+'.xls':'excel_data.xls';
    
    // Create download link element
    downloadLink = document.createElement("a");
    
    document.body.appendChild(downloadLink);
    
    if(navigator.msSaveOrOpenBlob){
        var blob = new Blob(['\ufeff', tableHTML], {
            type: dataType
        });
        navigator.msSaveOrOpenBlob( blob, filename);
    }else{
        // Create a link to the file
        downloadLink.href = 'data:' + dataType + ', ' + tableHTML;
    
        // Setting the file name
        downloadLink.download = filename;
        
        //triggering the function
        downloadLink.click();
    }
}