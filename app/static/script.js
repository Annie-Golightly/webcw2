

function zoom(){
    var image = document.querySelector('.zoom-image');
    image.classList.add('zoom-in'); //calls the css zoom-in function
};




window.onload = function(){  //when the page loads, it will call the zoom function
    if (window.location.pathname === '/'){
        zoom();
    }
};