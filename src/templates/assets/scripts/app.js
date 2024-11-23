/*
    Javascript file for the statistics page (/p/{name} and /p/{name}/{profile})
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


// Set the color for the Trophy fish rarities and Jacob medals
const rarityColor = {
    "Bronze": "var(--§c)",
    "Silver": "var(--§7)",
    "Gold": "var(--§6)",
    "Diamond": "var(--§b)",
    "Platinum": "var(--§3)"
}

document.querySelectorAll(".trophy-count p strong").forEach(element => {
    element.style.color = rarityColor[element.innerHTML.toString()]
})

document.querySelectorAll(".medal-title > p").forEach(element => {
    element.style.color = rarityColor[element.innerHTML.toString()]
})


// Rabbit rarity repartition bar
const rabbitBarContainer = document.getElementById("rabbit-repartition-bar")

if (rabbitBarContainer != null) {
    const totalRabbit = Number(rabbitBarContainer.attributes.getNamedItem("rabbit-count").value.replace(",", ""))

    function computeRabbitBar() {
        const rabbitBarWidth = rabbitBarContainer.clientWidth;

        let barOffset = 0

        rabbitBarContainer.querySelectorAll("div").forEach((rabbitDiv) => {
            const rabbitCount = Number(rabbitDiv.attributes.getNamedItem("rabbit-count").value.replace(",", ""))
            if (rabbitCount > 0) {
                const part = ((rabbitCount/totalRabbit) * rabbitBarWidth); // get occupied size in px

                rabbitDiv.style.width = `${(rabbitBarWidth - barOffset)}px`
                barOffset += part
            }
        })
    }

    computeRabbitBar()
    window.addEventListener("resize", computeRabbitBar)
}

// Script for the detailed rabbit collection dashboard
const dashboardBtn = document.getElementById("rabbit-dashboard-btn")
const rabbitRarities = ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC", "DIVINE"]
const displayFoundBtn = document.getElementById("found-rabbit")
const displayNotFoundBtn = document.getElementById("not-found-rabbit")


function updateRabbitDisplay() {
    for (let i = 0; i < rabbitRarities.length; i++) {
        const tickBox = document.querySelector("input[value=" + rabbitRarities[i] + "]")
        const rabbitsDiv = document.getElementsByClassName(rabbitRarities[i] + "-rabbit-div")[0]

        if (!tickBox.checked) {
            rabbitsDiv.style.display = "none"
        } else {
            rabbitsDiv.style.display = "block"
        }
    }

    const displayFound = displayFoundBtn.checked
    const displayNotFound = displayNotFoundBtn.checked
    const rabbitDivList = document.querySelectorAll("div.rabbit-div")

    // Should display rabbit that have been found at least once
    if (displayFound) {
        rabbitDivList.forEach((element) => {
            if (element.attributes.found.value > 0) {
                element.style.display = "inline-flex"
            }
        })
    } else {
        rabbitDivList.forEach((element) => {
            if (element.attributes.found.value > 0) {
                element.style.display = "none"
            }
        })
    }

    // Should display rabbit that haven't been found yet
    if (displayNotFound) {
        rabbitDivList.forEach((element) => {
            if (element.attributes.found.value.toString() === "0") {
                element.style.display = "inline-flex"
            }
        })
    } else {
        rabbitDivList.forEach((element) => {
            if (element.attributes.found.value.toString() === "0") {
                element.style.display = "none"
            }
        })
    }
}

dashboardBtn.addEventListener("click", updateRabbitDisplay)
document.addEventListener("DOMContentLoaded", updateRabbitDisplay)