//function sets given theme/color-scheme
const setTheme = themeName => {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;
}

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
        return toggleTheme()
    }
})();

//click handler
vanilla_button = document.getElementById('vanilla-button')
feb_button = document.getElementById('feb-button')
jul_button = document.getElementById('jul-button')
oct_button = document.getElementById('oct-button')
dec_button = document.getElementById('dec-button')

vanilla_button.addEventListener('onclick', function(){
    return toggleTheme('theme-vanilla')
})
feb_button.addEventListener('onclick',function(){
    return toggleTheme('theme-valentinesDay')
})
jul_button.addEventListener('onclick', function(){
    return toggleTheme('theme-fourthOfJuly')
})
oct_button.addEventListener('onclick', function(){
    return toggleTheme('theme-halloween')
})
dec_button.addEventListener('onclick', function(){
    return toggleTheme('theme-christmas')
})
