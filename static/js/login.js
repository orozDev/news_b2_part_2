const loginForm = document.querySelector('#login_form')

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault()
    const form = e.target

    const body = new FormData(form)

    const res = await fetch('/ajax/login/', {
        method: 'POST',
        body,
    })

    if (res.status === 200 || res.status === 400) {
        const data = await res.json()
        if (data.isAuthenticated) {
            window.location.reload()
        } else {
            const messageBlock = document.querySelector('#login_form_message')
            messageBlock.innerHTML = '<i class="fa-solid fa-circle-exclamation"></i> ' + data.message
        }
    } else alert('Network error')

})