# switchmate

## HTTP API

### Endpoints

**show switch VLANs**<br>
GET `http://localhost/show-vlan`<br>

**show switch interfaces status**<br>
GET `http://localhostlocal/show-interfaces-status`<br>

**show google spreadsheet switch config**<br>
GET `http://localhost/show-google-config?spreadsheet_key={{ google spreadsheet key }}`<br>

**push google spreadsheet switch config to switch**<br>
GET `http://localhost/configure-switch-with-google-spreadsheet?spreadsheet_key={{ google spreadsheet key }}`<br>

**push port config(s) to switch**<br>
POST `http://localhost/configure-port`<br>

Request

```json
[
	{
		"port": "1/0/1",
		"name": "port description",
		"vlan": "70",
		"mode": "access"
	},
	{
		"port": "1/0/2",
		"name": "port description",
		"vlan": "71",
		"mode": "trunk"
	}
]
```

**write memory**<br>
GET `http://localhost/write-mem`<br>