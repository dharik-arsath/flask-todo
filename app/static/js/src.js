var submit_btn = document.querySelector("#submit");
const delete_btns = document.querySelectorAll(".delete");
const inprogress_btns = document.querySelectorAll(".inprogress")

const del_workspace_btn = document.querySelector(".delete_workspace_btn")
const edit_btn = document.querySelectorAll(".edit")


function get_workspace() {
    const url = window.location;
    const workspace = url.toString().split("/")[4]

    return workspace
}


function get_todo_id(element) {
    const todo_full_id = element.getAttribute("data-id");
    let todo_id;
    if (todo_id !== null) {
        todo_id = parseInt(todo_full_id.split("-")[1])
    }

    return todo_id;
}

function delete_workspace() {
    const workspace = get_workspace()

    let data = new FormData()
    data.append("workspace", workspace);


    (async () => {
        const POST_ROUTE = "/delete-workspace"
        const rawResponse = await fetch(POST_ROUTE, {
            method: 'POST',
            body: data
        });

        const content = await rawResponse.json();

        if (content.status == 200) {
            window.location = "/workspaces/";
        }
    })();
}

del_workspace_btn.addEventListener("click", delete_workspace)


function create_todo() {
    const modal = document.querySelector(".modal");

    const title = document.querySelector("#title").value.trim();
    const desc = document.querySelector("#desc").value.trim();
    const priority = document.querySelector("#priority").value;
    var error_field = document.querySelector(".error");

    if (title.length == 0) {
        const msg = "Title must be present..."
        error_field.textContent = msg;
        return;
    }

    let data = new FormData()
    data.append("title", title);
    data.append("desc", desc);
    data.append("priority", priority);

    (async () => {
        const workspace = get_workspace()

        const POST_ROUTE = "/workspaces/" + workspace + "/create-todo";

        const rawResponse = await fetch(POST_ROUTE, {
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

submit_btn.addEventListener("click", create_todo);


function delete_todo(todo_id) {
    const data = JSON.stringify({
        todo_id: todo_id
    });

    (async () => {
        const workspace = get_workspace()
        const POST_ROUTE = "/workspaces/" + workspace + "/delete-todo"
        const rawResponse = await fetch(POST_ROUTE, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: data
        });

        const content = await rawResponse.json();

        if (content.todo_id == todo_id) {
            document.querySelector("#todo-" + todo_id.toString()).remove();
        }
    })();
}


delete_btns.forEach(element => {
    element.addEventListener("click", () => {
        todo_id = get_todo_id(element)
        delete_todo(todo_id);
    })

})


function update_inprogress(todo_id) {
    const data = JSON.stringify({
        todo_id: todo_id,
        "inprogress" : true
    });

    (async () => {
        const workspace = get_workspace()
        const POST_ROUTE = "/workspaces/" + workspace + "/update-inprogress"
        const rawResponse = await fetch(POST_ROUTE, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: data
        });

        const content = await rawResponse.json();

        if (content.todo_id == todo_id) {
            document.querySelector("#todo-" + todo_id.toString()).remove();
        }
    })();
}

inprogress_btns.forEach(element => {
    element.addEventListener("click", e => {
        const todo_id = get_todo_id(element);

        console.log("calling in progerss.")
        update_inprogress(todo_id);
    })

})


function edit_todo(todo_id, element) {

    const card = element.closest('.card-body');

    // Get the title and description elements within the card
    const prev_title = card.querySelector('.title').textContent;
    const prev_desc = card.querySelector('.description').textContent;

    const modal = document.querySelector(".modal");

    document.querySelector("#title").value = prev_title;
    document.querySelector("#desc").value = prev_desc;

    submit_btn.removeEventListener("click", create_todo);

    submit_btn.addEventListener("click", () => {

        var title = document.querySelector("#title").value.trim();
        var desc = document.querySelector("#desc").value.trim();
        var error_field = document.querySelector(".error");

        if (title.length == 0) {
            const msg = "Title must be present..."
            error_field.textContent = msg;
            return;
        }

        let data = new FormData()
        data.append("title", title);
        data.append("desc", desc);
        data.append("todo-id", todo_id);

        (async () => {
            const workspace = get_workspace()

            const POST_ROUTE = "/workspaces/" + workspace + "/update-todo";

            const rawResponse = await fetch(POST_ROUTE, {
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

        title.value = "";
        desc.value = "";
    })
}



edit_btn.forEach(element => {
    element.addEventListener("click", e => {
        const todo_full_id = element.getAttribute("data-id");
        let todo_id;
        if (todo_id !== null) {
            todo_id = parseInt(todo_full_id.split("-")[1])
        }

        edit_todo(todo_id, element);
    })

})