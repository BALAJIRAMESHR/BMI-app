window.onload = function() {
    var box = document.querySelector('.scrollable-box');
    if (box) {
        box.scrollTop = box.scrollHeight;
    }
}
