var submit_btn = document.querySelector("#submit");
const delete_btns = document.querySelectorAll(".delete");
const completed_btns = document.querySelectorAll(".complete")
const incomplete_btns = document.querySelectorAll(".incomplete")
const del_workspace_btn = document.querySelector(".delete_workspace_btn")


function get_workspace(){
    const url       = window.location;
    const workspace = url.toString().split("/")[4]
    
    return workspace
}



function delete_workspace(){
    const workspace  = get_workspace()

    let data = new FormData()
    data.append("workspace", workspace);


    (async () => {
        const POST_ROUTE = "/delete-workspace"  
        const rawResponse = await fetch(POST_ROUTE, {
          method: 'POST',
          body: data
        });

        const content = await rawResponse.json();

        if(content.status == 200){
            window.location = "/workspaces/";
        }
        })();
    }

    del_workspace_btn.addEventListener("click", e => {
        delete_workspace();  
    })

    function create_todo(){
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
        const workspace = get_workspace() 

        const POST_ROUTE  = "/workspaces/" + workspace + "/create-todo";

        const rawResponse = await fetch(POST_ROUTE, {
          method: 'POST',
          body: data
        });

        const content = await rawResponse.json();
        if(content.status == 200){
            modal.classList.remove("show");
            modal.classList.add("hide");
            
            var backdrop = document.getElementsByClassName('modal-backdrop')[0];
            backdrop.parentNode.removeChild(backdrop);

            location.reload();
        }
    })();
}

submit_btn.addEventListener("click", function () {
        create_todo();    
    }
)    


function delete_todo(todo_id){
    const data    = JSON.stringify({
        todo_id : todo_id
    });

    (async () => {
        const workspace  = get_workspace()
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
        
        if(content.todo_id == todo_id){
            document.querySelector("#todo-"+todo_id.toString()).remove();
        }
      })();
}


delete_btns.forEach(element => {
    element.addEventListener("click", e => {
        const todo_full_id = element.getAttribute("data-id");
        let todo_id;
        if(todo_id !== null){
            todo_id = parseInt(todo_full_id.split("-")[1])
        }

        delete_todo(todo_id);
    })

})





function complete_todo(todo_id){
    const data    = JSON.stringify({
        todo_id : todo_id
    });

    (async () => {
        const workspace = get_workspace()
        const POST_ROUTE = "/workspaces/" + workspace + "/completed" 
        const rawResponse = await fetch(POST_ROUTE, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: data
        });

        const content = await rawResponse.json();
        
        if(content.todo_id == todo_id){
            document.querySelector("#todo-"+todo_id.toString()).remove();
        }
      })();
}

completed_btns.forEach(element => {
    element.addEventListener("click", e => {
        const todo_full_id = element.getAttribute("data-id");
        let todo_id;
        if(todo_id !== null){
            todo_id = parseInt( todo_full_id.split("-")[1] )
        }

        complete_todo(todo_id);
    })

})



function incomplete_todo(todo_id){
    const data    = JSON.stringify({
        todo_id : todo_id
    });

    (async () => {
        const workspace   = get_workspace()
        const POST_ROUTE  = "/workspaces/" + workspace + "/incompleted"

        const rawResponse = await fetch(POST_ROUTE, {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          body: data
        });

        const content = await rawResponse.json();
        
        if(content.todo_id == todo_id){
            document.querySelector("#todo-"+todo_id.toString()).remove();
        }
      })();
}

incomplete_btns.forEach(element => {
    element.addEventListener("click", e => {
        const todo_full_id = element.getAttribute("data-id");
        let todo_id;
        if(todo_id !== null){
            todo_id = parseInt( todo_full_id.split("-")[1] )
        }

        incomplete_todo(todo_id);
    })

})


// // Get all navbar links
// var navbarLinks = document.querySelectorAll('.navbar-nav .nav-link');

// // Add event listener to each link
// navbarLinks.forEach(function(link) {
//   link.addEventListener('click', function(event) {
//     // Remove active class from all links
//     navbarLinks.forEach(function(link) {
//       link.classList.remove('active');
//     });

//     // Add active class to the clicked link
//     this.classList.add('active');
//   });
// });

