# coding=utf-8
from app.application import Application


app = Application("config.ini")

# app.add_handlers()


if __name__ == "__main__":
    app.run(address="0.0.0.0", port=8889)