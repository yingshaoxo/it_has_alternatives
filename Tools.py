#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
#!/usr/bin/env /usr/bin/python3
from auto_everything.base import Python, Terminal
from auto_everything.develop import YRPC


py = Python()
t = Terminal()
yrpc = YRPC()


class Tools():
    def push(self, comment: str):
        t.run('git add .')
        t.run('git commit -m "{}"'.format(comment))
        t.run('git push origin')

    def pull(self):
        t.run("""
git fetch --all
git reset --hard origin/master
""")

    def generate_protocol_files(self):
        yrpc.generate_code(
            which_language="typescript",
            input_folder="./protocols",
            input_files=["it_has_alternatives.proto"],
            output_folder="./front_end/src/generated_yrpc"
        )

        yrpc.generate_code(
            which_language="python",
            input_folder="./protocols",
            input_files=["it_has_alternatives.proto"],
            output_folder="./backend_service/backend_service/generated_yrpc"
        )

    def run(self):
        pass


py.make_it_runnable()
py.fire(Tools)
