function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    console.log()
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');



document.addEventListener("DOMContentLoaded", function() {
    let btns = document.querySelectorAll(".productContainer button[data-id]");

    btns.forEach(btn => {
        btn.addEventListener("click", addToCart);
    });

    function addToCart(e) {
        let product_id = e.target.dataset.id;
        let url = "/add_to_cart";

        let data = { id: product_id };

        fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json", 'X-CSRFToken': csrftoken },
                body: JSON.stringify(data)
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById("num_of_items").innerHTML = data;
                console.log(data);
            })
            .catch(error => {
                console.log(error);
            });
    }
});


document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("testButton").addEventListener("click", function() {
        alert("This is a test button!");
    });
});
