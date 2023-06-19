const filter_div = document.querySelector("#filter");


function filter_data(priority){
    const data = JSON.stringify({
        priority: priority
    });

    (async () => {

        const workspace = get_workspace()

        const ROUTE = "/workspaces/" + workspace + "/list-available-todo" + `?priority=${priority}`;
        console.log(ROUTE);

        document.location = ROUTE;
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

