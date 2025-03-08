// {% load static %}

const inputBox = document.getElementById("input-box");
const listContainer = document.getElementById("list-container");

function addTask()
{
    alert(inputBox.value);
    // const tasks = loadData();
    if(inputBox.value === '')
    {
        alert("You must write something!");
    }
    else{

        
        console.log(listContainer.childNodes[0].innerHTML);
        
        // 
        // document.querySelectorAll("#list-container li")[0].innerText.split("\n")[0]

        var ls = document.querySelectorAll("#list-container li")
        for(let i=0;i<ls.length;i++)
        {
            var temp=ls[i].innerText.split("\n")[0];
            if(temp === inputBox.value)
            {
                alert("Already Exist!");
                inputBox.value = "";
                return;
            }
        }
        let li = document.createElement("li");
        li.innerHTML = inputBox.value;
        listContainer.appendChild(li);
        let span = document.createElement("span");
        span.innerHTML = "\u00d7";
        li.appendChild(span);
    }
    inputBox.value = "";
    saveData();
}

listContainer.addEventListener("click",function(e)
{
    if(e.target.tagName === "LI")
    {
        e.target.classList.toggle("checked");
        saveData();
    }
    else if(e.target.tagName  === "SPAN")
    {
        e.target.parentElement.remove();
        saveData();
    }
},false);

function saveData()
{
    localStorage.setItem("data", listContainer.innerHTML);
}

function showTask()
{
    listContainer.innerHTML = localStorage.getItem("data");
}
showTask();

// var index = boardTitlesList.findIndex((item) => {
//     return item.boardTitle === SEARCHED_TITLE
// });

// if (index === -1) {
//     /* NOT FOUND */
// } else {
//     /* FOUND */
// }