// Show live date and time in footer
function updateDateTime() {
    const now = new Date();
    document.getElementById("datetime").innerText = now.toLocaleString();
}
setInterval(updateDateTime, 1000);
updateDateTime();
