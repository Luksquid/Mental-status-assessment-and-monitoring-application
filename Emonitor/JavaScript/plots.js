function countFilesInDirectory() {
    const files = fs.readdirSync('./plots');
    const fileCount = files.filter(file => fs.statSync(path.join('./plots', file)).isFile()).length;
    return fileCount;
}

function load_images(){

    
    const container = document.getElementById("statisticsMainSide");

    container.innerHTML = '';
    i = 0;
    number_of_files = countFilesInDirectory();
    end = false;

    for(let i = number_of_files-1; i > -1; i--){
        let imgElement = document.createElement("img");
        imgElement.src = './plots/'+String(i)+'.png';
        imgElement.style.width = "800px";
        imgElement.style.height = "430px";
        imgElement.style.marginBottom = "30px";
        container.appendChild(imgElement);
    }
}

document.getElementById("showStatistics").addEventListener("click", function() {
    load_images();
});