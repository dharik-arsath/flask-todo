var workspace_btn = document.querySelector("#submit");
// const delete_btns = document.querySelectorAll(".delete");

function create_workspace() {
    const modal = document.querySelector(".modal");

    const title = document.querySelector("#title").value.trim();
    const desc = document.querySelector("#desc").value.trim();
    var error_field = document.querySelector(".error");

    if (title.length == 0) {
        const msg = "Title must be present..."
        error_field.textContent = msg;
        return;
    }

    let data = new FormData()
    data.append("title", title);
    data.append("desc", desc);


    (async () => {
        const rawResponse = await fetch('/create-workspace', {
            method: 'POST',
            body: data
        });

        const content = await rawResponse.json();
        if (content.status == 200) {
            modal.classList.remove("show");
            modal.classList.add("hide");

            var backdrop = document.getElementsByClassName('modal-backdrop')[0];
            backdrop.parentNode.removeChild(backdrop);

            location.reload();
        }
    })();
}

workspace_btn.addEventListener("click", create_workspace);