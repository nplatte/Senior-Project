const FakeButton = document.querySelector(".class_button")
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