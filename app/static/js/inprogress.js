
const completed_btns = document.querySelectorAll(".complete")
const back_to_available = document.querySelectorAll(".back_to_available")

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


function update_inprogress(data, todo_id) {
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

back_to_available.forEach(element => {
    element.addEventListener("click", e => {
        console.log("click");
        todo_id = get_todo_id(element)

        const data = JSON.stringify({
            todo_id: todo_id,
            "inprogress": false
        });

        update_inprogress(data, todo_id);
    })

})


function update_completed(data, todo_id) {
    (async () => {
        const workspace = get_workspace()
        const POST_ROUTE = "/workspaces/" + workspace + "/update-completed"

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

completed_btns.forEach(element => {
    element.addEventListener("click", () => {
        todo_id = get_todo_id(element)

        const data = JSON.stringify({
            todo_id: todo_id,
            "update-status": true
        });

        update_completed(data, todo_id);
    })

})
