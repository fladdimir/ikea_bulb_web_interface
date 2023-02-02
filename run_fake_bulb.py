import tests.fake_bulb as fb

fb.connect()
fb.client.loop_forever()
