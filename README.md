# Notes only for Andrew Ng's students (funny project)

A project we built to pass a lab in the university about using HTTP protocol, we used ML for face verification and also used a picture of Andrew Ng as background (just to show our appreciation for this great sensi)

## About the Project 

The goal of the lab was to learn about connection protocols, so we decided to build a website using the following:

-Python

-[Flask framework](https://flask.palletsprojects.com/en/3.0.x/) (to implement the back-end)

-[SQLite](https://docs.python.org/3/library/sqlite3.html) in python

-frontend tools(HTML, CSS, JS, Bootstrap, [jinja2](https://flask.palletsprojects.com/en/2.3.x/templating/))

-[TensorFlow](https://www.tensorflow.org/), [Keras](https://keras.io/), and [Numpy](https://numpy.org/) for the face verification (we used the [Facenet](https://github.com/davidsandberg/facenet/tree/master) which's built on [inceptionv1](https://github.com/davidsandberg/facenet/blob/master/src/models/inception_resnet_v1.py) model for feature extraction, without post-training, you can find the Facenet paper [here](https://arxiv.org/pdf/1503.03832.pdf)) 

-[Pytesseract](https://pypi.org/project/pytesseract/) for fake ID scanning

### Website features

- Sign up and log in
- CRUD operations on notes
- forget your password (scanning fake ID and face verification)

## Side notes

The lab task was a small project about HTTP protocol, but we decided to put some ML sprinkles, it was just a small funny project.

## Words of thanks 

For the great sensi [Andrew Ng](https://www.linkedin.com/in/andrewyng/) for the valuable materials we've learned from his courses on [Coursera](https://www.coursera.org/) and [Deepleaning.ai](https://learn.deeplearning.ai/).

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change
