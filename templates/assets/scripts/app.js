/*
    Javascript file for the statistics page (/p/{name}/ and /p/{name}/{profile})
 */

const profileSelector = document.getElementById('profile-selector')
const playerName = document.getElementById('main-skin-img').alt.toString()

profileSelector.addEventListener('change', () => {
    const currentPage = this.window.location
    console.log(currentPage)
    const nextProfile = profileSelector.value.split(" ")[0].replace(" ", "")

    this.window.location = '/p/' + playerName + '/' + nextProfile
})