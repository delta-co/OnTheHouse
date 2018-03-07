function apply_ingredient_autosuggest(element)
{
    console.log("Test");
    var autosuggest_div = document.createElement("div");
    autosuggest_div.classList.add("ingredient-autosuggest-list");
    autosuggest_div.classList.add("hidden");
    //autosuggest_div.innerText = "HO HO HO";
    element.__autosuggest_div = autosuggest_div;
    function hide_div(){
        //console.log("hiding autosuggest");
        autosuggest_div.classList.add("hidden");
    };
    function show_div(){
        //console.log("showing autosuggest");
        var cont_rect = element.parentElement.getBoundingClientRect();
        var elem_rect = element.getBoundingClientRect();
        //console.log(cont_rect);
        //console.log(elem_rect);
        autosuggest_div.style.top = elem_rect.bottom - cont_rect.top;
        autosuggest_div.style.left = elem_rect.left - cont_rect.left;
        autosuggest_div.classList.remove("hidden");
    };
    function update_suggestions()
    {
        var value = element.value;
        value = value.split(/,/g);
        value = value[value.length - 1];
        value = value.trim();
        value = value.toLocaleLowerCase();

        var suggestions = [];
        if (value !== "")
        {
            for (var index = 0; index < ALL_INGREDIENTS.length; index += 1)
            {
                var ingredient = ALL_INGREDIENTS[index];
                if (ingredient.toLocaleLowerCase().indexOf(value) != -1)
                {
                    suggestions.push(ingredient);
                }
            }
        }
        if (suggestions.length > 0)
        {
            autosuggest_div.innerHTML = suggestions.join("<br>");
            show_div();
        }
        else
        {
            hide_div();
        }
    }
    element.addEventListener("focus", update_suggestions);
    element.addEventListener("blur", hide_div);
    element.addEventListener("keyup", update_suggestions);
    element.parentElement.appendChild(autosuggest_div);
}

function bind_enter(box, button)
{
    var hook = function(event)
    {
        if (event.key === "Enter")
        {
            button.click();
        }
    }
    box.addEventListener("keyup", hook);
}

function get(url, callback)
{
    var request = new XMLHttpRequest();
    request.onreadystatechange = function()
    {
        if (request.readyState == 4)
        {
            if (callback != null)
            {
                var text = request.responseText;
                var response = JSON.parse(text);
                response["_request_url"] = url;
                response["_status"] = request.status;
                callback(response);
            }
        }
    };
    var asynchronous = true;
    request.open("GET", url, asynchronous);
    request.send();
}

function post(url, data, callback)
{
    var request = new XMLHttpRequest();
    request.onreadystatechange = function()
    {
        if (request.readyState == 4)
        {
            if (callback != null)
            {
                var text = request.responseText;
                var response = JSON.parse(text);
                response["_request_url"] = url;
                response["_status"] = request.status;
                callback(response);
            }
        }
    };
    var asynchronous = true;
    request.open("POST", url, asynchronous);
    request.send(data);
}
