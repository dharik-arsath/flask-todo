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

workspace_btn.addEventListener("click", function () {
    create_workspace();
}
)


// function delete_workspace(workspace_id) {
//     const data = JSON.stringify({
//         workspace_id: workspace_id
//     });

//     (async () => {
//         const rawResponse = await fetch('/delete-todo', {
//             method: 'POST',
//             headers: {
//                 'Accept': 'application/json',
//                 'Content-Type': 'application/json'
//             },
//             body: data
//         });

//         const content = await rawResponse.json();

//         if (content.workspace_id == workspace_id) {
//             document.querySelector("#todo-" + workspace_id.toString()).remove();
//         }
//     })();
// }


// delete_btns.forEach(element => {
//     element.addEventListener("click", e => {
//         const workspace_full_id = element.getAttribute("data-id");
//         let workspace_id;
//         if (workspace_id !== null) {
//             workspace_id = parseInt(workspace_full_id.split("-")[1])
//         }

//         delete_workspace(workspace_id);
//     })

// })