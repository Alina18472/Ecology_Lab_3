// facksChecker.js
const status = sessionStorage.getItem("status")
const element = document.getElementById("faks-image")

if (status !== "Выполнено") {
    element.style.visibility = "hidden"
}
else {
    element.style.visibility = "visible"
}
