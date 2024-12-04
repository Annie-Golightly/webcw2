function loadData(){ 

    var gearItem = document.getElementById("dropdown").value; //this gets the type the user selected
    let allCards = document.querySelectorAll(".card-group");  //gets all of the card groups

    for (var x=0;x<allCards.length;x++){  //iterates through each card group
    let type = allCards[x].getAttribute('data-val'); //get the type of the current card group

    //if the given group has the same type as selected or selected is all, show, if not hide
    if (type == gearItem || gearItem=="all"){
        console.log(type);
        allCards[x].style.display= "flex"; 
    }
    else{
        allCards[x].style.display = "none";
    }
    }
} 

function loadUserData(){ 

    var memberItem = document.getElementById("dropdown").value; //this gets the user to show
    let allCards = document.querySelectorAll(".card-group");
    for (var x=0;x<allCards.length;x++){  //iterates through each card group
    let type = allCards[x].getAttribute('data-val'); //get the user for the current card group
    
    if (type == memberItem || memberItem=="all"){
        console.log(type);
        allCards[x].style.display= "flex"; 
    }
    else{
        allCards[x].style.display = "none";
    }
    }
} 