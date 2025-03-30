update_state(state, id)
fetch(
    "/update_ticket_status/<id>/<status>");
        
    // FetchRes is the promise to resolve
    // it by using.then() method
    fetchRes.then(res =>res.json()).then(d => {console.log(d)}
)