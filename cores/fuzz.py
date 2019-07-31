"""
submit():
	response = submit(url, payload)
	for modules in import_module:
		modules.check(response, payload)

for payload in payloads
	threading.run(submit(payload, options))

"""


def get_method(url, params, fuzz_params, payloads, threads = 16):
	def run_threads(threads):
		# TODO progress bar
		# Run threads
		for thread in threads:
			thread.start()
		
		# Wait for threads completed
		for thread in threads:
			thread.join()
			
	def send(url, params, fuzz_params, payload):
		try:
			import mechanicalsoup
			# TODO add proxy
			browser = mechanicalsoup.StatefulBrowser()
			send_payload = {k: "%s" % (payload) if k == fuzz_param else params[k] for k in params.keys()}
			resp = browser.open(url, params = send_payload)
			resp = str(resp.text)
		except UnicodeEncodeError:
			resp = str(resp.text.encode('utf-8'))
		except Exception:
			resp = ""
		finally:
			browser.close()
		
		# TODO check HTTP code
		import importlib, cores
		from modules import ActiveScan
		modules = cores.load_modules(ActiveScan)
		for module in modules:
			module = importlib.import_module('modules.%s' % (module))
			module = module.Check()
			
			# Re-generate payload and signature. Work for XSS
			module.payload = payload
			module.signatures = module.signature()

			module.check(url, send_payload[fuzz_params], resp, fuzz_params)
		
		
	try:
		params = {k: v for k, v in params.items() if v}  # TODO check here
		workers = []
		import threading
		for fuzz_param in fuzz_params:
			for payload in payloads:
				# Fill thread pool, run them all
				if len(workers) == threads:
					run_threads(workers)
					del workers[:]
				worker = threading.Thread(
					target = send,
					args = (url, params, fuzz_param, payload)
				)
				worker.daemon = True
				workers.append(worker)
		
		# Run all last threads
		run_threads(workers)
		del workers[:]
						
	except Exception as error:
		from cores import events
		events.error(error, "Fuzz GET")