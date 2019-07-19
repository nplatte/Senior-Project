var AssignmentList = document.querySelectorAll(".assignment_container");
var Assignments = document.querySelectorAll(".assignment");

AssignmentList.forEach(AssignHandler);

function AssignHandler(item, index, array){
    item.addEventListener("click", function() {
        Assignments[index].click()
    })
}