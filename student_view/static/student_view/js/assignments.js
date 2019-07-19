var EventHandler = document.querySelector(".assignment_list");
EventHandler.addEventListener("click", ViewAssignment, false);

function ViewAssignment(i) {
    if (i.target !== i.currentTarget) {
        var ClickedItem = i.target;
    ClickedItem.assignment_container.assignment.click();
    } 
}