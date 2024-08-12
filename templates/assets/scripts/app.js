/*
    Javascript file for the statistics page (/p/{name}/ and /p/{name}/{profile})
 */


// Handle the profile selector update
const profileSelector = document.getElementById("profile-selector")
const playerName = document.getElementById("main-skin-img").alt.toString()

profileSelector.addEventListener("change", () => {
    const currentPage = this.window.location
    console.log(currentPage)
    const nextProfile = profileSelector.value.split(" ")[0].replace(" ", "")

    this.window.location = "/p/" + playerName + "/" + nextProfile
})


// Set the color for the Trophy fish rarities
const rarityColor = {
    "Bronze": "var(--§c)",
    "Silver": "var(--§7)",
    "Gold": "var(--§6)",
    "Diamond": "var(--§b)",
}
document.querySelectorAll(".trophy-count p strong").forEach(element => {
    element.style.color = rarityColor[element.innerHTML.toString()]
})