document.addEventListener("DOMContentLoaded", function () {
    let dropArea = document.getElementById("drop-area");
    let fileInput = document.getElementById("fileElem");
    
    // Browse button triggers file input
    document.getElementById("browse-btn").addEventListener("click", function () {
        fileInput.click();
    });

    // Drag & Drop events
    dropArea.addEventListener("dragover", function (e) {
        e.preventDefault();
        dropArea.style.background = "#e3f2fd";
    });

    dropArea.addEventListener("dragleave", function () {
        dropArea.style.background = "white";
    });

    dropArea.addEventListener("drop", function (e) {
        e.preventDefault();
        dropArea.style.background = "white";
        let files = e.dataTransfer.files;
        uploadFiles(files);
    });

    // File input change event
    fileInput.addEventListener("change", function () {
        uploadFiles(fileInput.files);
    });

    function uploadFiles(files) {
        let formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append("file", files[i]);
        }

        fetch("/upload", {
            method: "POST",
            body: formData
        })
        .then(response => response.text())
        .then(result => {
            alert(result);
            location.reload(); // Refresh file list
        })
        .catch(error => console.error("Error:", error));
    }
});
