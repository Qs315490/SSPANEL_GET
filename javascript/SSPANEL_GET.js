process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0;
class SSPANEL {
	url = '';
	token = '';
	vcode = '';
	email = '';
	dy_url = '';

	constructor(url = "5.52vpn.club", token = "b=3", vcode = "geetest") {
		this.url = url;
		this.token = token;
		this.vcode = vcode;
		this.email = this.random_email()
	}

	random_email() {
		let possible = "0123456789";
		let email_num = ''
		for (var i = 0; i < 10; i++)
			email_num += possible.charAt(Math.floor(Math.random() * possible.length));
		return email_num
	}

	cookie = '';
	async http(path, pushdata = '') {
		const options = {
			//securet: false,
			timeout: 15,
			headers: {
				'Cookie': this.cookie
			}
		}
		const url = `https://${this.url}/${path}`;
		if (pushdata == '') {
			// GET
			options.method = 'GET';
		} else {
			// POST
			options.method = 'POST';
			options.headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
			options.body = pushdata;
		}
		let res = await fetch(url, options)
		// console.log(res)
		if (res.status === 200) {
			let raw_cookie = res.headers.get('set-cookie')
			// console.log(raw_cookie)
			if (raw_cookie !== null) {
				const real_cookie = raw_cookie
					.replace(/expires=(.+?);\s/gi, '')
					.replace(/path=\/(,?)(\s?)/gi, '')
					.trim()
				this.cookie += real_cookie
				// console.log(this.cookie)
			}
		}
		return res;
	}

	async register() {
		let data = `email=${this.email}%40qs.com&name=zido&passwd=00000000&repasswd=00000000&wechat=${this.email}&imtype=2`;
		switch (this.vcode) {
			case 'geetest':
				data += '&geetest_challenge=d1fe173d08e959397adf34b1d77e88d7f7&geetest_validate=75775555755555e84_555557757550_755555775579b13&geetest_seccode=75775555755555e84_555557757550_755555775579b13|jordan';
				break;
			case 'false' || '':
				break;
			default:
				data = Object.assign(data, this.vcode)
				break;
		}
		let res = await this.http('auth/register', data);
		// console.log(await res.text());
		let back = await res.json();
		// console.log(back);
		return new Promise((resolve, reject) => {
			if (back.ret === 1) {
				resolve(back);
			} else {
				reject(back);
			}
		});
	}
	async login() {
		let data = `email=${this.email}%40qs.com&passwd=00000000&code`;
		let res = await this.http('auth/login', data);
		let back = await res.json();
		// console.log(back);
		return new Promise((resolve, reject) => {
			if (back.ret === 1) {
				resolve(back);
			} else {
				reject(back);
			}
		});
	}
	async user() {
		let res = await this.http('user');
		return new Promise(async (resolve, reject) => {
			if (res.url !== `https://${this.url}/user`) {
				console.log(res.url)
				reject('登录失败')
			}
			let regex = `https://[\\w./?=&]+${this.token}[\\w=&]*`
			let reg = new RegExp(regex);
			let text = await res.text();
			// console.log(text);
			resolve(reg.exec(text))
		})
	}
}

var sspanel = new SSPANEL();
sspanel.register().then(back => {
	console.log(back)
	return sspanel.login()
}).then(back => {
	console.log(back)
	return sspanel.user()
}).then(str => {
	console.log(str[0])
}).catch((err) => {
	console.log(err)
})