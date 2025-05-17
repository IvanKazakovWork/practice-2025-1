document.addEventListener('DOMContentLoaded', function () {
	// Active navigation link highlighter
	const currentLocation = window.location.pathname.split('/').pop()
	const navLinks = document.querySelectorAll('nav ul li a')

	navLinks.forEach(link => {
		const linkPage = link.getAttribute('href').split('/').pop()
		if (
			linkPage === currentLocation ||
			(currentLocation === '' && linkPage === 'index.html')
		) {
			// Remove active class from all links first
			navLinks.forEach(l => l.classList.remove('active'))
			// Add active class to the current page link
			link.classList.add('active')
		}
	})

	console.log('МеталлМастер Платформа JS инициализирован.')
})
