function wrapper(){
    console.log(`Helllo ${document.location}`);
    btnEdit = document.querySelector("#btn-edit");

    btnEdit.addEventListener('click', e => {
        document.location = "./python";
    })
}

window.addEventListener("DOMContentLoaded", wrapper);