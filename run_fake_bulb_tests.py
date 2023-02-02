import tests.fake_bulb_test as t

# requires running mqtt server
# docker-compose -f tests/docker-compose.yml up

# requires running fake bulb
# python run_fake_bulb.py

t.test()
