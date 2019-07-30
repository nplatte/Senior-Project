var HandoutList = document.querySelectorAll(".handout_container");
var Handouts = document.querySelectorAll(".handout");

HandoutList.forEach(AssignHandler);

function AssignHandler(item, index, array){
    item.addEventListener("click", function() {
        Handouts[index].click()
    })
}