document.addEventListener('DOMContentLoaded', function() {
    let form = document.querySelector("form");
    form.addEventListener('submit', function(event) {
        let name = document.querySelector('#name').value;
        alert('hello, ' + name);
        event.preventDefault();
    });
});
