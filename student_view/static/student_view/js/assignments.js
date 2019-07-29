var AssignmentList = document.querySelectorAll(".assignment_container");
var Assignments = document.querySelectorAll(".assignment");

AssignmentList.forEach(AssignHandler);

function AssignHandler(item, index, array){
    item.addEventListener("click", function() {
        Assignments[index].click()
    })
}


const FakeButton = document.querySelector(".assignment_button")
const RealButton = document.querySelector(".hidden_button")

FakeButton.addEventListener("click", function(){
    RealButton.click()
})


const FileText = document.querySelector("#custom_text")

RealButton.addEventListener("change", function(){
    if (RealButton.value){
        var filename = RealButton.value.replace(/^.*[\\\/]/, '')
        FileText.innerHTML = filename;
    } else {
        FileText.innerHTML = "Empty";
    }
})