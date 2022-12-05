import csv
import time
import nox

# pymunks = [
#     ('4.0.0', ['2.7']),
#     ('5.4.1', ['2.7','3.9']),
#     ('5.5.0', ['2.7','3.9']),
#     ('5.6.0', ['2.7','3.9']),
#     ('6.0.0', ['3.9']),
#     ('6.1.0', ['3.9']),
#     ('6.2.0', ['3.9']),
#     ('6.3.0', ['3.9','3.11']),
#     ('6.4.0', ['3.9','3.11','pypy3.9']),
# ]

pymunks = [
    ('5.4.1', ['3.9']),
    ('5.5.0', ['3.9']),
    ('5.6.0', ['3.9']),
    ('6.0.0', ['3.9']),
    ('6.1.0', ['3.9']),
    ('6.2.0', ['3.9']),
    ('6.3.0', ['3.9']),
    ('6.4.0', ['3.9']),
]

tests = [
    "pymunk-get.py",
    "pymunk-callback.py",
    "pymunk-collision-callback.py"
]

params = []
for (pymunk, pythons) in pymunks:
    for test in tests:
        params.extend( [(python, pymunk, test) for python in pythons])


# docker run --rm -it -v $(pwd):/src thekevjames/nox:latest nox -f src/noxfile.py
# docker run --rm -it -v $(pwd):/src viblo/pymunk-bench:2022.12.01 nox -f src/noxfile.py
result_file = f'results/results-{time.strftime("%Y%m%d-%H%M%S")}.csv'

with open(result_file, 'w', newline='') as csvfile:
    w = csv.writer(csvfile, dialect='unix')
    w.writerow(['Python', 'Pymunk Version', 'Test', 'Runtime (s)'])

def write_result(r):
    with open(result_file, 'a', newline='') as csvfile:
        w = csv.writer(csvfile, dialect='unix')
        w.writerow(r)

@nox.session
@nox.parametrize('python,pymunk,test', params)
def get(session, pymunk,test):
    session.install(f"pymunk=={pymunk}")
    out = session.run("python", test, silent=True)
    running_time_s = out.split('\n')[-2]
    session.log(running_time_s)
    print(running_time_s)
    print(f"python {session.python} pymunk {pymunk} test {test} {float(running_time_s):.2f}")
    write_result([session.python, pymunk, test, round(float(running_time_s),2)])