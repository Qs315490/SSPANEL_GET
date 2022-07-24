const https = require('https');

class SSPANEL {
	url = '';
	token = '';
	vcode = '';
	email = '';
	dy_url = '';

	constructor(url = "52vpn.club", token = "b=3", vcode = "geetest") {
		this.url = url;
		this.token = token;
		this.vcode = vcode;
	}

	random_email() {
		var possible = "0123456789";
		for (var i = 0; i < 10; i++)
			this.email += possible.charAt(Math.floor(Math.random() * possible.length));
	}

	#cookie = '';
	http(path, pushdata = '') {
		// TODO 实现http请求
		const options = {
			hostname: this.url,
			path: path,
			securet: false
		}
		if (pushdata == '') {
			// GET
			options.method = 'GET';
			options.port = 80;
			options.headers = {
				'Cookie': this.#cookie
			}
		} else {
			// POST
			options.method = 'POST';
			options.port = 443;
			options.headers = {
				'Content-Type': 'application/x-www-form-urlencoded',
				'Content-Length': Buffer.byteLength(pushdata),
				'Cookie': this.#cookie
			}
		}
		
		var back_data = '';

		const req = https.request(options, (res) => {
			if (res.statusCode == 200) {
				this.#cookie = res.headers['set-cookie']
			}
			res.on('data', (data) => {
				back_data = data.toString();
			});
		});
		req.on('error', (e) => {
			console.log(e);
		});
		if (pushdata != '') {
			req.write(pushdata);
		}
		req.end();
		return back_data;
	}

	register() {
		if (this.email == '') {
			this.random_email();
		}
		var data = `email=${this.email}%40qs.com&name=zido&passwd=00000000&repasswd=00000000&wechat=${this.email}&imtype=2`;
		switch (this.vcode) {
			case 'geetest':
				data += '&geetest_challenge=d1fe173d08e959397adf34b1d77e88d7f7&geetest_validate=75775555755555e84_555557757550_755555775579b13&geetest_seccode=75775555755555e84_555557757550_755555775579b13|jordan';
				break;
			case '':
			case 'false':
				break;
			default:
				data = Object.assign(data, this.vcode)
				break;
		}
		var info = this.http('/auth/register', data);
		console.log(info);
	}
	login() {
		var data = `email=${this.email}%40qs.com&passwd=00000000&code`;
		var info = this.http('/auth/login', data);
		console.log(info);
	}
	user() {
		var info=this.http('/user/');
	}
}

var sspanel = new SSPANEL();
sspanel.register();
sspanel.login();
sspanel.user();