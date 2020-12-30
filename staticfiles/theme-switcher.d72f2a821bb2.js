let htmltag = document.getElementById('htmltag')


//function sets given theme/color-scheme
const setTheme = themeName => {
    htmltag.setAttribute('class', themeName)
    localStorage.setItem('class', themeName)
}


// var xhttp = new XMLHttpRequest();
// xhttp.onreadystatechange = function() {
//     if (this.readyState == 4 && this.status == 200) {
//
//     }
// }
// function to toggle between themes
const toggleTheme = () => {
    switch (localStorage.getItem('theme')) {
        case 'theme-fourthOfJuly':
            return setTheme('theme-fourthOfJuly');
        case 'theme-christmas':
            return setTheme('theme-christmas');
        case 'theme-valentinesDay':
            return setTheme('theme-valentinesDay');
        case 'theme-halloween':
            return setTheme('theme-halloween');
        default:
            return setTheme('theme-vanilla');
    }

}

//immediately invoked to set theme on ititial load
(function () {
    if (localStorage.getItem('theme') === 'theme-vanilla') {
        return setTheme('theme-vanilla')
    } else {
        return setTheme()
    }
})();

//click handler
let vanilla_button = document.getElementById('vanilla-button')
let feb_button = document.getElementById('feb-button')
let jul_button = document.getElementById('jul-button')
let oct_button = document.getElementById('oct-button')
let dec_button = document.getElementById('dec-button')

vanilla_button.addEventListener('onclick', function(){
    return setTheme('theme-vanilla')
})
feb_button.addEventListener('onclick',function(){
    return setTheme('theme-valentinesDay')
})
jul_button.addEventListener('onclick', function(){
    return setTheme('theme-fourthOfJuly')
})
oct_button.addEventListener('onclick', function(){
    return setTheme('theme-halloween')
})
dec_button.addEventListener('onclick', function(){
    return setTheme('theme-christmas')
})
