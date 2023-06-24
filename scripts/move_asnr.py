import shutil


def move_files(file_paths, destination_folder):
    for file_path in file_paths:
        file_path = file_path.strip()
        try:
            shutil.copy(file_path, destination_folder)
            print(f"Moved {file_path} to {destination_folder}")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except PermissionError:
            print(f"Permission denied for {file_path}.")
        except Exception as e:
            print(f"An error occurred while moving {file_path}: {str(e)}")


def read_file_paths(file_path):
    with open(file_path, "r") as file:
        return file.read().splitlines()


if __name__ == "__main__":
    # Update paths
    input_file = "out/final_datasets.txt"
    destination_folder = "./datasets/"

    file_paths = read_file_paths(input_file)
    move_files(file_paths, destination_folder)
