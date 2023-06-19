const filter_div = document.querySelector("#filter");


function filter_data(priority){
    const data = JSON.stringify({
        priority: priority
    });

    (async () => {
        window.addEventListener('popstate', function(event) {
            console.log("popping...")
            if (event.state !== null) {
                history.replaceState(null, null, '/workspaces/');
                // Additional logic to handle the home page navigation
              }
          });
          
        const workspace = get_workspace()

        // const ROUTE = "/workspaces/" + workspace + "/list-available-todo" + `?priority=${priority}`;
        const ROUTE = window.location.pathname + `?priority=${priority}`;
        console.log(ROUTE);
        
        document.location = ROUTE;
        history.pushState(null, null, ROUTE);
        // const rawResponse = await fetch(ROUTE, {
        //     method: 'GET',
        // });
        
        // const content = await rawResponse.text();

    
        // document.querySelector(".container").innerHTML = content;
        // console.log(content);
    })();
}

function handleFilter(e){
    const isButton = e.target.nodeName;

    if (!isButton) {
        return;
      }
    
    const button_id = e.target.id;
    var filter_type;
    if (button_id == "low"){
        filter_type = "low";
    }
    else if(button_id == "normal"){
        filter_type = "normal";
    }
    else if(button_id == "high"){
        filter_type = "high";
    }
    else{
        filter_type = "default";
    }

    filter_data(filter_type);
}


filter_div.addEventListener('click', handleFilter);

