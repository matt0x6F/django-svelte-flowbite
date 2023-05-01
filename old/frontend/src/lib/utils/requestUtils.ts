import { onDestroy } from 'svelte';
import { browser } from '$app/environment';
import { goto } from '$app/navigation';
import type { Token, UserResponse, User } from '$lib/interfaces/user.interface';
import type { CustomError } from '$lib/interfaces/error.interface';
import { notificationData } from '$lib/store/notificationStore';
import { userData } from '$lib/store/userStore';

import { variables } from '$lib/utils/constants';
import { formatText } from '$lib/formats/formatString';

export const browserGet = (key: string): string | undefined => {
	if (browser) {
		const item = localStorage.getItem(key);
		if (item) {
			return item;
		}
	}
	return undefined;
};

export const browserSet = (key: string, value: string): void => {
	if (browser) {
		localStorage.setItem(key, value);
	}
};

export const getCookie = (name: string): string | undefined => {
	const value: string = `; ${document.cookie}`;
	const parts: string[] = value.split(`; ${name}=`);

	if (parts.length === 2) return parts.pop().split(';').shift();
};

const getSession = async (): Promise<[object, CustomError[]]> => {
	let user: User = {};

	const unsubscribe = userData.subscribe((value) => {
		user = value;
	});

	if (user.tokens?.csrf === undefined) {
		const [token, errors] = await getCSRF();
		if (errors.length > 0) {
			return [{}, errors];
		}

		console.log("Token: " + token);

		userData.set({
			authenticated: false,
			tokens: {
				csrf: token,
			},
		});
	}

    fetch(`${variables.BASE_API_URI}/accounts/session/`, {
      credentials: "same-origin",
    })
    .then((res) => res.json())
    .then(async (data) => {
      console.log(data);
      if (data.isAuthenticated) {
		const [token, errors] = await getCSRF();
		if (errors.length > 0) {
			return [{}, errors];
		}

		userData.set({
			authenticated: true,
			tokens: {
				csrf: token,
			},
		});
      } else {
        const [token, errors] = await getCSRF();
		if (errors.length > 0) {
			return [{}, errors];
		}

		userData.set({
			authenticated: false,
			tokens: {
				csrf: token,
			},
		});
      }
    })
    .catch((err) => {
      console.log(err);
    });

	onDestroy(unsubscribe);
  }
  
const getCSRF = async (): Promise<[string, CustomError[]]> => {
	let csrfToken: string = '';
	let errors: Array<CustomError> = [];

    fetch(`${variables.BASE_API_URI}/accounts/csrf/`, {
      credentials: "same-origin",
    })
    .then((res) => {
      	let token = res.headers.get("X-CSRFToken");
      	
		if (token == null) {
			csrfToken = '';
		} else {
			csrfToken = token
		}
    })
    .catch((error) => {
	  	errors = [{ error: 'An error occurred.' }, { error: `${error} `}];
    });

	return [csrfToken, errors];
  }

export const post = async (
	fetch: any,
	url: string,
	body: unknown
): Promise<[object, CustomError[]]> => {
	let csrfToken = "";
	try {
		try {
			const [token, errors] = await getCSRF();
			console.log("Token: " + token + " Errors: " + JSON.stringify(errors));

			if (errors.length > 0) {
				return [{}, errors];
			} else {
				console.log("Setting CSRF Token: " + token)
				csrfToken = token;
			}
		}
		catch(error) {
			const errors: Array<CustomError> = [{ error: 'An error occurred.' }, { error: `${error} `}];
			return [{}, errors];
		}

		const headers = {'Content-Type': 'application/octet-stream', 'Authorization': '', 'X-CSRFToken': '', 'Access-Control-Allow-Origin': '', 'Access-Control-Allow-Credentials': ''};
		if (!(body instanceof FormData)) {
			headers['Content-Type'] = 'application/json';
			body = JSON.stringify(body);
			const token = browserGet('refreshToken');
			if (token) {
				headers['Authorization'] = `Bearer ${token}`;
			}

			const csrftoken = getCookie('csrftoken');
			if (csrftoken) {
				headers['X-CSRFToken'] = csrftoken;
				headers['Access-Control-Allow-Origin'] = 'http://localhost:81';
				headers['Access-Control-Allow-Credentials'] = 'true';
			}

			// log headers
			console.log("Headers: " + JSON.stringify(headers));

			const res = await fetch(url, {
				method: 'POST',
				body,
				headers,
				credentials: 'same-origin'
			});

			const response = await res.json();
			if (response.errors) {
				const errors: Array<CustomError> = [];
				for (const p in response.errors) {
					errors.push({ error: response.errors[p] });
				}
				return [{}, errors];
			}
			return [response, []];
		}
	} catch (error) {
		const errors: Array<CustomError> = [{ error: 'An error occurred.' }, { error: `${error} `}];
		return [{}, errors];
	}

	const errors: Array<CustomError> = [{ error: 'An unknown error occurred.' }]

	return [{}, errors];
};

export const getCurrentUser = async (
	fetch: any,
	refreshUrl: string,
	userUrl: string
): Promise<[object, Array<CustomError>]> => {
	const jsonRes = await fetch(refreshUrl, {
		method: 'POST',
		mode: 'cors',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			refresh: `${browserGet('refreshToken')}`
		})
	});
	const accessRefresh: Token = await jsonRes.json();
	if (accessRefresh.access) {
		const res = await fetch(userUrl, {
			headers: {
				Authorization: `Bearer ${accessRefresh.access}`
			}
		});
		if (res.status === 400) {
			const data = await res.json();
			const error = data.user.error[0];
			return [{}, error];
		}
		const response = await res.json();
		return [response.user, []];
	} else {
		return [{}, [{ error: 'Refresh token is invalid...' }]];
	}
};

export const logOutUser = async (): Promise<void> => {
	const res = await fetch(`${variables.BASE_API_URI}/token/refresh/`, {
		method: 'POST',
		mode: 'cors',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			refresh: `${browserGet('refreshToken')}`
		})
	});
	const accessRefresh = await res.json();
	const jres = await fetch(`${variables.BASE_API_URI}/accounts/logout/`, {
		method: 'POST',
		mode: 'cors',
		headers: {
			Authorization: `Bearer ${accessRefresh.access}`,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			refresh: `${browserGet('refreshToken')}`
		})
	});
	if (jres.status !== 204) {
		const data = await jres.json();
		const error = data.user.error[0];
		throw { id: error.id, message: error };
	}
	localStorage.removeItem('refreshToken');
	userData.set({});
	notificationData.update(() => 'You have successfully logged out...');
	await goto('/accounts/login');
};

export const handlePostRequestsWithPermissions = async (
	fetch: any,
	targetUrl: string,
	body: unknown,
	method = 'POST'
): Promise<[object, Array<CustomError>]> => {
	const res = await fetch(`${variables.BASE_API_URI}/token/refresh/`, {
		method: 'POST',
		mode: 'cors',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			refresh: `${browserGet('refreshToken')}`
		})
	});
	const accessRefresh = await res.json();
	const jres = await fetch(targetUrl, {
		method: method,
		mode: 'cors',
		headers: {
			Authorization: `Bearer ${accessRefresh.access}`,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify(body)
	});

	if (method === 'PATCH') {
		if (jres.status !== 200) {
			const data = await jres.json();
			console.error(`Data: ${data}`);
			const errs = data.errors;
			console.error(errs);
			return [{}, errs];
		}
		return [await jres.json(), []];
	} else if (method === 'POST') {
		if (jres.status !== 201) {
			const data = await jres.json();
			console.error(`Data: ${data}`);
			const errs = data.errors;
			console.error(errs);
			return [{}, errs];
		}
		return [jres.json(), []];
	}
};

export const UpdateField = async (
	fieldName: string,
	fieldValue: string,
	url: string
): Promise<[object, Array<CustomError>]> => {
	const userObject: UserResponse = { user: {} };
	let formData: UserResponse | any;
	if (url.includes('/user/')) {
		formData = userObject;
		formData['user'][`${fieldName}`] = fieldValue;
	} else {
		formData[`${fieldName}`] = fieldValue;
	}

	const [response, err] = await handlePostRequestsWithPermissions(fetch, url, formData, 'PATCH');
	if (err.length > 0) {
		return [{}, err];
	}
	notificationData.update(() => `${formatText(fieldName)} has been updated successfully.`);
	return [response, []];
};