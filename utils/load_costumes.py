import os


def load_costumes(costumes_directory: str):
    costumes = {}

    for file in os.listdir(costumes_directory):
        if file.endswith(".png"):
            filename = file.split(".")[0]
            filename = "-".join(filename.split("-")[1::])
            costumes[filename] = os.path.join(costumes_directory, file)

    return costumes
