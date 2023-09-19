const apiUrl = 'http://localhost:5000/api/v1';

function login() {
    const email = document.querySelector('#login .input-box input[type="text"]').value;
    const password = document.querySelector('#login .input-box input[type="password"]').value;

    const loginData = {
        email: email,
        password: password
    };
    console.log(loginData);

    fetch(`${apiUrl}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
    })
        .then((response) => {
            console.log(response.status);
            if (!response.ok) {
                throw Error('Network response was not okay');
            }
            return response.json();
        })
        .then((data) => {
            console.log(data);
        })
        .catch((error) => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

function register() {
	const email = document.querySelector('#register .input-box input[type="text"]').value;
	const password = document.querySelector('#register .input-box input[type="password"]').value;

	const registerData = {
		email: email,
		password: password
	};

	fetch(`${apiUrl}/auth/register`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(registerData)
	})
		.then((response) => {
			console.log(response.status);
			if (!response.ok) {
				throw Error('Network response was not okay');
			}
			return response.json();
		})
		.then((data) => {
			console.log(data);
		})
		.catch((error) => {
			console.error('There has been a problem with your fetch operation:', error);
		});
}
