
const PAGE_URI = window.document.baseURI;

const navPages = document.getElementById("navPages")

let list = navPages.querySelectorAll("a")
list.forEach(link => {
    if (link.href === PAGE_URI){
        link.classList.add("selected")
    }
})

const local_time = document.getElementById("local_time")

local_time.innerText = new Date().toLocaleTimeString()
setInterval(() => {
    local_time.innerText = new Date().toLocaleTimeString()
}, 1000)
