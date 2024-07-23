/*
    Javascript file for the "/info" page
 */

// Toggling the license display
const licenseContainer = document.getElementById("license-container")
const licenseToggleDiv = document.getElementById("license-toggle-container")
const licenseToggleState = document.getElementById("license-toggle-text")

licenseToggleDiv.addEventListener("click", () => {
    let state = licenseToggleState.textContent;
    if (state === "[OFF]") {
        licenseToggleDiv.getElementsByClassName("toggle-icon")[0].src = "/images/Redstone_Lamp_On.webp"
        licenseToggleState.textContent = "[ON]"
        licenseToggleState.style.color = "#00be00"

        licenseContainer.style.visibility = "visible"
    } else {
        licenseToggleDiv.getElementsByClassName("toggle-icon")[0].src = "/images/Redstone_Lamp_Off.webp"
        licenseToggleState.textContent = "[OFF]"
        licenseToggleState.style.color = "#be0000"

        licenseContainer.style.visibility = "hidden"
    }
})