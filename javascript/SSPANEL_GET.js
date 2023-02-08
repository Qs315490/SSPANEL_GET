
class SSPANEL {
	url = '';
	token = '';
	vcode = '';
	email = '';
	dy_url = '';

	constructor(url = "2.52vpn.club", token = "b=3", vcode = "geetest") {
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
	async http(path, pushdata = '') {
		// TODO 实现http请求
		const options = {
			//securet: false,
			timeout: 15
		}
		const url = `https://${this.url}/${path}`;
		if (pushdata == '') {
			// GET
			options.method = 'GET';
			options.headers = {
				'Cookie': this.#cookie
			};
			await fetch(url,options).then(data => data.text()).then(data => {

			}).catch(err => {
				console.error(err);
			})
		} else {
			// POST
			options.method = 'POST';
			options.headers = {
				'Cookie': this.#cookie
			};
			options.form = pushdata;
			await fetch(url, options).then(res => {
				if (res.status == 200) {
					this.#cookie = res.headers.cookie;
				}
				return res.text()
			}).then(data => {

			}).catch(err => {
				console.error(err);
			})
		}
		// TODO: 未知错误
	}

	register() {
		if (this.email == '') {
			this.random_email();
		}
		var data = {
			email: `${this.email}@qs.com`,
			name: 'zido',
			passwd: '00000000',
			repasswd: '00000000',
			wechat: `${this.email}`,
			imtype: 2
		}
		switch (this.vcode) {
			case 'geetest':
				//data += '&geetest_challenge=d1fe173d08e959397adf34b1d77e88d7f7&geetest_validate=75775555755555e84_555557757550_755555775579b13&geetest_seccode=75775555755555e84_555557757550_755555775579b13|jordan';
				data = Object.assign(data, {
					geetest_challenge: 'd1fe173d08e959397adf34b1d77e88d7f7',
					geetest_validate: '75775555755555e84_555557757550_755555775579b13',
					geetest_seccode: '75775555755555e84_555557757550_755555775579b13|jordan'
				});
				break;
			case 'false' || '':
				break;
			default:
				data = Object.assign(data, this.vcode)
				break;
		}
		var info = this.http('auth/register', data);
		console.log(info);
	}
	login() {
		//var data = `email=${this.email}%40qs.com&passwd=00000000&code`;
		let data = {
			email: `${this.email}@qs.com`,
			passwd: '00000000',
			code
		}
		var info = this.http('auth/login', data);
		console.log(info);
	}
	user() {
		var info = this.http('user');
		let reg = new RegExp(`https://[\\w./?=&]+${this.token}[\\w=&]*`);
		return reg.exec(info);
	}
}

var sspanel = new SSPANEL();
sspanel.register();
sspanel.login();
var str = sspanel.user();
console.log(str);