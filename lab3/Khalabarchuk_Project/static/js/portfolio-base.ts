
const PAGE_URI = window.document.baseURI;

const navPages = document.getElementById("navPages")

let list = navPages.querySelectorAll("a")
list.forEach(link => {
    if (link.href === PAGE_URI){
        link.classList.add("selected")
    }
})
